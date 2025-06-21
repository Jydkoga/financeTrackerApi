from flask import Flask
from models import db
from flask_cors import CORS
from views.transaction_views import transaction_bp
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv('DATABASE_URL')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    #enabling CORS for the app
    CORS(app)

    db.init_app(app)
    migrate = Migrate(app,db)

    app.register_blueprint(transaction_bp, url_prefix='/transactions')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)