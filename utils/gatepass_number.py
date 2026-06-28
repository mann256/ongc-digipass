from datetime import datetime

from models.gate_pass import GatePass


def generate_gatepass_number(location):

    today = datetime.now()

    year = today.strftime("%Y")

    month = today.strftime("%m")

    location = location.strip().upper()

    prefix = f"{year}/{month}/{location}/"

    latest_pass = (

        GatePass.query

        .filter(

            GatePass.gp_number.like(f"{prefix}%")

        )

        .order_by(

            GatePass.id.desc()

        )

        .first()

    )

    if latest_pass:

        last_number = int(

            latest_pass.gp_number.split("/")[-1]

        )

        sequence = last_number + 1

    else:

        sequence = 1

    return f"{prefix}{sequence:03d}"