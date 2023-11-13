from app import db
from datetime import datetime
from app.books.models import Book
from app.auth.models import User

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)
#     role = db.Column(db.String(20), default='Regular User')  # or 'Administrator'


