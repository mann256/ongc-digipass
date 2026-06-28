from database.db import db


class GatePassItem(db.Model):

    __tablename__ = "gate_pass_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    gate_pass_id = db.Column(
        db.Integer,
        db.ForeignKey("gate_passes.id")
    )

    item_no = db.Column(
        db.Integer
    )

    material_description = db.Column(
        db.String(200)
    )

    asset_serial_no = db.Column(
        db.String(200)
    )

    qty = db.Column(
        db.Integer
    )

    remarks = db.Column(
        db.String(300)
    )