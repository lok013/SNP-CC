from flask import Flask, request, jsonify, redirect, url_for, session, render_template
from flask_socketio import SocketIO, join_room, leave_room, send
import sqlite3
import random
import os

app = Flask(__name__)
app.secret_key = '851566fb5eec568f008448cb894a30c940f91d2591801b9b'  # Required for session management
socketio = SocketIO(app)

# Helper function to generate unique room code
def generate_room_code():
    return f'{random.randint(1000, 9999)}'

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('E:/SNP-CC/database/chat_app.db')
    conn.row_factory = sqlite3.Row
    return conn

# Login route to authenticate and store roll_number in session
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        security_pin = request.form['security_pin']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if roll number and pin exist in the database
        cursor.execute("SELECT * FROM students_info WHERE roll_number = ? AND pin = ?", (roll_number, security_pin))
        user = cursor.fetchone()

        if user:
            session['roll_number'] = roll_number  # Store roll_number in session
            return redirect(url_for('choose_chat'))  # Redirect to the choice page
        else:
            return redirect(url_for('http://127.0.0.1:5000/login'))  # Redirect back to the login page on invalid credentials

    return render_template('login.html') # Redirect to the login page for any non-POST requests

# Route to choose between chat applications
@app.route('/choose_chat')
def choose_chat():
    roll_number = session.get('roll_number')
    if not roll_number:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('index.html', roll_number=roll_number)

# API Route to create a room
@app.route('/create_room', methods=['POST'])
def create_room():
    room_code = generate_room_code()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO rooms (room_code) VALUES (?)", (room_code,))
        conn.commit()
        return jsonify({"room_code": room_code}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# API Route to join a room
@app.route('/join_room', methods=['POST'])
def join_room_api():
    data = request.json
    room_code = data.get('room_code')
    roll_number = data.get('roll_number')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT room_id FROM rooms WHERE room_code = ?", (room_code,))
    room = cursor.fetchone()

    if room:
        room_id = room['room_id']
        cursor.execute("INSERT INTO room_members (room_id, user_roll_number) VALUES (?, ?)", (room_id, roll_number))
        conn.commit()
        conn.close()
        return jsonify({"message": "Joined room successfully", "room_code": room_code}), 200
    else:
        conn.close()
        return jsonify({"error": "Room not found"}), 404

# WebSocket event for joining a room
@socketio.on('join')
def handle_join(data):
    room_code = data['room_code']
    roll_number = data['roll_number']
    join_room(room_code)
    send(f'{roll_number} has joined the room.', to=room_code)

# WebSocket event for leaving a room
@socketio.on('leave')
def handle_leave(data):
    room_code = data['room_code']
    roll_number = data['roll_number']
    leave_room(room_code)
    send(f'{roll_number} has left the room.', to=room_code)

# WebSocket event for handling messages
@socketio.on('message')
def handle_message(data):
    room_code = data['room_code']
    roll_number = data['roll_number']
    message = data['message']
    send(f'{roll_number}: {message}', to=room_code)

# Route for group chat
@app.route('/group_chat')
def group_chat():
    roll_number = session.get('roll_number')
    if not roll_number:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('chat_g.html', roll_number=roll_number)

# Route for logout
@app.route('/logout')
def logout():
    session.pop('roll_number', None)  # Clear the session
    return redirect(url_for('login'))  # Correct redirection to login route


if __name__ == '__main__':
    socketio.run(app, port=5002, debug=True)
