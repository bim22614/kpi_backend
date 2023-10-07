from . import app
from flask import jsonify, request
import datetime
import json

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
  date = datetime.datetime.now()
  status = "OK"

  return jsonify({
    "date": date,
    "status": status
  })

users = {
    1: {"id": 1, "name": "John Doe"},
    2: {"id": 2, "name": "Oliver Jr"},
}
categories = {
    1: {"id": 1, "name": "Food"},
    2: {"id": 2, "name": "Transport"},
    3: {"id": 3, "name": "Housing"},
}
records = {
    1: {
        "id": 1,
        "user_id": 1,
        "category_id": 1,
        "date": "2023-07-20T12:00:00",
        "amount": 100,
    },
    2: {
        "id": 2,
        "user_id": 2,
        "category_id": 2,
        "date": "2023-07-21T13:00:00",
        "amount": 200,
    },
}


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    if user_id not in users:
        return jsonify({"error": "No such user id"}), 404
    return jsonify(users[user_id])


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "No such user with this id"}), 404
    del users[user_id]
    return jsonify({"message": "user was deleted"}), 200


@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    user = {"id": len(users) + 1, "name": data["name"]}
    users.update({user["id"]: user})
    return jsonify(user), 201


@app.route("/category", methods=["GET"])
def get_categories():
    return jsonify(categories)


@app.route("/category/<int:category_id>", methods=["GET"])
def get_category(category_id):
    if category_id not in categories:
        return jsonify({"error": "No such category id"}), 404
    return jsonify(categories[category_id])


@app.route("/category", methods=["POST"])
def create_category():
    data = request.get_json()
    category = {"id": len(categories) + 1, "name": data["name"]}
    categories.update({category["id"]: category})
    return jsonify(category), 201


@app.route("/category/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    if category_id not in categories:
        return jsonify({"error": "No such category with this id"}), 404
    del categories[category_id]
    return jsonify({"message": "category was deleted"}), 200


@app.route("/record", methods=["GET"])
def get_records():
    return jsonify(records)


@app.route("/record/<int:record_id>", methods=["GET"])
def get_record(record_id):
    if record_id not in records:
        return jsonify({"error": "No such id"}), 404
    return jsonify(records[record_id])


@app.route("/record", methods=["POST"])
def create_record():
    data = request.get_json()
    record = {
        "id": len(records) + 1,
        "user_id": data["user_id"],
        "category_id": data["category_id"],
        "date": data["date"],
        "amount": data["amount"],
    }
    records.update({record["id"]: record})
    return jsonify(record), 201


@app.route("/record/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    if record_id not in records:
        return jsonify({"error": "No such record with this id"}), 404
    del records[record_id]
    return jsonify({"message": "record was deleted"}), 200