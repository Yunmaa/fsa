from flask import request
from flask_restx import Api, Resource, Namespace, fields
from smsapi import db
from smsapi.models import Student, Course, Grade
from flask_jwt_extended import jwt_required
from .utils import calculate_gpa
from .schemas import StudentSchema, CourseSchema, GradeSchema


# Initialize namespaces
student_ns = Namespace('Students', description='Student Operations')
course_ns = Namespace('Courses', description='Course Operations')
# grade_ns = Namespace('Grades', description='Grade Operations')


# Create the student model
student_model = student_ns.model('Student', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'email': fields.String(required=True),
    # 'grades': fields.List(fields.Nested(grade_ns.model('Grade', {
    #     'id': fields.Integer(readonly=True),
    #     'course_id': fields.Integer(required=True),
    #     'grade': fields.Float(required=True),
    # })))
})

# Create the course model
course_model = course_ns.model('Course', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'teacher': fields.String(required=True),
    'students': fields.List(fields.Nested(student_model))
    # 'grades': fields.List(fields.Nested(grade_ns.model('Grade', {
    #     'id': fields.Integer(readonly=True),
    #     'student_id': fields.Integer(required=True),
    #     'grade': fields.Float(required=True),
    # })))
})

# Create the grade model
grade_model = student_ns.model('Grade', {
    'student_id': fields.Integer(required=True),
    'course_id': fields.Integer(required=True),
    'grade': fields.Float(required=True)
})

# gpa_model = student_ns.model('StudentGPA', {
#     'gpa': fields.Float(readOnly=True, description='The student GPA')
# })

# Initialize schemas
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
grade_schema = GradeSchema()
grades_schema = GradeSchema(many=True)


@student_ns.route('')
class StudentListResource(Resource):
    @jwt_required()
    @student_ns.doc('get_students')
    @student_ns.marshal_with(student_model, envelope='students')
    def get(self):
        students = Student.query.all()
        return students_schema.dump(students), 200

    @jwt_required()
    @student_ns.doc('create_student', expect=student_model)
    @student_ns.expect(student_model)
    @student_ns.marshal_with(student_model, code=201)
    def post(self):
        data = request.get_json()

        if not data:
            return {"message": "No input data provided"}, 400

        student_data, errors = student_schema.load(data)
        print("Student data:", student_data)
        print("Errors:", errors)

        if errors:
            return errors, 422

        student = Student(**student_data)
        db.session.add(student)
        db.session.commit()

        return student_schema.dump(student), 201


# Student resource
@student_ns.route('/<int:student_id>')
class StudentResourceID(Resource):
    @jwt_required()
    @student_ns.doc('get_student', params={'student_id': 'Student ID'})
    @student_ns.marshal_with(student_model)
    def get(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404
        return students_schema.dump(student), 200

    @jwt_required()
    @student_ns.doc('update_student', params={'student_id': 'Student ID'}, expect=student_model)
    @student_ns.expect(student_model)
    @student_ns.marshal_with(student_model)
    def put(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404

        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400

        student_data, errors = student_schema.load(data, partial=True)
        if errors:
            return errors, 422

        for key, value in student_data.items():
            setattr(student, key, value)

        db.session.commit()

        return student_schema.dump(student), 200

    @jwt_required()
    @student_ns.doc('delete_student', params={'student_id': 'Student ID'})
    @student_ns.response(204, 'Student deleted')
    def delete(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404

        db.session.delete(student)
        db.session.commit()

        return {"message": "Student deleted"}, 200


# Course resource
# Retrieving all students, all courses, and students registered in a particular course
@course_ns.route('/')
class CourseResource(Resource):
    @jwt_required()
    @course_ns.doc('get_courses')
    @course_ns.marshal_with(course_model, envelope='courses')
    def get(self):
        courses = Course.query.all()
        return courses_schema.dump(courses), 200

    @jwt_required()
    @course_ns.doc('create_course', expect=course_model)
    @course_ns.expect(course_model)
    @course_ns.marshal_with(course_model, code=201)
    def post(self):
        data = request.get_json()
        errors = course_schema.validate(data)
        if errors:
            return errors, 400
        course = Course(**data)
        db.session.add(course)
        db.session.commit()
        return course_schema.dump(course), 201


# Course registration functionality
@course_ns.route('/<int:course_id>/register/<int:student_id>')
class CourseRegistrationResource(Resource):
    @jwt_required()
    @course_ns.doc('get_course', params={'course_id': 'ID of the course to register for'})
    @course_ns.marshal_with(course_model)
    def post(self, course_id, student_id):
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 404

        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404

        grade = Grade(student_id=student_id, course_id=course_id, grade=0)
        db.session.add(grade)
        db.session.commit()

        return {"message": "Student registered for the course"}, 200


# Endpoints for retrieving all students, all courses, and students registered in a particular course
@course_ns.route('')
class CourseListResource(Resource):
    @jwt_required()
    @course_ns.doc('get_courses')
    def get(self):
        courses = Course.query.all()
        return courses_schema.dump(courses), 200


@course_ns.route('/<int:course_id>')
class CourseResourceID(Resource):
    @jwt_required()
    @course_ns.doc('get_course', params={'course_id': 'Course ID'})
    @course_ns.marshal_with(course_model)
    def get(self, course_id):
        course = Course.query.get_or_404(course_id)
        return course

    @jwt_required()
    @course_ns.doc('update_course', params={'course_id': 'Course ID'}, expect=course_model)
    @course_ns.expect(course_model)
    @course_ns.marshal_with(course_model)
    def put(self, course_id):
        course = Course.query.get_or_404(course_id)
        data = request.get_json()
        course.name = data['name']
        course.course_id = data['course_id']
        course.teacher_id = data['teacher_id']
        db.session.commit()
        return course

    @jwt_required()
    @course_ns.doc('delete_course', params={'course_id': 'Course ID'})
    @course_ns.response(204, 'Course deleted')
    def delete(self, course_id):
        course = Course.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        return '', 204


# Student grades resource
@student_ns.route('/<int:student_id>/grades')
class StudentGradesResource(Resource):
    @jwt_required()
    @student_ns.doc('get_student_gpa', params={'student_id': 'Student ID'})
    def get(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404

        # Get the student's numerical grades from the Grade model
        grades = [grade.grade for grade in student.grades]

        # Calculate the student's GPA
        gpa = calculate_gpa(grades)

        # Return the calculated GPA along with the student's grades
        return {
                   "grades": grades_schema.dump(student.grades),
                   "gpa": gpa,
               }, 200


# Students registered in a course resource
@course_ns.route('/<int:course_id>/students')
class CourseStudentsResource(Resource):
    @jwt_required()
    @course_ns.doc('get_students', params={'course_id': 'Course ID'})
    @course_ns.marshal_with(student_model)
    def get(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 404

        grades = Grade.query.filter_by(course_id=course_id).all()
        student_ids = [grade.student_id for grade in course.grades]
        students = Student.query.filter(Student.id.in_(student_ids)).all()

        return students_schema.dump(students), 200


@course_ns.route('/<int:course_id>/grades')
class CourseGradesResource(Resource):
    @jwt_required()
    @course_ns.doc('get_course_grades', params={'course_id': 'Course ID'})
    @course_ns.marshal_with(grade_model)
    def get(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 404
        grades = Grade.query.filter_by(course_id=course_id).all()
        grades_data = grades_schema.dump(grades)

        for grade_data in grades_data:
            student = Student.query.get(grade_data['student_id'])
            grade_data['student_name'] = student.name
            grade_data['student_email'] = student.email
        return grades_data, 200


@student_ns.route('/<int:student_id>/gpa')
class StudentGPAResource(Resource):
    @jwt_required()
    @student_ns.doc('get_student_gpa', params={'student_id': 'Student ID'})
    def get(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404

        grades = Grade.query.filter_by(student_id=student_id).all()
        gpa = calculate_gpa(grades)

        return {"gpa": gpa}, 200


# api.add_namespace(student_ns, path='/students')
# api.add_namespace(course_ns, path='/courses')
# api.add_namespace(grade_ns, path='/grades')
