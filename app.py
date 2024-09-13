import os
import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Инициализация базы данных кабинетов
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

# Создание базы данных для оборудования в кабинете
def init_cabinet_db(cabinet_name):
    db_name = f'cabinets/{cabinet_name}.db'
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

# Создание таблицы характеристик для оборудования
def init_computer_db(cabinet_name, computer_name):
    db_name = f'cabinets/{cabinet_name}_{computer_name}.db'
    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characteristics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                value TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

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

# Добавить кабинет
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

# Добавить оборудование
@app.route('/add_computer', methods=['POST'])
def add_computer():
    data = request.get_json()
    cabinet_name = data.get('cabinet_name')
    computer_name = data.get('name')
    computer_type = data.get('type')

    db_name = f'cabinets/{cabinet_name}.db'

    if not os.path.exists(db_name):
        return jsonify({"error": "Cabinet not found"}), 404

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM computers WHERE name = ?", (computer_name,))
    if cursor.fetchone():
        return jsonify({"error": "Computer with this name already exists"}), 400

    cursor.execute("INSERT INTO computers (name, type) VALUES (?, ?)", (computer_name, computer_type))
    conn.commit()
    conn.close()

    init_computer_db(cabinet_name, computer_name)
    return '', 204

# Получить список оборудования в кабинете
@app.route('/get_computers/<cabinet_name>', methods=['GET'])
def get_computers(cabinet_name):
    db_name = f'cabinets/{cabinet_name}.db'
    if not os.path.exists(db_name):
        return jsonify([])

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM computers")
    computers = cursor.fetchall()
    conn.close()

    return jsonify([{"name": c[0]} for c in computers])

# Получить характеристики для оборудования (с отображением сохраненных значений)
@app.route('/get_characteristics/<cabinet_name>/<computer_name>', methods=['GET'])
def get_characteristics(cabinet_name, computer_name):
    conn = sqlite3.connect(f'cabinets/{cabinet_name}.db')
    cursor = conn.cursor()
    cursor.execute("SELECT type FROM computers WHERE name = ?", (computer_name,))
    computer_type = cursor.fetchone()[0]
    conn.close()

    # Возможные характеристики в зависимости от типа оборудования
    characteristics_template = {
        "comp": ["Инвентарный номер", "Процессор", "ОЗУ", "Накопитель"],
        "laptop": ["Инвентарный номер", "Процессор", "ОЗУ", "Накопитель"],
        "monitor": ["Инвентарный номер", "Модель"],
        "projector": ["Инвентарный номер", "Модель"],
        "printer": ["Инвентарный номер", "Модель", "Сетевой принтер/нет"],
        "monoblock": ["Инвентарный номер", "Процессор", "ОЗУ", "Жесткий диск"],
        "interactive_board": ["Инвентарный номер", "Производитель"]
    }

    # Получаем сохраненные характеристики
    conn = sqlite3.connect(f'cabinets/{cabinet_name}_{computer_name}.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, value FROM characteristics")
    saved_characteristics = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()

    # Возвращаем шаблон характеристик с сохраненными значениями, если они есть
    characteristics = []
    for characteristic in characteristics_template.get(computer_type, []):
        characteristics.append({
            'name': characteristic,
            'value': saved_characteristics.get(characteristic, "")
        })

    return jsonify(characteristics)

# Удалить кабинет
@app.route('/delete_cabinet/<cabinet_name>', methods=['DELETE'])
def delete_cabinet(cabinet_name):
    conn = sqlite3.connect('cabinets.db')
    cursor = conn.cursor()
    
    # Удаляем кабинет из таблицы cabinets
    cursor.execute("DELETE FROM cabinets WHERE name = ?", (cabinet_name,))
    
    if cursor.rowcount == 0:
        return jsonify({"error": "Cabinet not found"}), 404

    conn.commit()
    conn.close()

    # Удаляем базу данных для этого кабинета
    db_name = f'cabinets/{cabinet_name}.db'
    if os.path.exists(db_name):
        os.remove(db_name)
    
    # Удаляем базы данных характеристик для оборудования в этом кабинете
    for file in os.listdir('cabinets'):
        if file.startswith(f'{cabinet_name}_'):
            os.remove(f'cabinets/{file}')

    return '', 204

# Удалить оборудование
@app.route('/delete_computer/<cabinet_name>/<computer_name>', methods=['DELETE'])
def delete_computer(cabinet_name, computer_name):
    db_name = f'cabinets/{cabinet_name}.db'

    if not os.path.exists(db_name):
        return jsonify({"error": "Cabinet not found"}), 404

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Удаляем компьютер из таблицы computers
    cursor.execute("DELETE FROM computers WHERE name = ?", (computer_name,))

    if cursor.rowcount == 0:
        return jsonify({"error": "Computer not found"}), 404

    conn.commit()
    conn.close()

    # Удаляем базу данных характеристик для этого компьютера
    computer_db = f'cabinets/{cabinet_name}_{computer_name}.db'
    if os.path.exists(computer_db):
        os.remove(computer_db)

    return '', 204


# Сохранить или обновить характеристики оборудования
@app.route('/save_characteristics/<cabinet_name>/<computer_name>', methods=['POST'])
def save_characteristics(cabinet_name, computer_name):
    data = request.get_json()
    characteristics = data.get('characteristics', {})

    db_name = f'cabinets/{cabinet_name}_{computer_name}.db'
    if not os.path.exists(db_name):
        return jsonify({"error": "Computer not found"}), 404

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Для каждой характеристики проверяем, существует ли она, если да, обновляем, если нет — добавляем
    for name, value in characteristics.items():
        cursor.execute('''
            INSERT INTO characteristics (name, value)
            VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET value=excluded.value
        ''', (name, value))

    conn.commit()
    conn.close()

    return '', 204


if __name__ == '__main__':
    init_main_db()
    app.run(debug=True)
