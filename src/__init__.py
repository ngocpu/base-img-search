from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config.config import config

db = SQLAlchemy()
migrate = Migrate()


def init_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)

    from src.routes.fish_route import fish_bp
    app.register_blueprint(fish_bp)
    with app.app_context():
        try:
            db.engine.connect()
            print("✅ Connected to the database successfully!")
        except Exception as e:
            print(f"❌ Failed to connect to the database: {e}")

    return app