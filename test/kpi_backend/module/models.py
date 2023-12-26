from sqlalchemy import ForeignKeyConstraint, UniqueConstraint, orm, event, Index
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    custom_categories = db.relationship("CategoryModel", backref="creator", lazy="dynamic", cascade="all, delete-orphan")
    
    record = db.relationship("RecordModel", back_populates="user", lazy="dynamic", cascade="all, delete-orphan")
    

class RecordModel(db.Model):
    __tablename__ = "record"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        unique=False,
        nullable=False
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        unique=False,
        nullable=False
    )
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    sum = db.Column(db.Float(precision=2), unique=False, nullable=False)

    user = db.relationship("UserModel", back_populates="record")
    category = db.relationship("CategoryModel", back_populates="record")

    @orm.validates('user_id')
    def validate_user_id(self, key, user_id):
        if user_id is not None and UserModel.query.get(user_id) is None:
            raise ValueError(f"User with this id does not exist")
        return user_id

    @orm.validates('category_id')
    def validate_category_id(self, key, category_id):
        if category_id is not None and CategoryModel.query.get(category_id) is None:
            raise ValueError("Category with this id does not exist")
        return category_id


class CategoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)  # if null -> not custom

    record = db.relationship("RecordModel", back_populates="category", lazy="dynamic", cascade="all, delete-orphan")

    @orm.validates('user_id')
    def validate_user_id(self, key, user_id):
        if user_id is not None and UserModel.query.get(user_id) is None:
            raise ValueError(f"User with id {user_id} does not exist")
        return user_id
    
    __table_args__ = (
        Index('unique_category_per_user', 'name', 'user_id', unique=True),
        Index('unique_category_name_null_user_id', 'name', postgresql_where=(user_id == None), unique=True),
    )



@event.listens_for(UserModel, 'after_delete')
def delete_user_relatives(mapper, connection, target):
    connection.execute(RecordModel.__table__.delete().where(RecordModel.user_id == target.id))
    connection.execute(CategoryModel.__table__.delete().where(CategoryModel.user_id == target.id))

@event.listens_for(CategoryModel, 'after_delete')
def delete_category_records(mapper, connection, target):
    connection.execute(RecordModel.__table__.delete().where(RecordModel.category_id == target.id))

