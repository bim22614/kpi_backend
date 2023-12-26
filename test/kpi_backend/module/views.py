from flask import jsonify, request
from flask import Blueprint
from marshmallow import ValidationError
from .init_data import users, categories, records
from .schemas import UserSchema, RecordSchema, CategorySchema
from .models import db
from .models import UserModel, CategoryModel, RecordModel
import datetime
import json
import os


views_blueprint = Blueprint('views', __name__)

@views_blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400


@views_blueprint.route('/healthcheck', methods=['GET'])
def healthcheck():
  date = datetime.datetime.now()
  status = "OK"

  return jsonify({
    "date": date,
    "status": status
  })


@views_blueprint.route("/users", methods=["GET"])
def get_users():
    users = UserModel.query.all()
    serializer = UserSchema(many=True)
    return {"users": serializer.dump(users)}


@views_blueprint.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = UserModel.query.get(user_id)
    if user is None:
        return jsonify({"message": f"No user with id {user_id} found"}), 404

    serializer = UserSchema()
    return {"user": serializer.dump(user)}


@views_blueprint.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = UserModel.query.get(user_id)
    if user is None:
        return jsonify({f"message": "No user with id {user_id} found"}), 404

    db.session.delete(user)
    db.session.commit()

    return {"msg": "User deleted"}


@views_blueprint.route("/user", methods=["POST"])
def create_user():
    serializer = UserSchema()
    validated_data = serializer.load(request.json)

    user = UserModel(**validated_data)
    db.session.add(user)
    db.session.commit()

    return {"msg": "User created", "user": serializer.dump(user)}


@views_blueprint.route("/category", methods=["GET"])
def get_categories():
    categories = CategoryModel.query.filter(CategoryModel.user_id == None).all()
    serializer = CategorySchema(many=True)
    return {"categories": serializer.dump(categories)}


@views_blueprint.route("/category/<int:category_id>", methods=["GET"])
def get_category(category_id):
    category = CategoryModel.query.filter(CategoryModel.user_id == None, CategoryModel.id == category_id).first()
    if category is None:
        return jsonify({"message": f"No category with id {category_id} found"}), 404
    
    serializer = CategorySchema()
    return {"category": serializer.dump(category)}


@views_blueprint.route("/category", methods=["POST"])
def create_category():
    serializer = CategorySchema()
    validated_data = serializer.load(request.json)

    category = CategoryModel(**validated_data)
    db.session.add(category)
    db.session.commit()

    return {"msg": "Category created", "category": serializer.dump(category)}


@views_blueprint.route("/category/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    category = CategoryModel.query.filter(CategoryModel.user_id == None, CategoryModel.id == category_id).first()
    if category is None:
        return jsonify({"message": f"No category with id {category_id} found"}), 404

    db.session.delete(category)
    db.session.commit()

    return {"msg": "Category deleted"}


@views_blueprint.route("/user/<int:user_id>/category", methods=["GET"])
def get_user_categories(user_id):
    user = UserModel.query.get(user_id)
    if user is None:
        return {"error": "User not found"}, 404

    user_categories = CategoryModel.query.filter(CategoryModel.user_id == user_id).all()
    serializer = CategorySchema(many=True)
    return {"user_categories": serializer.dump(user_categories)}


@views_blueprint.route("/user/<int:user_id>/category/<int:category_id>", methods=["GET"])
def get_user_category(user_id, category_id):
    user_category = CategoryModel.query.filter(CategoryModel.user_id == user_id, CategoryModel.id == category_id).first()
    if user_category is None:
        return jsonify({"message": f"No category with id {category_id} found"}), 404
    
    serializer = CategorySchema()
    return {"user_category": serializer.dump(user_category)}


@views_blueprint.route("/user/<int:user_id>/category", methods=["POST"])
def create_user_category(user_id):
    data = request.json
    data["user_id"] = user_id

    serializer = CategorySchema()
    validated_data = serializer.load(data)
    
    user_category = CategoryModel(**validated_data)
    db.session.add(user_category)
    db.session.commit()

    return {"msg": "User category created", "user_category": serializer.dump(user_category)}


@views_blueprint.route("/user/<int:user_id>/category/<int:category_id>", methods=["DELETE"])
def delete_user_category(user_id, category_id):
    user_category = CategoryModel.query.filter(CategoryModel.user_id == user_id, CategoryModel.id == category_id).first()
    if user_category is None:
        return jsonify({"message": f"No category with id {category_id} found"}), 404

    db.session.delete(user_category)
    db.session.commit()

    return {"msg": "User category deleted"}


@views_blueprint.route("/record", methods=["GET"])
def get_records():
    records = (
        RecordModel.query
        .join(CategoryModel, RecordModel.category_id == CategoryModel.id)
        .filter(CategoryModel.user_id == None)  # Фільтр на категорії з user_id, що дорівнює None
        .all()
    )
    serializer = RecordSchema(many=True)
    return {"records": serializer.dump(records)}


@views_blueprint.route("/user/<int:user_id>/record", methods=["GET"])
def get_user_records(user_id):
    records = (
        RecordModel.query
        .join(CategoryModel, RecordModel.category_id == CategoryModel.id)
        .filter(CategoryModel.user_id == user_id)  # Фільтр на категорії з user_id, що дорівнює None
        .all()
    )
    serializer = RecordSchema(many=True)
    return {"records": serializer.dump(records)}


@views_blueprint.route("/record/<int:record_id>", methods=["GET"])
def get_record(record_id):
    record = (
        RecordModel.query
        .join(CategoryModel, RecordModel.category_id == CategoryModel.id)
        .filter(RecordModel.id == record_id)
        .filter(CategoryModel.user_id == None)
        .first()
    )
    if record is None:
        return jsonify({"message": f"No recotd with such parameters found"}), 404
    serializer = RecordSchema()
    return {"record": serializer.dump(record)}


@views_blueprint.route("/user/<int:user_id>/record/<int:record_id>", methods=["GET"])
def get_user_record(user_id, record_id):
    record = (
        RecordModel.query
        .join(CategoryModel, RecordModel.category_id == CategoryModel.id)
        .filter(RecordModel.id == record_id)
        .filter(CategoryModel.user_id == user_id)
        .first()
    )
    if record is None:
        return jsonify({"message": f"No record with such parameters found"}), 404
    
    serializer = RecordSchema()
    return {"records": serializer.dump(record)}


@views_blueprint.route("/record", methods=["POST"])
def create_record():
    serializer = RecordSchema()
    validated_data = serializer.load(request.json)

    user = UserModel.query.filter(UserModel.id == validated_data["user_id"]).first()
    if not user:
        return {"error": "No user with such id"}, 404

    category = CategoryModel.query.filter(CategoryModel.id == validated_data["category_id"]).first()
    if category:
        if category.user_id:
            if category.user_id != validated_data["user_id"]:
                return {"error": "You cant create record with category of an other user"}, 404
    else:
        return {"error": "No category with such id"}, 404


    record = RecordModel(**validated_data)
    db.session.add(record)
    db.session.commit()

    return {"msg": "Record created", "record": serializer.dump(record)}


@views_blueprint.route("/record/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    record = (
        RecordModel.query
        .join(CategoryModel, RecordModel.category_id == CategoryModel.id)
        .filter(RecordModel.id == record_id)
        .filter(CategoryModel.user_id == None)
        .first()
    )

    if not record:
        return {"error": "There is not a record with such parameters"}, 404

    db.session.delete(record)
    db.session.commit()

    return {"msg": "Record deleted"}


@views_blueprint.route("/user/<int:user_id>/record/<int:record_id>", methods=["DELETE"])
def delete_user_record(user_id, record_id):
    record = (
        RecordModel.query
        .join(CategoryModel, RecordModel.category_id == CategoryModel.id)
        .filter(RecordModel.id == record_id)
        .filter(CategoryModel.user_id == user_id)
        .first()
    )

    if not record:
        return {"error": "There is not a record with such parameters"}, 404

    db.session.delete(record)
    db.session.commit()

    return {"msg": "Record deleted"}