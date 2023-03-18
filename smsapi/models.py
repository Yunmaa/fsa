from .exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    # courses = db.relationship('Course', secondary='student_course', backref='students')
    grades = relationship('Grade', backref='student', lazy=True)


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    # Create a unique constraint to ensure that each student can only have one grade per course
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_student_course'),)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher = db.Column(db.String(100), nullable=False)
    grades = relationship('Grade', backref='course', lazy=True)
    # student_course = db.Table('student_course',
    #                           db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    #                           db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    #                           db.Column('grade', db.Float))
