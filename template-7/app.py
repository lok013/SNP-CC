from flask import Flask, request, jsonify, render_template
from flask import redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('E:/SNP-CC/database/student_info.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/admin')
def admin_page():
    return render_template('admin.html')


    
@app.route('/modify/<roll_number>')
def modify_user_page(roll_number):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM students_info WHERE roll_number = ?', (roll_number,)).fetchone()
    conn.close()
    
    if user:
        return render_template('modify.html', user=user)
    else:
        return 'User not found', 404


@app.route('/api/users/modify/<roll_number>', methods=['POST'])
def modify_user(roll_number):
    roll_number_new = request.form['roll_number']
    name_new = request.form['name']
    secret_pin_new = request.form['secret_pin']

    conn = get_db_connection()
    try:
        conn.execute('UPDATE students_info SET roll_number = ?, name = ?, secret_pin = ? WHERE roll_number = ?', 
                     (roll_number_new, name_new, secret_pin_new, roll_number))
        conn.commit()
        message = 'User modified successfully'
    except Exception as e:
        message = f'Error: {e}'
    finally:
        conn.close()

    return jsonify({'status': message})



@app.route('/api/users/update/<roll_number>', methods=['POST'])
def update_user(roll_number):
    name = request.form['name']
    secret_pin = request.form['secret_pin']
    
    conn = get_db_connection()
    conn.execute('UPDATE students_info SET name = ?, secret_pin = ? WHERE roll_number = ?', (name, secret_pin, roll_number))
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin_page'))  # Ensure 'admin_page' matches the function name



@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM students_info').fetchall()  # Correct table name
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/api/users', methods=['POST'])
def add_user():
    user = request.get_json()
    roll_number = user.get('roll_number')
    name = user.get('name')
    secret_pin = user.get('secret_pin')

    if not roll_number or not name or not secret_pin:
        return jsonify({'status': 'Error: Missing data'}), 400

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO students_info (roll_number, name, secret_pin) VALUES (?, ?, ?)', 
                     (roll_number, name, secret_pin))
        conn.commit()
        message = 'User added successfully'
    except sqlite3.IntegrityError:
        message = 'Error: User with this roll number already exists'
    except Exception as e:
        message = f'Error: {e}'
    finally:
        conn.close()
    
    return jsonify({'status': message})

@app.route('/api/users/<roll_number>', methods=['DELETE'])
def delete_user(roll_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students_info WHERE roll_number = ?', (roll_number,))
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'status': 'Error: User not found'}), 404
    conn.commit()
    conn.close()
    return '', 204

@app.route('/api/users/search/<roll_number>', methods=['GET'])
def search_user(roll_number):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM students_info WHERE roll_number = ?', (roll_number,)).fetchone()
    conn.close()
    
    if user:
        return jsonify(dict(user))
    else:
        return jsonify({})  # Return an empty JSON object if no user is found

if __name__ == '__main__':
    app.run(port=5003, debug=True)  # Port 5003
