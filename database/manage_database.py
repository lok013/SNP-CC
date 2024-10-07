import sqlite3

# Step 1: Create a connection to the SQLite database
def create_connection():
    try:
        conn = sqlite3.connect('chat_app.db')
        # Enable foreign key constraints to ensure data integrity
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# Step 2: Create tables only if they don't exist
def create_tables():
    conn = create_connection()
    if conn is None:
        print("Failed to create database connection.")
        return

    try:
        cursor = conn.cursor()

        # Check if 'rooms' table exists
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_code VARCHAR(4) UNIQUE NOT NULL
        )
        ''')

        # Check if 'room_members' table exists
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS room_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER,
            user_roll_number VARCHAR(10),
            FOREIGN KEY (room_id) REFERENCES rooms (room_id) ON DELETE CASCADE
        )
        ''')

        # Check if 'room_messages' table exists
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS room_messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER,
            user_roll_number VARCHAR(10),
            message_content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES rooms (room_id) ON DELETE CASCADE
        )
        ''')

        # Commit changes to the database
        conn.commit()
        print("Tables created or verified successfully!")

    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
    finally:
        if conn:
            conn.close()

# Step 3: Test the database setup
if __name__ == '__main__':
    create_tables()
