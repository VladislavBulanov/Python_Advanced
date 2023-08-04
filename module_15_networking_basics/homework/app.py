from flask import Flask, request, jsonify
from typing import List

from models import (
    Room,
    Booking,
    create_tables,
    insert_room,
    get_rooms,
    is_room_booked,
    insert_booking,
)

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = "sample_key"


@app.route("/add-room", methods=["POST"])
def add_room():
    # Parse the request data as JSON:
    data = request.get_json()

    # Create a new "Room" object from the request data:
    new_room = Room(
        room_id=0,
        floor=data["floor"],
        beds=data["beds"],
        guest_num=data["guestNum"],
        price=data["price"],
    )

    room_id = insert_room(new_room)
    return jsonify({"roomId": room_id}), 200


@app.route("/room", methods=["GET"])
def get_room():
    # Get the rooms from the database:
    rooms: List[Room] = get_rooms()

    # Convert the rooms to a list of dictionaries for JSON serialization:
    rooms_data: List[dict] = []
    for room in rooms:
        room_data = {
            "roomId": room.room_id,
            "floor": room.floor,
            "beds": room.beds,
            "guestNum": room.guest_num,
            "price": room.price,
        }
        rooms_data.append(room_data)

    return jsonify({"rooms": rooms_data}), 200


@app.route("/booking", methods=["POST"])
def make_booking():
    # Parse the request data as JSON:
    data = request.get_json()

    # Create a new "Booking" object from the request data:
    new_booking = Booking(
        check_in=data["bookingDates"]["checkIn"],
        check_out=data["bookingDates"]["checkOut"],
        first_name=data["firstName"],
        last_name=data["lastName"],
        room_id=data["roomId"],
    )

    if is_room_booked(
        new_booking.room_id,
        new_booking.check_in,
        new_booking.check_out,
    ):
        return f"Room is already booked", 409

    insert_booking(new_booking)
    result_message = (
        f"The room №{data['roomId']} is successfully booked "
        f"for period from {data['bookingDates']['checkIn']} "
        f"to {data['bookingDates']['checkOut']}"
    )
    return result_message, 200


if __name__ == "__main__":
    create_tables()
    app.run(debug=True, port=5000)
