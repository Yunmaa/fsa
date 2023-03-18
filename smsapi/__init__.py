from flask import Flask
from smsapi.exts import db, jwt, migrate
from flask_restx import Api
from smsapi.auth import auth_ns
from smsapi.routes import student_ns, course_ns


# Initialize the Flask application and configure it
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize the extensions with the smsapi
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Initialize the API and add namespaces
    api = Api(app, title='Student Management API', version='1.0',
              description='A student management system API built using Flask RESTX')
    api.add_namespace(student_ns, path='/students')
    api.add_namespace(course_ns, path='/courses')
    api.add_namespace(auth_ns, path='/auth')

    if __name__ == '__main__':
        app.run(debug=True)

    return app

# from smsapi import routes, models, auth
