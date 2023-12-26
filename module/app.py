#import views
from flask import Flask
from flask_migrate import Migrate
from .models import db
from .models import UserModel, CategoryModel, RecordModel
from .init_data import users, categories, records
from .views import views_blueprint
from datetime import datetime


app = Flask(__name__)
app.app_context().push()

app.config.from_pyfile('config.py', silent=True)
app.register_blueprint(views_blueprint)

db.init_app(app)
migrate = Migrate(app, db)

db.create_all()

def initialize_users():
    tables = [UserModel, CategoryModel, RecordModel]
    
    if all(not table.query.first() for table in tables):
        for user_data in users:
            user = UserModel(**user_data)
            db.session.add(user)
        
        for category_data in categories.values():
            category = CategoryModel(**category_data)
            db.session.add(category)
        
        for record_data in records.values():
            record_data["created_at"] = datetime.strptime(record_data["created_at"], "%Y-%m-%dT%H:%M:%S")
            record = RecordModel(**record_data)
            db.session.add(record)
        
        db.session.commit()
        print("Data added to the database.")
    else:
        print("Database is not empty, data was not added.")

initialize_users()