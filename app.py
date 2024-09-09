import os
import sqlite3
from flask import Flask, request, jsonify, render_template, redirect

app = Flask(__name__)

# Функция для инициализации базы данных кабинетов
def init_main_db():
    if not os.path.exists('cabinets.db'):
        conn = sqlite3.connect('cabinets.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cabinets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
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
            name TEXT NOT NULL
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
    
    # Добавляем кабинет в основную базу данных
    conn = sqlite3.connect('cabinets.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cabinets (name) VALUES (?)", (cabinet_name,))
    conn.commit()
    conn.close()

    # Создаем отдельную базу для кабинета
    init_cabinet_db(cabinet_name)

    return '', 204

# Удалить кабинет и все его компьютеры
@app.route('/delete_cabinet/<int:cabinet_id>', methods=['DELETE'])
def delete_cabinet(cabinet_id):
    conn = sqlite3.connect('cabinets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM cabinets WHERE id = ?", (cabinet_id,))
    cabinet_name = cursor.fetchone()[0]
    
    # Удаляем кабинет из основной базы
    cursor.execute("DELETE FROM cabinets WHERE id = ?", (cabinet_id,))
    conn.commit()
    conn.close()

    # Удаляем базу данных кабинета и всех его компьютеров
    os.remove(f'cabinets/{cabinet_name}.db')

    return '', 204

# Получить компьютеры в кабинете
@app.route('/get_computers/<int:cabinet_id>', methods=['GET'])
def get_computers(cabinet_id):
    conn = sqlite3.connect('cabinets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM cabinets WHERE id = ?", (cabinet_id,))
    cabinet_name = cursor.fetchone()[0]
    
    db_name = f'cabinets/{cabinet_name}.db'
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
    cabinet_id = data.get('cabinet_id')
    computer_name = data.get('name')

    # Получаем имя кабинета
    conn = sqlite3.connect('cabinets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM cabinets WHERE id = ?", (cabinet_id,))
    cabinet_name = cursor.fetchone()[0]

    # Добавляем компьютер в базу кабинета
    db_name = f'cabinets/{cabinet_name}.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO computers (name) VALUES (?)", (computer_name,))
    conn.commit()
    conn.close()

    # Создаем базу данных для характеристик компьютера
    init_computer_db(cabinet_name, computer_name)

    return '', 204

# Удалить компьютер
@app.route('/delete_computer/<int:cabinet_id>/<int:computer_id>', methods=['DELETE'])
def delete_computer(cabinet_id, computer_id):
    # Получаем имя кабинета
    conn = sqlite3.connect('cabinets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM cabinets WHERE id = ?", (cabinet_id,))
    cabinet_name = cursor.fetchone()[0]

    # Получаем имя компьютера
    db_name = f'cabinets/{cabinet_name}.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM computers WHERE id = ?", (computer_id,))
    computer_name = cursor.fetchone()[0]

    # Удаляем компьютер из базы кабинета
    cursor.execute("DELETE FROM computers WHERE id = ?", (computer_id,))
    conn.commit()
    conn.close()

    # Удаляем базу данных характеристик компьютера
    os.remove(f'cabinets/{cabinet_name}_{computer_name}.db')

    return '', 204

# Страница характеристик компьютера
@app.route('/computer/<int:cabinet_id>/<int:computer_id>')
def computer(cabinet_id, computer_id):
    # Получаем имя кабинета
    conn = sqlite3.connect('cabinets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM cabinets WHERE id = ?", (cabinet_id,))
    cabinet_name = cursor.fetchone()[0]

    # Получаем имя компьютера
    db_name = f'cabinets/{cabinet_name}.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM computers WHERE id = ?", (computer_id,))
    computer_name = cursor.fetchone()[0]
    conn.close()

    return render_template('computer.html', computer_name=computer_name)

if __name__ == '__main__':
    # Создаем основную базу кабинетов, если ее нет
    init_main_db()

    # Запускаем сервер
    app.run(debug=True)
