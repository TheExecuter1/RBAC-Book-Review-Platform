from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask import jsonify
import os
from dotenv import load_dotenv 

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fuz:fuz@localhost/book_review'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret_key')

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    # @app.errorhandler(404)
    # def not_found_error(error):
    #     return jsonify({'message': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'message': 'An internal error occurred'}), 500


    from app.auth.routes import auth_blueprint
    from app.books.routes import books_blueprint
    from app.reviews.routes import reviews_blueprint
    from app.comments.routes import comments_blueprint

    app.register_blueprint(comments_blueprint, url_prefix='/')
    app.register_blueprint(books_blueprint, url_prefix='/')
    app.register_blueprint(reviews_blueprint, url_prefix='/')
    app.register_blueprint(auth_blueprint)

    return app
