from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DB_PATH = '../database/student_info.db'

@app.route('/exists', methods=['GET', 'POST'])
def exists():
    if request.method == 'POST':
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        roll_number = request.form['roll_number']

        # Ensure roll_number is passed correctly
        query = "SELECT roll_number FROM students_info WHERE roll_number=?"
        cursor.execute(query, (roll_number,))  # Note the tuple with trailing comma

        result = cursor.fetchall()
        connection.close()

        if result:
            return render_template('exists.html', message="Well, look at that! Your roll number made the cut—just like your epic last-minute study sessions!")
        else:
            return render_template('exists.html', message="Oops! It seems like your roll number is playing hide and seek with our database. Unfortunately, it’s still hiding!")

    return render_template('exists.html')

if __name__ == '__main__':
    app.run(debug=True,port=5004)
