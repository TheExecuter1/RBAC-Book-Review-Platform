from app import db
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(20), default='Regular User')  # or 'Administrator'
    password_hash = db.Column(db.String(128))


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
