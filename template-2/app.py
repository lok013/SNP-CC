from flask import Flask, render_template, request, session, redirect, url_for, make_response  # Added make_response
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Flask application configuration
app.config['SECRET_KEY'] = '851566fb5eec568f008448cb894a30c940f91d2591801b9b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/SNP-CC/database/student_info.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

 
# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    __tablename__ = 'students_info'
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    secret_pin = db.Column(db.String(50), nullable=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        roll_number = request.form.get('roll_number')
        secret_pin = request.form.get('secret_pin')

        student = Student.query.filter_by(roll_number=roll_number, secret_pin=secret_pin).first()

        if student:
            session['roll_number'] = roll_number
            print(f"Session set for user: {roll_number}")  # Debug statement
            return redirect(url_for('choose_chat'))  # Redirect to the choose_chat route
        else:
            return render_template('login.html', error="Invalid roll number or secret pin")

    return render_template('login.html')

@app.route('/choose_chat')
def choose_chat():
    roll_number = session.get('roll_number')
    response = make_response(render_template('index.html', roll_number=roll_number))  # Create a response object
    response.headers['Content-Security-Policy'] = "default-src 'self';"  # Set CSP header
    response.headers['X-Content-Type-Options'] = 'nosniff'  # Add security headers
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response  # Return the response object

if __name__ == '__main__':
    app.run(debug=True, port=5000)



#  from flask import Flask, render_template, request, session, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # Flask application configuration
# app.config['SECRET_KEY'] = '851566fb5eec568f008448cb894a30c940f91d2591801b9b'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/SNP-CC/database/student_info.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize SQLAlchemy
# db = SQLAlchemy(app)

# # Student Model
# class Student(db.Model):
#     __tablename__ = 'students_info'
#     id = db.Column(db.Integer, primary_key=True)
#     roll_number = db.Column(db.String(50), unique=True, nullable=False)
#     secret_pin = db.Column(db.String(50), nullable=False)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         roll_number = request.form.get('roll_number')
#         secret_pin = request.form.get('secret_pin')

#         student = Student.query.filter_by(roll_number=roll_number, secret_pin=secret_pin).first()

#         if student:
#             session['roll_number'] = roll_number
#             print(f"Session set for user: {roll_number}")  # Debug statement
#             return redirect(url_for('choose_chat'))  # Redirect to the choose_chat route
#         else:
#             return render_template('login.html', error="Invalid roll number or secret pin")

#     return render_template('login.html')

# @app.route('/choose_chat')
# def choose_chat():
#     roll_number = session.get('roll_number')
#     if roll_number:
#         return render_template('index.html', roll_number=roll_number)  # Render the choose_chat page
#     else:
#         return redirect(url_for('login'))  # Redirect to login if not logged in

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)



# from flask import Flask, render_template, request, session, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from flask_session import Session

# app = Flask(__name__)

# # Flask application configuration
# app.config['SECRET_KEY'] = '851566fb5eec568f008448cb894a30c940f91d2591801b9b'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/SNP-CC/database/student_info.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize SQLAlchemy for student_info.db
# db = SQLAlchemy(app)

# # Configure Flask-Session to use SQLAlchemy and sessions.db
# app.config['SESSION_TYPE'] = 'sqlalchemy'
# app.config['SESSION_SQLALCHEMY'] = db
# app.config['SESSION_SQLALCHEMY_BINDS'] = {
#     'sessions': 'sqlite:///E:/SNP-CC/database/sessions.db'
# }
# app.config['SESSION_PERMANENT'] = False
# app.config['SESSION_USE_SIGNER'] = True
# app.config['SESSION_KEY_PREFIX'] = 'app_'

# # Initialize Flask-Session
# Session(app)

# # Student Model
# class Student(db.Model):
#     __tablename__ = 'students_info'
#     id = db.Column(db.Integer, primary_key=True)
#     roll_number = db.Column(db.String(50), unique=True, nullable=False)
#     secret_pin = db.Column(db.String(50), nullable=False)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         roll_number = request.form.get('roll_number')
#         secret_pin = request.form.get('secret_pin')

#         student = Student.query.filter_by(roll_number=roll_number, secret_pin=secret_pin).first()

#         if student:
#             session['roll_number'] = roll_number
#             print(f"Session set for user: {roll_number}")  # Debug statement
#             return redirect(url_for('chat'))
#         else:
#             return render_template('login.html', error="Invalid roll number or secret pin")

#     return render_template('login.html')

# @app.route('/chat')
# def chat():
#     roll_number = session.get('roll_number')
#     if roll_number:
#         return redirect('http://127.0.0.1:5001/chat')  # Redirect to chat app
#     else:
#         return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
