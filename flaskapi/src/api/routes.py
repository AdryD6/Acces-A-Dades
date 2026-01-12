from flask import jsonify, request
from src.config import db
from src.models.student import Student

def init_api_routes(app):

    # 1. GET: Obtener todos los estudiantes
    @app.route('/api/students', methods=['GET'])
    def get_students():
        # Buscamos todos en la base de datos
        students = db.session.query(Student).all()
        
        # Convertimos los objetos a una lista de diccionarios (JSON)
        students_list = []
        for s in students:
            students_list.append({
                'id': s.id, 
                'name': s.name, 
                'age': s.age, 
                'spec': s.spec
            })
        return jsonify(students_list)

    # 2. GET (ID): Obtener un estudiante específico
    @app.route('/api/student/<int:student_id>', methods=['GET'])
    def get_student_by_id(student_id):
        student = db.session.query(Student).get(student_id)
        
        if student is None:
            return jsonify({"error": "Not Found"}), 404
        else:
            return jsonify({
                'id': student.id,
                'name': student.name,
                'age': student.age,
                'spec': student.spec
            })

    # 3. POST: Crear un nuevo estudiante
    @app.route('/api/student', methods=['POST'])
    def post_student():
        student_data = request.get_json()
        
        # Creamos el objeto estudiante con los datos recibidos
        new_student = Student(
            name=student_data.get('name'),
            age=student_data.get('age'),
            spec=student_data.get('spec')
        )
        
        # Guardamos en la base de datos
        db.session.add(new_student)
        db.session.commit()
        
        return jsonify({
            'id': new_student.id,
            'name': new_student.name,
            'age': new_student.age,
            'spec': new_student.spec
        }), 201

    # 4. PUT: Actualizar un estudiante
    @app.route('/api/student/<int:student_id>', methods=['PUT'])
    def put_student(student_id):
        student_json = request.get_json()
        student_bd = db.session.query(Student).get(student_id)
        
        if student_bd is None:
            return jsonify({"error": "Not Found"}), 404
        else:
            # Actualizamos solo si nos envían el dato, si no, dejamos el que estaba
            student_bd.name = student_json.get("name", student_bd.name)
            student_bd.age = student_json.get("age", student_bd.age)
            student_bd.spec = student_json.get("spec", student_bd.spec)
            
            db.session.commit()
            
            return jsonify({
                'id': student_bd.id,
                'name': student_bd.name,
                'age': student_bd.age,
                'spec': student_bd.spec
            }), 200

    # 5. DELETE: Borrar un estudiante
    @app.route('/api/student/<int:student_id>', methods=['DELETE'])
    def delete_student(student_id):
        student = db.session.query(Student).get(student_id)
        
        if student is None:
            return "Not Found", 404
        else:
            db.session.delete(student)
            db.session.commit()
            return "", 204