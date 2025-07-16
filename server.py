from flask import Flask
from models import db
from flask_cors import CORS
from views.transaction_views import transaction_bp
from views.transaction_group_views import transaction_group_bp
from views.category_views import category_bp
from views.user_views import user_bp
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

DB_URI = os.getenv("DB_URI")
print({DB_URI})


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    # enabling CORS for the app
    CORS(app)

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(transaction_bp, url_prefix="/transactions")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(transaction_group_bp, url_prefix="/transaction_groups")
    app.register_blueprint(category_bp, url_prefix="/categories")

    @app.route("/check_db")
    def check_db():
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT current_database();"))
            db_name = result.fetchone()[0]
            return f"✅ Currently connected to database: {db_name}"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8000)
