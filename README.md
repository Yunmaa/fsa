# Student Management API

## Goal
Build a student management API utilizing Python, Flask-RESTX, SQLite3, and Swagger UI.

## Overview
This Flask-based web app offers a straightforward API for creating and managing students, courses, and grades, as well as assigning students to courses. The API features endpoints for creating, reading, updating, and deleting students and courses, as well as retrieving students registered in particular courses and their respective grades. Additionally, it calculates students' GPAs using a 4.0 scale and secures the API using JWT tokens for authentication and authorization purposes. The app is built using Python and employs Flask and Flask-RESTful libraries for delivering RESTful API endpoints. The app's design allows for easy extension and customization for developers seeking to enhance its existing functionality and develop more sophisticated applications.


## Technologies Used
- [Python](https://www.python.org/)
- [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/)
- [Flask-JWT](https://flask-jwt-extended.readthedocs.io/en/stable/)


# Getting Started
## Installation
## Clone the repository
```
git clone https://github.com/Yunmaa/fsa.git
```

Install dependencies with pip:
```
cd fsa
pip install -r requirements.txt
```

## Setup and Configuration

### `.env` Configuration
Create a .env file containing the following settings:
```

FLASK_DEBUG=<True/False>
FLASK_APP=run.py
SECRET_KEY=<your secret key>
SQLALCHEMY_DATABASE_URI=sqlite:///sms.db
SQLALCHEMY_TRACK_MODIFICATIONS=False
JWT_SECRET_KEY = <JWT secrete key>
ALGORITHM = <hashing algorithm>
ACCESS_TOKEN_EXPIRES_MINUTES = <expiration time of the access and refresh tokens>

```  
Note: The `DATABASE_URL` setting is not required, but it must have a value even if an arbitrary value for your app to run during development and testing. But during production, this must be set to a valid database URL.


# Running the App

## Navigate to the app's root directory
For example: cd fsa

## Create and activate a virtual environment
python3 -m venv venv.
Then execute: 
venv\Scripts\activate.bat (for Windows)
OR source venv/bin/activate (for Linux or macOS)

## Set the Flask app environment variable
#### Windows
```
set FLASK_APP=run.py 
```
#### Mac or Linux
```
export FLASK_APP=run.py
```

## Create database tables
flask db upgrade


## Launch the application
```
flask run
```
This will start the application on port 5000 by default.

## Testing
A total of 7 tests are included. In the terminal, run pytest or pytest -v or python -m pytest tests/.

## Contact
- Mail: iamjuben@gmail.com
- GitHub: https://github.com/Yunmaa

## Acknowledgements
- [AltSchool Africa](https://www.altschoolafrica.com/)
- [Caleb Emelike](https://github.com/CalebEmelike)
