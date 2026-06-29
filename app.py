from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import send_file
from flask import session
from datetime import datetime

from config import Config
from database.db import db
from models.user import User
from models.gate_pass import GatePass
from models.gate_pass_item import GatePassItem
from utils.pdf_generator import (
    generate_gatepass_pdf
)
from utils.gatepass_number import generate_gatepass_number
from utils.excel_report import generate_gatepass_excel

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Configure app
app.config.from_object(Config)
print(Config.SQLALCHEMY_DATABASE_URI)

# Initialize database
db.init_app(app)
@app.context_processor
def inject_user():

    return {

        "current_user":
        session.get("name"),

        "current_role":
        session.get("role"),

        "current_cpf":
        session.get("cpf")

    }

# Create tables
with app.app_context():
    db.create_all()
    
    print("Tables created")


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        cpf = request.form.get("cpf")
        password = request.form.get("password")

        print("CPF:", cpf)
        print("Password:", password)

        user = User.query.filter_by(
            cpf=cpf
        ).first()

        print("User Found:", user)

        if user and user.password == password:

            session["user_id"] = user.id

            session["cpf"] = user.cpf

            session["name"] = user.name

            session["role"] = user.role

            return redirect(
                url_for("home")
            )

        print("LOGIN FAILED")

    return render_template(
        "login.html"
    )


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    if session["role"] == "USER":

        query = GatePass.query.filter_by(
            created_by_cpf=session["cpf"]
        )

    else:

        query = GatePass.query

    pending_count = query.filter_by(
        status="PENDING"
    ).count()

    approved_count = query.filter_by(
        status="APPROVED"
    ).count()

    rejected_count = query.filter_by(
        status="REJECTED"
    ).count()

    cancelled_count = query.filter_by(
        status="CANCELLED"
    ).count()

    in_transit_count = query.filter_by(
        status="IN_TRANSIT"
    ).count()

    completed_count = query.filter_by(
        status="COMPLETED"
    ).count()

    total_count = query.count()

    return render_template(

        "dashboard.html",

        pending_count=pending_count,

        approved_count=approved_count,

        rejected_count=rejected_count,

        cancelled_count=cancelled_count,

        in_transit_count=in_transit_count,

        completed_count=completed_count,

        total_count=total_count

    )

@app.route("/home")
def home():

    return render_template(
        "home.html"
    )

@app.route("/site-details")
def site_details():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    if session["role"] not in [

        "ADMIN",

        "HEAD_INFOCOM"

    ]:

        return "Access Denied", 403

    locations = [

        "Infocom",

        "Avani Bhavan",

        "Sabarmati"

    ]

    data = []

    for location in locations:

        total = GatePass.query.filter_by(
            location=location
        ).count()

        pending = GatePass.query.filter_by(
            location=location,
            status="PENDING"
        ).count()

        approved = GatePass.query.filter_by(
            location=location,
            status="APPROVED"
        ).count()

        rejected = GatePass.query.filter_by(
            location=location,
            status="REJECTED"
        ).count()

        data.append({

            "name": location,

            "total": total,

            "pending": pending,

            "approved": approved,

            "rejected": rejected

        })

    return render_template(

        "site_details.html",

        locations=data

    )

@app.route(
    "/create-gatepass",
    methods=["GET", "POST"]
)
def create_gatepass():

    if request.method == "POST":

        gatepass_date = request.form.get(
            "gatepass_date"
        )

        location = request.form.get(
            "location"
        )

        dispatched_from = request.form.get(
            "dispatched_from"
        )

        dispatched_to = request.form.get(
            "dispatched_to"
        )

        vehicle_type = request.form.get(
            "vehicle_type"
        )

        vehicle_number = request.form.get(
            "vehicle_number"
        )

        eway_bill_no = request.form.get(
            "eway_bill_no"
        )

        receiver_cpf = request.form.get(
            "receiver_cpf"
        )

        receiver_name = request.form.get(
            "receiver_name"
        )

        approving_authority = request.form.get(
            "approving_authority"
        )

        returnable = request.form.get(
            "returnable"
        )

        print(
            "Authority:",
            approving_authority
        )

        gp_number = generate_gatepass_number(
            request.form["location"]
        )

        gate_pass = GatePass(

            gp_number=gp_number,

            gatepass_date=gatepass_date,

            location=location,

            dispatched_from=dispatched_from,

            dispatched_to=dispatched_to,

            vehicle_type=vehicle_type,

            vehicle_number=vehicle_number,

            eway_bill_no=eway_bill_no,

            receiver_cpf=receiver_cpf,

            receiver_name=receiver_name,

            approving_authority=approving_authority,

            returnable=returnable,

            created_by_name=session["name"],

            created_by_cpf=session["cpf"],

            status="PENDING"

        )

        db.session.add(
            gate_pass
        )

        db.session.commit()

        # -----------------------------
        # Save Item Details
        # -----------------------------

        item_numbers = request.form.getlist(
            "item_no[]"
        )

        materials = request.form.getlist(
            "material_description[]"
        )

        assets = request.form.getlist(
            "asset_serial_no[]"
        )

        census_no = request.form.getlist(
            "census_no[]"
        )

        qtys = request.form.getlist(
            "qty[]"
        )

        remarks = request.form.getlist(
            "remarks[]"
        )

        for i in range(
            len(item_numbers)
        ):

            item = GatePassItem(

                gate_pass_id=gate_pass.id,

                item_no=item_numbers[i],

                material_description=materials[i],

                asset_serial_no=assets[i],

                census_no=census_no[i],

                qty=qtys[i],

                remarks=remarks[i]

            )

            db.session.add(
                item
            )

        db.session.commit()

        return redirect(

            url_for(
                "gatepass_list"
            )

        )

    return render_template(
        "create_gatepass.html"
    )


@app.route(
    "/edit-gatepass/<int:gatepass_id>",
    methods=["GET", "POST"]
)
def edit_gatepass(gatepass_id):

    gate_pass = GatePass.query.get_or_404(
        gatepass_id
    )

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    items = (
        GatePassItem.query
        .filter_by(
            gate_pass_id=gate_pass.id
        )
        .order_by(
            GatePassItem.item_no
        )
        .all()
    )

    role = session["role"]

    if role == "USER":

        if gate_pass.created_by_cpf != session["cpf"]:

            return "Access Denied", 403

        if gate_pass.status != "PENDING":

            return "Cannot Edit", 403

    elif role in [

        "ADMIN",

        "HEAD_INFOCOM"

    ]:

        if gate_pass.status in [

            "CANCELLED",

            "COMPLETED"

        ]:

            return "Cannot Edit", 403

    else:

        return "Access Denied", 403

    if request.method == "POST":

        gate_pass.gatepass_date = request.form.get(
            "gatepass_date"
        )

        gate_pass.location = request.form.get(
            "location"
        )

        gate_pass.dispatched_from = request.form.get(
            "dispatched_from"
        )

        gate_pass.dispatched_to = request.form.get(
            "dispatched_to"
        )

        gate_pass.vehicle_type = request.form.get(
            "vehicle_type"
        )

        gate_pass.vehicle_number = request.form.get(
            "vehicle_number"
        )

        gate_pass.eway_bill_no = request.form.get(
            "eway_bill_no"
        )

        gate_pass.receiver_cpf = request.form.get(
            "receiver_cpf"
        )

        gate_pass.receiver_name = request.form.get(
            "receiver_name"
        )

        gate_pass.returnable = request.form.get(
            "returnable"
        )

        gate_pass.approving_authority = request.form.get(
            "approving_authority"
        )

        GatePassItem.query.filter_by(

            gate_pass_id=gate_pass.id

        ).delete()

        item_numbers = request.form.getlist(
            "item_no[]"
        )

        materials = request.form.getlist(
            "material_description[]"
        )

        assets = request.form.getlist(
            "asset_serial_no[]"
        )

        census_no = request.form.getlist(
            "census_no[]"
        )

        qtys = request.form.getlist(
            "qty[]"
        )

        remarks = request.form.getlist(
            "remarks[]"
        )

        for i in range(len(item_numbers)):

            item = GatePassItem(

                gate_pass_id=gate_pass.id,

                item_no=item_numbers[i],

                material_description=materials[i],

                asset_serial_no=assets[i],

                census_no=census_no[i],

                qty=qtys[i],

                remarks=remarks[i]

            )

            db.session.add(
                item
            )

        db.session.commit()

        return redirect(

            url_for(

                "view_gatepass",

                gatepass_id=gate_pass.id

            )

        )

    return render_template(

        "create_gatepass.html",

        edit=True,

        gate_pass=gate_pass,

        items=items

    )


@app.route(
    "/cancel-gatepass/<int:gatepass_id>",
    methods=["GET", "POST"]
)
def cancel_gatepass(gatepass_id):

    gate_pass = GatePass.query.get_or_404(
        gatepass_id
    )

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    role = session["role"]

    if role == "USER":

        if gate_pass.created_by_cpf != session["cpf"]:

            return "Access Denied", 403

        if gate_pass.status not in [

            "PENDING",

            "APPROVED"

        ]:

            return "Cannot Cancel", 403

    elif role in [

        "ADMIN",

        "HEAD_INFOCOM"

    ]:

        if gate_pass.status in [

            "COMPLETED",

            "CANCELLED"

        ]:

            return "Cannot Cancel", 403

    else:

        return "Access Denied", 403

    if request.method == "POST":

        gate_pass.status = "CANCELLED"

        gate_pass.cancel_reason = request.form.get(
            "cancel_reason"
        )

        db.session.commit()

        return redirect(

            url_for(

                "view_gatepass",

                gatepass_id=gate_pass.id,

                success="cancelled"

            )

        )

    return render_template(

        "cancel_gatepass.html",

        gate_pass=gate_pass

    )

@app.route("/gatepass-list")
def gatepass_list():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    if session["role"] == "USER":

        query = GatePass.query.filter_by(

            created_by_cpf=session["cpf"]

        )

    else:

        query = GatePass.query

    # ----------------------------------
    # Location Filter
    # ----------------------------------

    location = request.args.get("location")

    if location:

        query = query.filter_by(
            location=location
        )

    # ----------------------------------
    # From Date Filter
    # ----------------------------------

    from_date = request.args.get("from_date")

    if from_date:

        query = query.filter(
            GatePass.gatepass_date >= from_date
        )

    # ----------------------------------
    # To Date Filter
    # ----------------------------------

    to_date = request.args.get("to_date")

    if to_date:

        query = query.filter(
            GatePass.gatepass_date <= to_date
        )

    # ----------------------------------
    # Status Filter
    # ----------------------------------

    status = request.args.get("status")

    if status:

        query = query.filter_by(
            status=status
        )

    gate_passes = (

        query

        .order_by(
            GatePass.id.desc()
        )

        .all()

    )

    return render_template(

        "gatepass_list.html",

        gate_passes=gate_passes

    )

@app.route(
    "/view-gatepass/<int:gatepass_id>"
)
def view_gatepass(gatepass_id):

    gate_pass = GatePass.query.get_or_404(
        gatepass_id
    )

    if (

        session["role"] == "USER"

        and

        gate_pass.created_by_cpf != session["cpf"]

    ):

        return "Access Denied", 403

    items = (
        GatePassItem.query
        .filter_by(
            gate_pass_id=gatepass_id
        )
        .all()
    )

    return render_template(

        "view_gatepass.html",

        gate_pass=gate_pass,

        items=items,

        success=request.args.get("success"),

        admin_role=session.get("role")
    )

@app.route(
    "/print-gatepass/<int:gatepass_id>"
)
def print_gatepass(gatepass_id):

    gate_pass = GatePass.query.get_or_404(
        gatepass_id
    )

    if (

        session["role"] == "USER"

        and

        gate_pass.created_by_cpf != session["cpf"]

    ):

        return "Access Denied", 403

    items = (
        GatePassItem.query
        .filter_by(
            gate_pass_id=gatepass_id
        )
        .all()
    )

    pdf_path = generate_gatepass_pdf(

        gate_pass=gate_pass,

        items=items,

        admin_name=Config.ADMIN_NAME,

        admin_role=Config.ADMIN_ROLE

    )

    return send_file(

        pdf_path,

        as_attachment=True,

        download_name=f"{gate_pass.gp_number}.pdf"

    )

@app.route("/export-gatepass-report")
def export_gatepass_report():

    file_path = generate_gatepass_excel()

    return send_file(
        file_path,
        as_attachment=True,
        download_name="gatepass_last_30_days.xlsx"
    )

@app.route(
    "/approve-gatepass/<int:gatepass_id>"
)
def approve_gatepass(gatepass_id):

    if session["role"] not in [

        "ADMIN",

        "HEAD_INFOCOM"

    ]:

        return "Access Denied", 403

    gate_pass = GatePass.query.get_or_404(
        gatepass_id
    )

    gate_pass.status = "APPROVED"

    gate_pass.approved_by = (
        gate_pass.approving_authority
    )

    db.session.commit()

    return redirect(
        url_for(
            "view_gatepass",
            gatepass_id=gate_pass.id,
            success="approved"
        )
    )

@app.route(
    "/reject-gatepass/<int:gatepass_id>"
)
def reject_gatepass(gatepass_id):

    if session["role"] not in [

        "ADMIN",

        "HEAD_INFOCOM"

    ]:

        return "Access Denied", 403

    gate_pass = GatePass.query.get_or_404(
        gatepass_id
    )

    gate_pass.status = "REJECTED"

    gate_pass.rejected_by = (
        gate_pass.approving_authority
    )

    db.session.commit()

    return redirect(
        url_for(
            "view_gatepass",
            gatepass_id=gate_pass.id,
            success="rejected"
        )
    )


@app.route(
    "/security",
    methods=["GET", "POST"]
)
def security_scan():

    gp_number = request.args.get("gp")

    gate_pass = GatePass.query.filter_by(
        gp_number=gp_number
    ).first_or_404()

    items = (
        GatePassItem.query
        .filter_by(
            gate_pass_id=gate_pass.id
        )
        .order_by(
            GatePassItem.item_no
        )
        .all()
    )


    if request.method == "POST":

        cpf = request.form.get(
            "cpf"
        )

        password = request.form.get(
            "password"
        )

        guard_name = request.form.get(
            "guard_name"
        )

        remarks = request.form.get(
            "remarks"
        )

        action = request.form.get(
            "action"
        )

        security = User.query.filter_by(

            cpf=cpf,

            password=password,

            role="GATE_SECURITY"

        ).first()

        if not security:

            return "Invalid Security Credentials", 403
        
        if action == "accept":

            # ==========================================
            # NON-RETURNABLE GATE PASS
            # ==========================================

            if gate_pass.returnable == "NO":

                if gate_pass.status == "APPROVED":

                    gate_pass.status = "IN_TRANSIT"

                    gate_pass.checkout_guard_name = guard_name
                    gate_pass.checkout_time = datetime.now()
                    gate_pass.checkout_remarks = remarks

                elif gate_pass.status == "IN_TRANSIT":

                    gate_pass.status = "COMPLETED"

                    gate_pass.checkin_guard_name = guard_name
                    gate_pass.checkin_time = datetime.now()
                    gate_pass.checkin_remarks = remarks

                elif gate_pass.status == "COMPLETED":

                    return "Gate Pass Already Completed"

                elif gate_pass.status == "CANCELLED":

                    return "Gate Pass Already Cancelled"

                else:

                    return f"Invalid Gate Pass Status : {gate_pass.status}", 400

            # ==========================================
            # RETURNABLE GATE PASS
            # ==========================================

            else:

                # First Checkout
                if gate_pass.status == "APPROVED":

                    gate_pass.status = "IN_TRANSIT"
                    gate_pass.trip_number = 1

                    gate_pass.first_checkout_guard_name = guard_name
                    gate_pass.first_checkout_time = datetime.now()
                    gate_pass.first_checkout_remarks = remarks

                # First Check-In
                elif (
                    gate_pass.status == "IN_TRANSIT"
                    and gate_pass.trip_number == 1
                ):

                    gate_pass.status = "IN_TRANSIT"
                    gate_pass.trip_number = 2

                    gate_pass.first_checkin_guard_name = guard_name
                    gate_pass.first_checkin_time = datetime.now()
                    gate_pass.first_checkin_remarks = remarks

                # Second Checkout
                elif (
                    gate_pass.status == "IN_TRANSIT"
                    and gate_pass.trip_number == 2
                ):

                    gate_pass.trip_number = 3

                    gate_pass.second_checkout_guard_name = guard_name
                    gate_pass.second_checkout_time = datetime.now()
                    gate_pass.second_checkout_remarks = remarks

                # Second Check-In
                elif (
                    gate_pass.status == "IN_TRANSIT"
                    and gate_pass.trip_number == 3
                ):

                    gate_pass.status = "COMPLETED"

                    gate_pass.second_checkin_guard_name = guard_name
                    gate_pass.second_checkin_time = datetime.now()
                    gate_pass.second_checkin_remarks = remarks

                elif gate_pass.status == "COMPLETED":

                    return "Gate Pass Already Completed"

                elif gate_pass.status == "CANCELLED":

                    return "Gate Pass Already Cancelled"

                else:

                    return f"Invalid Gate Pass Status : {gate_pass.status}", 400
            
        elif action == "decline":

            gate_pass.status = "CANCELLED"

            gate_pass.security_remarks = remarks

        print("=" * 60)

        if gate_pass.returnable == "NO":

            print("NON-RETURNABLE")

            print("Status:", gate_pass.status)

            print("Checkout Guard:", gate_pass.checkout_guard_name)
            print("Checkout Time:", gate_pass.checkout_time)
            print("Checkout Remarks:", gate_pass.checkout_remarks)

            print("Checkin Guard:", gate_pass.checkin_guard_name)
            print("Checkin Time:", gate_pass.checkin_time)
            print("Checkin Remarks:", gate_pass.checkin_remarks)

        else:

            print("RETURNABLE")

            print("Status:", gate_pass.status)
            print("Trip:", gate_pass.trip_number)

            print("First Checkout Guard:", gate_pass.first_checkout_guard_name)
            print("First Checkout Time:", gate_pass.first_checkout_time)
            print("First Checkout Remarks:", gate_pass.first_checkout_remarks)

            print("First Checkin Guard:", gate_pass.first_checkin_guard_name)
            print("First Checkin Time:", gate_pass.first_checkin_time)
            print("First Checkin Remarks:", gate_pass.first_checkin_remarks)

            print("Second Checkout Guard:", gate_pass.second_checkout_guard_name)
            print("Second Checkout Time:", gate_pass.second_checkout_time)
            print("Second Checkout Remarks:", gate_pass.second_checkout_remarks)

            print("Second Checkin Guard:", gate_pass.second_checkin_guard_name)
            print("Second Checkin Time:", gate_pass.second_checkin_time)
            print("Second Checkin Remarks:", gate_pass.second_checkin_remarks)

        print("=" * 60)

        db.session.commit()

        return redirect(

            url_for(

                "security_scan",

                gp=gate_pass.gp_number

            )

        )

    return render_template(

        "security_scan.html",

        gate_pass=gate_pass,

        items=items

    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )