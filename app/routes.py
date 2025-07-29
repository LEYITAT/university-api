
from flask import Blueprint, request, jsonify
from app.models import Estudiante, Curso, Inscripcion
from app.schemas import EstudianteSchema, CursoSchema, InscripcionSchema
from app.database import db
from sqlalchemy.exc import IntegrityError 
from marshmallow import ValidationError 


university_bp = Blueprint('university', __name__, url_prefix='/api/v1')


estudiante_schema = EstudianteSchema()
estudiantes_schema = EstudianteSchema(many=True)

curso_schema = CursoSchema()
cursos_schema = CursoSchema(many=True)

inscripcion_schema = InscripcionSchema()
inscripciones_schema = InscripcionSchema(many=True)


@university_bp.route('/estudiantes', methods=['POST'])
def create_estudiante():
    if not request.is_json:
        return jsonify({"message": "El cuerpo debe ser JSON"}), 400

    data = request.get_json()

    if not data:
        return jsonify({"message": "El cuerpo no puede estar vacío"}), 400

    try:
        estudiante_data = estudiante_schema.load(request.json)
        db.session.add(estudiante_data)
        db.session.commit()
        
        return jsonify(estudiante_schema.dump(estudiante_data)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400 
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "El email ya existe para otro estudiante."}), 409 
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500

@university_bp.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    all_estudiantes = Estudiante.query.all()
    return jsonify(estudiantes_schema.dump(all_estudiantes)), 200

@university_bp.route('/estudiantes/<int:id>', methods=['GET'])
def get_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id) 
    return jsonify(estudiante_schema.dump(estudiante)), 200

@university_bp.route('/estudiantes/<int:id>', methods=['PUT'])
def update_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id)
    try:
        
        updated_data = estudiante_schema.load(request.json, instance=estudiante, partial=True)
        db.session.commit()
        return jsonify(estudiante_schema.dump(updated_data)), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "El email ya existe para otro estudiante."}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500

@university_bp.route('/estudiantes/<int:id>', methods=['DELETE'])
def delete_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id)
    db.session.delete(estudiante)
    db.session.commit()
    return jsonify({"message": "Estudiante eliminado exitosamente"}), 204 


@university_bp.route('/cursos', methods=['POST'])
def create_curso():
    try:
        curso_data = curso_schema.load(request.json)
        db.session.add(curso_data)
        db.session.commit()
        return jsonify(curso_schema.dump(curso_data)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "El código del curso ya existe."}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500

@university_bp.route('/cursos', methods=['GET'])
def get_cursos():
    all_cursos = Curso.query.all()
    return jsonify(cursos_schema.dump(all_cursos)), 200

@university_bp.route('/cursos/<int:id>', methods=['GET'])
def get_curso(id):
    curso = Curso.query.get_or_404(id)
    return jsonify(curso_schema.dump(curso)), 200

@university_bp.route('/cursos/<int:id>', methods=['PUT'])
def update_curso(id):
    curso = Curso.query.get_or_404(id)
    try:
        updated_data = curso_schema.load(request.json, instance=curso, partial=True)
        db.session.commit()
        return jsonify(curso_schema.dump(updated_data)), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "El código del curso ya existe."}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500

@university_bp.route('/cursos/<int:id>', methods=['DELETE'])
def delete_curso(id):
    curso = Curso.query.get_or_404(id)
    db.session.delete(curso)
    db.session.commit()
    return jsonify({"message": "Curso eliminado exitosamente"}), 204


@university_bp.route('/inscripciones', methods=['POST'])
def create_inscripcion():
    try:
        
        data = inscripcion_schema.load(request.json)

        
        estudiante_existe = Estudiante.query.get(data['id_estudiante'])
        curso_existe = Curso.query.get(data['id_curso'])

        if not estudiante_existe:
            return jsonify({"message": f"Estudiante con ID {data['id_estudiante']} no encontrado."}), 404
        if not curso_existe:
            return jsonify({"message": f"Curso con ID {data['id_curso']} no encontrado."}), 404

        
        inscripcion = Inscripcion(
            id_estudiante=data['id_estudiante'],
            id_curso=data['id_curso'],
            estado=data.get('estado', 'activo') 
        )
        db.session.add(inscripcion)
        db.session.commit()
        
        return jsonify(inscripcion_schema.dump(inscripcion)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500


@university_bp.route('/inscripciones', methods=['GET'])
def get_inscripciones():
    all_inscripciones = Inscripcion.query.all()
    
    return jsonify(inscripciones_schema.dump(all_inscripciones)), 200

@university_bp.route('/inscripciones/<int:id>', methods=['GET'])
def get_inscripcion(id):
    inscripcion = Inscripcion.query.get_or_404(id)
    return jsonify(inscripcion_schema.dump(inscripcion)), 200

@university_bp.route('/inscripciones/<int:id>', methods=['PUT'])
def update_inscripcion(id):
    inscripcion = Inscripcion.query.get_or_404(id)
    try:
        
        updated_data = inscripcion_schema.load(request.json, instance=inscripcion, partial=True)

        
        if 'id_estudiante' in request.json and request.json['id_estudiante'] != inscripcion.id_estudiante:
            return jsonify({"message": "No se permite cambiar el ID del estudiante para una inscripción existente."}), 400
        if 'id_curso' in request.json and request.json['id_curso'] != inscripcion.id_curso:
            return jsonify({"message": "No se permite cambiar el ID del curso para una inscripción existente."}), 400

        db.session.commit()
        return jsonify(inscripcion_schema.dump(updated_data)), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500

@university_bp.route('/inscripciones/<int:id>', methods=['DELETE'])
def delete_inscripcion(id):
    inscripcion = Inscripcion.query.get_or_404(id)
    db.session.delete(inscripcion)
    db.session.commit()
    return jsonify({"message": "Inscripción eliminada exitosamente"}), 204