from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import os
import sqlite3

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = '2bfa9d3c8a96e7e0c5bbce32b3b3d8f705a89fa15d8b6a1b5e8ecff3d2a3c4f8'
jwt = JWTManager(app)

users = {"user": "password"}  # Простой словарь для хранения пользователей

def init_main_db():
    if not os.path.exists('cabinets.db'):
        conn = sqlite3.connect('cabinets.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cabinets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        conn.commit()
        conn.close()

def init_cabinet_db(cabinet_name):
    db_name = f'cabs/{cabinet_name}.db'
    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS computers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                type TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username in users and users[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(msg="This is a protected route")

@app.route('/getCabinets', methods=['GET'])
def getCabinets():
    conn = sqlite3.connect('cabinets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cabinets")
    cabinets = cursor.fetchall()
    conn.close()
    response = jsonify([{"id": c[0], 
                         "name": c[1]}
    for c in cabinets])
    print(response)
    return response

@app.route('/add_cabinet', methods=['POST'])
def add_cabinet():
    data = request.get_json()
    cabinet_name = data.get('name')

    conn = sqlite3.connect('cabinets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM cabinets WHERE name = ?", (cabinet_name,))
    if cursor.fetchone():
        return jsonify({"error": "Cabinet with this name already exists"}), 400

    cursor.execute("INSERT INTO cabinets (name) VALUES (?)", (cabinet_name,))
    conn.commit()
    conn.close()

    init_cabinet_db(cabinet_name)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5001)
