from app import db
from sqlalchemy import func
from app.reviews.models import Review

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    reviews = db.relationship('Review', backref='book', lazy=True)

    @property
    def average_rating(self):
        return db.session.query(func.avg(Review.rating)).filter(Review.book_id == self.id).scalar() or 0
