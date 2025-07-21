
import os

class Config:
 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://tu_usuario:tu_contraseña@localhost:5432/university_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 