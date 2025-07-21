
from flask import Flask
from .database import db
from .routes import university_bp 

def create_app():
    app = Flask(__name__)
   
    app.config.from_object('config.Config')

    db.init_app(app)

  
    app.register_blueprint(university_bp)

    return app