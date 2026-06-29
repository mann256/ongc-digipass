from database.db import db


class GatePass(db.Model):

    __tablename__ = "gate_passes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    gp_number = db.Column(
        db.String(50),
        unique=True
    )

    gatepass_date = db.Column(
        db.String(20)
    )

    location = db.Column(
        db.String(100)
    )

    dispatched_from = db.Column(
        db.String(100)
    )

    dispatched_to = db.Column(
        db.String(100)
    )

    vehicle_type = db.Column(
        db.String(50)
    )

    vehicle_number = db.Column(
        db.String(50)
    )

    eway_bill_no = db.Column(
        db.String(100)
    )

    address_to = db.Column(
        db.String(200)
    )

    receiver_cpf = db.Column(
        db.String(20)
    )

    receiver_name = db.Column(
        db.String(100)
    )

    returnable = db.Column(
        db.String(10)
    )

    created_by_name = db.Column(
        db.String(100)
    )

    created_by_cpf = db.Column(
        db.String(20)
    )

    status = db.Column(
        db.String(20),
        default="PENDING"
    )

    approved_by = db.Column(
    db.String(100)
    )

    rejected_by = db.Column(
        db.String(100)
    )

    approving_authority = db.Column(
    db.String(100)
    )

    checkout_guard_name = db.Column(
        db.String(100)
    )

    checkout_time = db.Column(
        db.DateTime
    )

    checkout_remarks = db.Column(
        db.String(250)
    )

    checkin_guard_name = db.Column(
        db.String(100)
    )

    checkin_time = db.Column(
        db.DateTime
    )

    checkin_remarks = db.Column(
        db.String(250)
    )

    # -------------------------
    # Returnable Gate Pass Flow
    # -------------------------

    trip_number = db.Column(
        db.Integer,
        default=1,
        nullable=False
    )

    # First Movement

    first_checkout_guard_name = db.Column(
        db.String(100)
    )

    first_checkout_time = db.Column(
        db.DateTime
    )

    first_checkout_remarks = db.Column(
        db.String(250)
    )

    first_checkin_guard_name = db.Column(
        db.String(100)
    )

    first_checkin_time = db.Column(
        db.DateTime
    )

    first_checkin_remarks = db.Column(
        db.String(250)
    )

    # Second Movement

    second_checkout_guard_name = db.Column(
        db.String(100)
    )

    second_checkout_time = db.Column(
        db.DateTime
    )

    second_checkout_remarks = db.Column(
        db.String(250)
    )

    second_checkin_guard_name = db.Column(
        db.String(100)
    )

    second_checkin_time = db.Column(
        db.DateTime
    )

    second_checkin_remarks = db.Column(
        db.String(250)
    )
