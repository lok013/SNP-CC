from flask import Flask, render_template, request, jsonify, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Flask application configuration
app.config['SECRET_KEY'] = '851566fb5eec568f008448cb894a30c940f91d2591801b9b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/SNP-CC/database/messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

class Message(db.Model):
    __tablename__ = 'messages'  # Explicitly set the table name to match the existing table

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False)
    recipient = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

@app.route('/chat')
def chat():
    roll_number = session.get('roll_number')
    if roll_number:
        return render_template('chat.html', roll_number=roll_number)
    else:
        return redirect('http://127.0.0.1:5000/login')



@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    recipient = data.get('recipient')
    message = data.get('message')
    sender = session.get('roll_number')

    if sender and recipient and message:
        if sender == recipient:
            return jsonify({'status': 'error', 'message': 'Cannot send a message to yourself'})
        
        print(f"Sending message from {sender} to {recipient}: {message}")  # Debug print
        new_message = Message(sender=sender, recipient=recipient, message=message)
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        print(f"Error: sender={sender}, recipient={recipient}, message={message}")  # Debug print
        return jsonify({'status': 'error', 'message': 'Invalid input'})


@app.route('/get_messages')
def get_messages():
    recipient = request.args.get('recipient')
    sender = session.get('roll_number')

    print(f"Fetching messages for sender: {sender}, recipient: {recipient}")

    if sender and recipient:
        messages = Message.query.filter(
            ((Message.sender == sender) & (Message.recipient == recipient)) |
            ((Message.sender == recipient) & (Message.recipient == sender))
        ).order_by(Message.timestamp).all()

        print(f"Messages retrieved: {messages}")

        return jsonify([{
            'sender': msg.sender,
            'message': msg.message,
            'timestamp': msg.timestamp.strftime('%H:%M')
        } for msg in messages])
    else:
        print("No sender or recipient provided")
        return jsonify([])


@app.route('/logout')
def logout():
    session.pop('roll_number', None)
    return redirect('http://127.0.0.1:5000/login')  # Adjusted to redirect to the correct login URL

if __name__ == '__main__':
    app.run(debug=True, port=5001)

