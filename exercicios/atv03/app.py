from flask import Flask
import pymysql
import os
from models import db  # <-- Importa o db daqui

def create_app():
    app = Flask(__name__, template_folder="views")
    app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')

    # Database configuration - default values (change via env vars if needed)
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASS = os.environ.get('DB_PASS', '')  # empty by default (your case)
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'animes_db')

    # SQLAlchemy connection string using pymysql driver
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Attempt to create the database if it does not exist (requires correct MySQL user privileges)
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, charset='utf8mb4')
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.close()
    except Exception as e:
        # If creation fails, continue; dev should ensure the DB exists or that credentials are correct.
        print('Warning: could not create database automatically. Make sure MySQL is running and credentials are correct.', e)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Import models so SQLAlchemy knows about them, then create tables
    with app.app_context():
        # import models to register with SQLAlchemy metadata
        from models import anime_model, user_model  # noqa: F401
        db.create_all()

    # Register routes (controllers)
    from controllers.routes import init_app
    init_app(app)

    return app

# Create the app instance used by the run block
app = create_app()

if __name__ == "__main__":
    # Run exactly on port 4000 and accessible on the network per assignment
    app.run(host='0.0.0.0', port=4000, debug=True)
