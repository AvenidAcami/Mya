import os
import sqlite3
from flask import Flask, request, jsonify, render_template, redirect, abort

app = Flask(__name__)

# Функция для инициализации базы данных кабинетов
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

# Создаем базу данных для компьютеров каждого кабинета
def init_cabinet_db(cabinet_name):
    db_name = f'cabinets/{cabinet_name}.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS computers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# Создаем базу данных для характеристик компьютера
def init_computer_db(cabinet_name, computer_name):
    db_name = f'cabinets/{cabinet_name}_{computer_name}.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characteristics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Получить список кабинетов
@app.route('/get_cabinets', methods=['GET'])
def get_cabinets():
    conn = sqlite3.connect('cabinets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM cabinets")
    cabinets = cursor.fetchall()
    conn.close()
    return jsonify([{"id": c[0], "name": c[1]} for c in cabinets])

# Добавить новый кабинет
@app.route('/add_cabinet', methods=['POST'])
def add_cabinet():
    data = request.get_json()
    cabinet_name = data.get('name')

    # Проверка на уникальность названия кабинета
    conn = sqlite3.connect('cabinets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM cabinets WHERE name = ?", (cabinet_name,))
    if cursor.fetchone():
        return jsonify({"error": "Cabinet with this name already exists"}), 400
    
    # Добавляем кабинет в основную базу данных
    cursor.execute("INSERT INTO cabinets (name) VALUES (?)", (cabinet_name,))
    conn.commit()
    conn.close()

    # Создаем отдельную базу для кабинета
    init_cabinet_db(cabinet_name)

    return '', 204

# Удалить кабинет и все его компьютеры
@app.route('/delete_cabinet/<cabinet_name>', methods=['DELETE'])
def delete_cabinet(cabinet_name):
    conn = sqlite3.connect('cabinets.db')
    cursor = conn.cursor()
    
    # Проверяем, существует ли кабинет
    cursor.execute("SELECT id FROM cabinets WHERE name = ?", (cabinet_name,))
    cabinet = cursor.fetchone()
    if not cabinet:
        return jsonify({"error": "Cabinet not found"}), 404

    # Удаляем кабинет из основной базы
    cursor.execute("DELETE FROM cabinets WHERE name = ?", (cabinet_name,))
    conn.commit()
    conn.close()

    # Удаляем базу данных кабинета и всех его компьютеров
    os.remove(f'cabinets/{cabinet_name}.db')

    return '', 204

# Получить компьютеры в кабинете по названию
@app.route('/get_computers/<cabinet_name>', methods=['GET'])
def get_computers(cabinet_name):
    db_name = f'cabinets/{cabinet_name}.db'
    
    if not os.path.exists(db_name):
        return jsonify({"error": "Cabinet not found"}), 404
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM computers")
    computers = cursor.fetchall()
    conn.close()
    return jsonify([{"id": c[0], "name": c[1]} for c in computers])

# Добавить компьютер в кабинет
@app.route('/add_computer', methods=['POST'])
def add_computer():
    data = request.get_json()
    cabinet_name = data.get('cabinet_name')
    computer_name = data.get('name')

    db_name = f'cabinets/{cabinet_name}.db'
    
    # Проверяем, существует ли база данных кабинета
    if not os.path.exists(db_name):
        return jsonify({"error": "Cabinet not found"}), 404

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Проверка на уникальность названия компьютера
    cursor.execute("SELECT id FROM computers WHERE name = ?", (computer_name,))
    if cursor.fetchone():
        return jsonify({"error": "Computer with this name already exists"}), 400
    
    # Добавляем компьютер в базу кабинета
    cursor.execute("INSERT INTO computers (name) VALUES (?)", (computer_name,))
    conn.commit()
    conn.close()

    # Создаем базу данных для характеристик компьютера
    init_computer_db(cabinet_name, computer_name)

    return '', 204

# Удалить компьютер по имени кабинета и имени компьютера
@app.route('/delete_computer/<cabinet_name>/<computer_name>', methods=['DELETE'])
def delete_computer(cabinet_name, computer_name):
    db_name = f'cabinets/{cabinet_name}.db'
    
    # Проверяем, существует ли база данных кабинета
    if not os.path.exists(db_name):
        return jsonify({"error": "Cabinet not found"}), 404

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Проверяем, существует ли компьютер
    cursor.execute("SELECT id FROM computers WHERE name = ?", (computer_name,))
    computer = cursor.fetchone()
    if not computer:
        return jsonify({"error": "Computer not found"}), 404

    # Удаляем компьютер из базы кабинета
    cursor.execute("DELETE FROM computers WHERE name = ?", (computer_name,))
    conn.commit()
    conn.close()

    # Удаляем базу данных характеристик компьютера
    os.remove(f'cabinets/{cabinet_name}_{computer_name}.db')

    return '', 204

# Страница характеристик компьютера по названию кабинета и компьютера
@app.route('/computer/<cabinet_name>/<computer_name>')
def computer(cabinet_name, computer_name):
    # Проверяем, существует ли база данных кабинета
    db_name = f'cabinets/{cabinet_name}.db'
    if not os.path.exists(db_name):
        return abort(404, description="Cabinet not found")

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM computers WHERE name = ?", (computer_name,))
    computer = cursor.fetchone()
    conn.close()

    if not computer:
        return abort(404, description="Computer not found")

    return render_template('computer.html', computer_name=computer_name)

if __name__ == '__main__':
    # Создаем основную базу кабинетов, если ее нет
    init_main_db()

    # Запускаем сервер
    app.run(debug=True)
