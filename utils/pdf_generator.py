import os
import qrcode

from datetime import datetime
from flask import request


from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet
)
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    HRFlowable
)
from reportlab.pdfgen import canvas
from config import BASE_URL


# ----------------------------------------------------------
# Page Border
# ----------------------------------------------------------

class GatePassCanvas(canvas.Canvas):

    def __init__(

        self,

        *args,

        **kwargs

    ):

        super().__init__(

            *args,

            **kwargs

        )

    def draw_page_border(self):

        self.setStrokeColor(

            colors.darkblue

        )

        self.setLineWidth(

            2

        )

        self.rect(
            20,
            20,
            555,
            802
        )

        self.setLineWidth(0.8)

        self.rect(
            28,
            28,
            539,
            786
        )

        self.saveState()

        self.setFont(
            "Helvetica-Bold",
            60
        )

        self.setFillGray(
            0.95
        )

    def showPage(self):

        self.draw_page_border()

        super().showPage()

    def save(self):

        self.draw_page_border()

        super().save()


# ----------------------------------------------------------
# PDF Generator
# ----------------------------------------------------------

def generate_gatepass_pdf(

    gate_pass,

    items,

    admin_name,

    admin_role

):

    reports_folder = (
        "generated_gatepasses"
    )

    os.makedirs(

        reports_folder,

        exist_ok=True

    )

    safe_gp_number = gate_pass.gp_number.replace("/", "_")

    pdf_path = os.path.join(
        reports_folder,
        f"{safe_gp_number}.pdf"
    )

    qr_path = os.path.join(
        reports_folder,
        f"{safe_gp_number}.png"
    )

    qr_url = (

        request.url_root.rstrip("/") + f"/security?gp={gate_pass.gp_number}"

    )

    qr = qrcode.make(

        qr_url

    )

    qr.save(

        qr_path

    )

    doc = SimpleDocTemplate(

        pdf_path,

        rightMargin=30,

        leftMargin=30,

        topMargin=25,

        bottomMargin=25

    )

    styles = getSampleStyleSheet()

    story = []

    # ------------------------------------------------------
    # Custom Styles
    # ------------------------------------------------------

    title_style = ParagraphStyle(

        "TitleStyle",

        parent=styles["Title"],

        alignment=TA_CENTER,

        fontSize=20,

        leading=24,

        textColor=colors.darkblue

    )

    subtitle_style = ParagraphStyle(

        "SubTitle",

        parent=styles["Heading2"],

        alignment=TA_CENTER,

        fontSize=13,

        leading=16,

        textColor=colors.black

    )

    normal_style = ParagraphStyle(

        "Normal",

        parent=styles["Normal"],

        fontSize=10,

        leading=14

    )

    heading_style = ParagraphStyle(

        "Heading",

        parent=styles["Heading2"],

        alignment=TA_CENTER,

        fontSize=12,

        textColor=colors.white,

        backColor=colors.HexColor("#004C99"),

        spaceAfter=10,

        spaceBefore=10

    )

    # ------------------------------------------------------
    # PROFESSIONAL HEADER
    # ------------------------------------------------------

    logo_path = os.path.join(
        "static",
        "images",
        "ongc_logo.png"
    )

    logo = ""

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=1.2 * inch,
            height=0.9 * inch
        )

    qr_image = Image(
        qr_path,
        width=0.9 * inch,
        height=0.9 * inch
    )

    company_style = ParagraphStyle(
        "CompanyStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=16,
        leading=18,
        textColor=colors.darkblue
    )

    gatepass_style = ParagraphStyle(
        "GatePassStyle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        fontSize=13,
        leading=15,
        textColor=colors.black
    )

    center_style = ParagraphStyle(
        "CenterStyle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10
    )

    company_text = Paragraph(
        """
        <b>OIL AND NATURAL GAS CORPORATION LIMITED</b>
        <br/>
        <font size="14"><b>MATERIAL GATE PASS</b></font>
        <br/>
        Internal Material Movement System
        """,
        company_style
    )

    header_table = Table(
        [
            [
                logo,
                company_text,
                qr_image
            ]
        ],
        colWidths=[70, 370, 70]
    )

    header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                ("ALIGN", (0,0), (0,0), "CENTER"),
                ("ALIGN", (1,0), (1,0), "CENTER"),
                ("ALIGN", (2,0), (2,0), "CENTER"),
                ("BOTTOMPADDING", (0,0), (-1,-1), 10)
            ]
        )
    )

    story.append(header_table)

    story.append(
        HRFlowable(
            width="100%",
            thickness=2,
            color=colors.darkblue
        )
    )

    story.append(
        Spacer(
            1,
            12
        )
    )


    # ------------------------------------------------------
    # GATE PASS INFORMATION
    # ------------------------------------------------------

    story.append(

        Paragraph(

            "GATE PASS DETAILS",

            heading_style

        )

    )

    info_data = [

        [

            "<b>Gate Pass No.</b>",

            gate_pass.gp_number,

            "<b>Date</b>",

            gate_pass.gatepass_date

        ],

        [

            "<b>Status</b>",

            gate_pass.status,

            "<b>Returnable</b>",

            gate_pass.returnable

        ],

        [

            "<b>Location</b>",

            gate_pass.location,

            "<b>Vehicle Type</b>",

            gate_pass.vehicle_type

        ],

        [

            "<b>Vehicle Number</b>",

            gate_pass.vehicle_number,

            "<b>E-Way Bill</b>",

            gate_pass.eway_bill_no
            if gate_pass.eway_bill_no
            else "-"

        ],

        [

            "<b>Dispatched From</b>",

            gate_pass.dispatched_from,

            "<b>Dispatched To</b>",

            gate_pass.dispatched_to

        ],

        [

            "<b>Receiver CPF</b>",

            gate_pass.receiver_cpf,

            "<b>Receiver Name</b>",

            gate_pass.receiver_name

        ],

        [

            "<b>Created By</b>",

            gate_pass.created_by_name

        ]

    ]

    formatted_info = []

    for row in info_data:

        formatted_info.append(

            [

                Paragraph(
                    row[0],
                    normal_style
                ),

                Paragraph(
                    str(row[1]),
                    normal_style
                ),

                Paragraph(
                    row[2],
                    normal_style
                ),

                Paragraph(
                    str(row[3]),
                    normal_style
                )

            ]

        )

    info_table = Table(

        formatted_info,

        colWidths=[120, 150, 120, 150]

    )

    info_table.setStyle(
        TableStyle(

            [

                ("GRID", (0,0), (-1,-1), 0.6, colors.grey),

                ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#D9EAF7")),

                ("BACKGROUND", (2,0), (2,-1), colors.HexColor("#D9EAF7")),

                ("TEXTCOLOR", (0,0), (0,-1), colors.darkblue),

                ("TEXTCOLOR", (2,0), (2,-1), colors.darkblue),

                ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),

                ("FONTNAME", (2,0), (2,-1), "Helvetica-Bold"),

                ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

                ("TOPPADDING", (0,0), (-1,-1), 10),

                ("BOTTOMPADDING", (0,0), (-1,-1), 10),

                ("LEFTPADDING", (0,0), (-1,-1), 8),

                ("RIGHTPADDING", (0,0), (-1,-1), 8)

            ]

        )

    )

    story.append(

        info_table

    )

    story.append(

        Spacer(

            1,

            15

        )

    )


    # ------------------------------------------------------
    # ITEM DETAILS
    # ------------------------------------------------------

    story.append(

        Paragraph(

            "MATERIAL DETAILS",

            heading_style

        )

    )

    item_data = [

        [

            Paragraph(
                "<b>Sl. No.</b>",
                normal_style
            ),

            Paragraph(
                "<b>Material Description</b>",
                normal_style
            ),

            Paragraph(
                "<b>Asset / Serial Number</b>",
                normal_style
            ),

            Paragraph(
                "<b>Quantity</b>",
                normal_style
            ),

            Paragraph(
                "<b>Remarks</b>",
                normal_style
            )

        ]

    ]

    if len(items) == 0:

        item_data.append(

            [

                "-",

                "No Item Added",

                "-",

                "-",

                "-"

            ]

        )

    else:

        for item in items:

            item_data.append(

                [

                    Paragraph(
                        str(item.item_no),
                        normal_style
                    ),

                    Paragraph(
                        str(item.material_description),
                        normal_style
                    ),

                    Paragraph(
                        str(item.asset_serial_no),
                        normal_style
                    ),

                    Paragraph(
                        str(item.qty),
                        normal_style
                    ),

                    Paragraph(
                        str(item.remarks),
                        normal_style
                    )

                ]

            )

    item_table = Table(

        item_data,

        colWidths=[50, 185, 140, 45, 120],

        repeatRows=1

    )

    item_table.setStyle(

        TableStyle(

            [

                # Outer Border
                ("BOX",(0,0),(-1,-1),1.2,colors.darkblue),

                # Grid
                ("GRID",(0,0),(-1,-1),0.4,colors.grey),

                # Header
                ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2F75B5")),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

                ("FONTSIZE",(0,0),(-1,0),11),

                ("ALIGN",(0,0),(-1,0),"CENTER"),

                ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

                ("BOTTOMPADDING",(0,0),(-1,0),10),

                ("TOPPADDING",(0,0),(-1,0),10),

                # Data Rows
                ("FONTNAME",(0,1),(-1,-1),"Helvetica"),

                ("FONTSIZE",(0,1),(-1,-1),9),

                ("TOPPADDING",(0,1),(-1,-1),8),

                ("BOTTOMPADDING",(0,1),(-1,-1),8),

                ("LEFTPADDING",(0,0),(-1,-1),6),

                ("RIGHTPADDING",(0,0),(-1,-1),6),

                ("ALIGN",(0,1),(0,-1),"CENTER"),

                ("ALIGN",(3,1),(3,-1),"CENTER"),

                ("ALIGN",(4,1),(4,-1),"CENTER"),

                # Alternate Row Colours
                ("ROWBACKGROUNDS",(0,1),(-1,-1),

                    [

                        colors.white,

                        colors.HexColor("#F8F9FA")

                    ]

                )

            ]

        )

    )

    
    story.append(
        item_table
    )

    story.append(
        Spacer(
            1,
            18
        )
    )

    # ------------------------------------------------------
    # SIGNATURES & QR CODE
    # ------------------------------------------------------

    story.append(

        Paragraph(

            "APPROVAL DETAILS",

            heading_style

        )

    )

    heading = "Approval Status"

    authority_name = "Pending Approval"

    if gate_pass.status in ["APPROVED", "COMPLETED"]:

        heading = "Approved By"

        authority_name = gate_pass.approved_by 

    elif gate_pass.status == "REJECTED":

        heading = "Rejected By"

        authority_name = gate_pass.rejected_by 

        

    # ------------------------------------------------------
    # APPROVAL DETAILS
    # ------------------------------------------------------

    approval_data = [

        [
            Paragraph("<b>Created By</b>", normal_style),
            Paragraph(str(gate_pass.created_by_name), normal_style)
        ],

        [
            Paragraph(f"<b>{heading}</b>", normal_style),
            Paragraph(str(authority_name), normal_style)
        ],

    ]

    approval_table = Table(

        approval_data,

        colWidths=[150, 360]

    )

    approval_table.setStyle(

        TableStyle(

            [

                ("BOX",(0,0),(-1,-1),1,colors.darkblue),

                ("GRID",(0,0),(-1,-1),0.5,colors.grey),

                ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#EAF2F8")),

                ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),

                ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

                ("TOPPADDING",(0,0),(-1,-1),10),

                ("BOTTOMPADDING",(0,0),(-1,-1),10)

            ]

        )

    )

    story.append(approval_table)

    story.append(

        Spacer(

            1,

            15

        )

    )

    # ------------------------------------------------------
    # SECURITY OUT
    # ------------------------------------------------------
    if gate_pass.returnable == "NO":

        story.append(

            Paragraph(

                "SECURITY OUT",

                heading_style

            )

        )

        security_out = [

            [
                Paragraph(
                    gate_pass.checkout_guard_name or "-",
                    normal_style
                )
            ],

            [
                Paragraph(
                    gate_pass.checkout_time.strftime("%d-%b-%Y %I:%M %p")
                    if gate_pass.checkout_time else "-",
                    normal_style
                )
            ],

            [
                Paragraph(
                    gate_pass.checkout_remarks or "-",
                    normal_style
                )
            ]

        ]

        security_out_table = Table(

            security_out,

            colWidths=[150,360]

        )

        security_out_table.setStyle(

            TableStyle(

                [

                    ("BOX",(0,0),(-1,-1),1,colors.darkblue),

                    ("GRID",(0,0),(-1,-1),0.5,colors.grey),

                    ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#EAF2F8")),

                    ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),

                    ("TOPPADDING",(0,0),(-1,-1),10),

                    ("BOTTOMPADDING",(0,0),(-1,-1),10)

                ]

            )

        )

        story.append(security_out_table)

        story.append(

            Spacer(

                1,

                15

            )

        )

        # ------------------------------------------------------
        # SECURITY IN
        # ------------------------------------------------------

        story.append(

            Paragraph(

                "SECURITY IN",

                heading_style

            )

        )

        security_in = [

            [
                Paragraph(
                    gate_pass.checkin_guard_name or "-",
                    normal_style
                )
            ],

            [
                Paragraph(
                    gate_pass.checkin_time.strftime("%d-%b-%Y %I:%M %p")
                    if gate_pass.checkin_time else "-",
                    normal_style
                )
            ],

            [
                Paragraph(
                    gate_pass.checkin_remarks or "-",
                    normal_style
                )
            ]

        ]

        security_in_table = Table(

            security_in,

            colWidths=[150,360]

        )

        security_in_table.setStyle(

            TableStyle(

                [

                    ("BOX",(0,0),(-1,-1),1,colors.darkblue),

                    ("GRID",(0,0),(-1,-1),0.5,colors.grey),

                    ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#EAF2F8")),

                    ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),

                    ("TOPPADDING",(0,0),(-1,-1),10),

                    ("BOTTOMPADDING",(0,0),(-1,-1),10)

                ]

            )

        )

        story.append(security_in_table)

        story.append(

            Spacer(

                1,

                20

            )

        )

    else:
        # ------------------------------------------------------
        # FIRST MOVEMENT
        # ------------------------------------------------------

        story.append(
            Paragraph(
                "FIRST MOVEMENT",
                heading_style
            )
        )

        first_movement = [

            ["Check Out Guard",
            gate_pass.first_checkout_guard_name or "-"],

            ["Check Out Time",
            gate_pass.first_checkout_time.strftime("%d-%b-%Y %I:%M %p")
            if gate_pass.first_checkout_time else "-"],

            ["Check Out Remarks",
            gate_pass.first_checkout_remarks or "-"],

            ["Check In Guard",
            gate_pass.first_checkin_guard_name or "-"],

            ["Check In Time",
            gate_pass.first_checkin_time.strftime("%d-%b-%Y %I:%M %p")
            if gate_pass.first_checkin_time else "-"],

            ["Check In Remarks",
            gate_pass.first_checkin_remarks or "-"]

        ]

        first_table = Table(
            first_movement,
            colWidths=[170,340]
        )

        first_table.setStyle(

            TableStyle([

                ("BOX",(0,0),(-1,-1),1,colors.darkblue),
                ("GRID",(0,0),(-1,-1),0.5,colors.grey),

                ("BACKGROUND",(0,0),(0,-1),
                colors.HexColor("#EAF2F8")),

                ("FONTNAME",(0,0),(0,-1),
                "Helvetica-Bold"),

                ("TOPPADDING",(0,0),(-1,-1),10),

                ("BOTTOMPADDING",(0,0),(-1,-1),10)

            ])

        )

        story.append(first_table)

        story.append(
            Spacer(
                1,
                20
            )
        )

        # ------------------------------------------------------
        # SECOND MOVEMENT
        # ------------------------------------------------------

        story.append(
            Paragraph(
                "SECOND MOVEMENT",
                heading_style
            )
        )

        second_movement = [

            ["Check Out Guard",
            gate_pass.second_checkout_guard_name or "-"],

            ["Check Out Time",
            gate_pass.second_checkout_time.strftime("%d-%b-%Y %I:%M %p")
            if gate_pass.second_checkout_time else "-"],

            ["Check Out Remarks",
            gate_pass.second_checkout_remarks or "-"],

            ["Check In Guard",
            gate_pass.second_checkin_guard_name or "-"],

            ["Check In Time",
            gate_pass.second_checkin_time.strftime("%d-%b-%Y %I:%M %p")
            if gate_pass.second_checkin_time else "-"],

            ["Check In Remarks",
            gate_pass.second_checkin_remarks or "-"]

        ]

        second_table = Table(
            second_movement,
            colWidths=[170,340]
        )

        second_table.setStyle(

            TableStyle([

                ("BOX",(0,0),(-1,-1),1,colors.darkblue),

                ("GRID",(0,0),(-1,-1),0.5,colors.grey),

                ("BACKGROUND",(0,0),(0,-1),
                colors.HexColor("#EAF2F8")),

                ("FONTNAME",(0,0),(0,-1),
                "Helvetica-Bold"),

                ("TOPPADDING",(0,0),(-1,-1),10),

                ("BOTTOMPADDING",(0,0),(-1,-1),10)

            ])

        )

        story.append(second_table)

        story.append(
            Spacer(
                1,
                20
            )
        )

    # ------------------------------------------------------
    # FOOTER
    # ------------------------------------------------------

    generated_time = datetime.now().strftime(

        "%d-%b-%Y %I:%M %p"

    )

    footer = Table(

        [

            [

                Paragraph(

                    f"""

                    <b>Generated On :</b>

                    {generated_time}

                    """,

                    normal_style

                )

            ],

            [

                Paragraph(

                    "<b>Computer Generated Document - No Signature Required</b>",

                    ParagraphStyle(

                        "Footer",

                        parent=normal_style,

                        alignment=TA_CENTER,

                        textColor=colors.grey,

                        fontSize=9

                    )

                )

            ]

        ],

        colWidths=[510]

    )

    footer.setStyle(

        TableStyle(

            [

                ("LINEABOVE",(0,0),(-1,0),1,colors.darkblue),

                ("TOPPADDING",(0,0),(-1,-1),8),

                ("BOTTOMPADDING",(0,0),(-1,-1),8),

                ("ALIGN",(0,0),(-1,-1),"CENTER")

            ]

        )

    )

    story.append(

        footer

    )

    # ------------------------------------------------------
    # BUILD PDF
    # ------------------------------------------------------

    doc.build(

        story,

        canvasmaker=GatePassCanvas

    )

    return pdf_path
