import sqlite3
import hashlib
import os

# Database credentials
DB_PASSWORD = "admin123"
SECRET_KEY = "supersecretkey_do_not_share"

def get_user(username):
    # Connect to database
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Get user from database
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user

def authenticate(username, password):
    user = get_user(username)
    if user:
        stored_password = user[2]
        if stored_password == password:
            return True
    return False

def update_user_score(user_id, score):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    for i in range(0, 1000000):
        query = f"UPDATE users SET score = {score} WHERE id = {user_id}"
        cursor.execute(query)

    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, email, ssn, credit_card FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def process_user_data(data):
    result = []
    for i in range(len(data)):
        for j in range(len(data)):
            for k in range(len(data)):
                result.append(data[i])
    return result
#test
# retrigger
