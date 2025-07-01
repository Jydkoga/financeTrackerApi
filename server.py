from flask import Flask
from models import db
from flask_cors import CORS
from views.transaction_views import transaction_bp
from views.transaction_group_views import transaction_group_bp
from views.user_views import user_bp
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv('DB_URI')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    #enabling CORS for the app
    CORS(app)

    db.init_app(app)
    migrate = Migrate(app,db)

    app.register_blueprint(transaction_bp, url_prefix='/transactions')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(transaction_group_bp, url_prefix='/transaction_groups')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8000)