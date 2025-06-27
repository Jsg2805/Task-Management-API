import mysql.connector

def db_creation():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    cursor = conn.cursor()
    
    # Create the database
    cursor.execute("CREATE DATABASE IF NOT EXISTS task_manager")
    cursor.execute("USE task_manager")  # Using consistent database name

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT  PRIMARY KEY,
            uname VARCHAR(100) NOT NULL,
            uemail VARCHAR(100) NOT NULL
        )
    """)
    
    # Create tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INT  PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            due_date DATE,
            priority ENUM('LOW', 'MEDIUM', 'HIGH'),
            status ENUM('TO DO', 'IN PROGRESS', 'DONE') DEFAULT 'TO DO',
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Connected to DB Successfully...")

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="task_manager"
    )

# Create tables when script runs
db_creation()
