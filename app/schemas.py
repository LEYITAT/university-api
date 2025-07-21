
from marshmallow import Schema, fields, validate  
from marshmallow  import SQLAlchemyAutoSchema 
from app.database import db 
from app.models import Estudiante, Curso, Inscripcion 
from datetime import datetime

class EstudianteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Estudiante
        load_instance = True  
        sqla_session = db.session 

    nombre = fields.String(required=True, validate=validate.Length(min=2, max=100))
    apellido = fields.String(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    fecha_nacimiento = fields.Date(required=True, format='%Y-%m-%d') 


class CursoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Curso
        load_instance = True
        sqla_session = db.session

    nombre = fields.String(required=True, validate=validate.Length(min=3, max=255))
    codigo = fields.String(required=True, validate=validate.Length(min=3, max=50))
    
    creditos_o_valor = fields.Decimal(required=True, as_string=True)
    departamento = fields.String(validate=validate.Length(max=100), allow_none=True)


class InscripcionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inscripcion
        load_instance = True
        sqla_session = db.session

    id_estudiante = fields.Integer(required=True)
    id_curso = fields.Integer(required=True)
    fecha_inscripcion = fields.DateTime(dump_default=datetime.utcnow, format='iso') 
    estado = fields.String(
        required=True,
        validate=validate.OneOf(["activo", "retirado", "reprobado", "aprobado"]),
        dump_default='activo'
    )

    
    estudiante = fields.Nested(EstudianteSchema, dump_only=True, exclude=('inscripciones',)) 
    curso = fields.Nested(CursoSchema, dump_only=True, exclude=('inscripciones',)) 