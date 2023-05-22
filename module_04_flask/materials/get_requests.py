from typing import List, Optional

from flask import Flask, request

app = Flask(__name__)


@app.route(
    "/search/", methods=["GET"],
)
def search():
    cell_tower_ids: List[int] = request.args.getlist("cell_tower_id", type=int)
    if not cell_tower_ids:
        return f"You must specify at least one cell_tower_id", 400

    phone_prefixes: List[str] = request.args.getlist("phone_prefix")

    protocols: List[str] = request.args.getlist("protocol")

    signal_level: Optional[float] = request.args.get(
        "signal_level", type=float, default=None
    )

    date_from: List[int] = request.args.getlist("date_from", type=int)
    date_to: List[int] = request.args.getlist("date_to", type=int)
    if date_from > date_to:
        return "'Date_to' must be later than 'Date_from'", 400

    return (
        f"Search for {cell_tower_ids} cell towers. Search criteria: "
        f"phone_prefixes={phone_prefixes}, "
        f"protocols={protocols}, "
        f"signal_level={signal_level}, "
        f"date_from={date_from}, "
        f"date_to={date_to}"
    )


if __name__ == "__main__":
    app.run(debug=True)
