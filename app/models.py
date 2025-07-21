
from app.database import db
from datetime import datetime

class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    id_estudiante = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)

   
    inscripciones = db.relationship('Inscripcion', backref='estudiante', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Estudiante {self.nombre} {self.apellido}>"

class Curso(db.Model):
    __tablename__ = 'curso'
    id_curso = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    creditos_o_valor = db.Column(db.Numeric(5, 2), nullable=False) 
    departamento = db.Column(db.String(100))

    
    inscripciones = db.relationship('Inscripcion', backref='curso', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Curso {self.nombre}>"

class Inscripcion(db.Model):
    __tablename__ = 'inscripcion'
    id_inscripcion = db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id_estudiante'), nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id_curso'), nullable=False)
    fecha_inscripcion = db.Column(db.TIMESTAMP(timezone=False), default=datetime.utcnow)
    estado = db.Column(db.String(20), default='activo', nullable=False)

    def __repr__(self):
        return f"<Inscripcion EstudianteID:{self.id_estudiante} CursoID:{self.id_curso}>"