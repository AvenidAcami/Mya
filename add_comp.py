import os
import sqlite3
import psutil
import platform
import subprocess
import datetime
import random

def get_computer_name():
    system = platform.system()
    if system == "Windows":
        try:
            output = subprocess.check_output("hostname", shell=True).decode().strip()
        except Exception as e:
            output = f"Error getting computer name: {str(e)}"
    elif system == "Linux":
        try:
            output = subprocess.check_output("hostname", shell=True).decode().strip()
        except Exception as e:
            output = f"Error getting computer name: {str(e)}"
    else:
        output = "Unsupported OS"
    return output

def get_cpu_model():
    system = platform.system()
    if system == "Windows":
        try:
            output = subprocess.check_output("wmic cpu get caption", shell=True).decode()
            cpu_model = output.split('\n')[1].strip()
        except Exception as e:
            cpu_model = f"Error getting CPU model: {str(e)}"
    elif system == "Linux":
        try:
            output = subprocess.check_output("lscpu | grep 'Model name:'", shell=True).decode()
            cpu_model = output.split(':')[1].strip()
        except Exception as e:
            cpu_model = f"Error getting CPU model: {str(e)}"
    else:
        cpu_model = "Unsupported OS"
    return cpu_model

def generate_computer_name(inventory_number):
    # Генерируем уникальное имя компьютера на основе текущей даты, времени и случайного числа
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    random_number = random.randint(1000, 9999)
    return f'Computer_{inventory_number}_{timestamp}_{random_number}'

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

def add_computer_to_cabinet(cabinet_number, inventory_number):
    cabinet_name = f'{cabinet_number}'
    computer_name = get_computer_name()

    # Получаем информацию о компьютере
    cpu_model = get_cpu_model()
    ram_info = f'{psutil.virtual_memory().total // (1024 * 1024)} MB'
    disk_info = f'{psutil.disk_usage("/").total // (1024 * 1024 * 1024)} GB'

    # Добавляем кабинет, если он не существует
    init_main_db()
    init_cabinet_db(cabinet_name)

    # Добавляем компьютер в базу данных
    db_name = f'cabinets/{cabinet_name}.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM computers WHERE name = ?", (computer_name,))
    if cursor.fetchone():
        print("Computer with this name already exists.")
        return

    cursor.execute("INSERT INTO computers (name, type) VALUES (?, ?)", (computer_name, 'comp'))
    conn.commit()
    conn.close()

    # Создаем базу данных для характеристик компьютера
    init_computer_db(cabinet_name, computer_name)

    # Сохраняем характеристики
    characteristics = {
        'Инвентарный номер': inventory_number,
        'Процессор': cpu_model,
        'ОЗУ': ram_info,
        'Накопитель': disk_info
    }

    conn = sqlite3.connect(f'cabinets/{cabinet_name}_{computer_name}.db')
    cursor = conn.cursor()
    for name, value in characteristics.items():
        cursor.execute('''
            INSERT INTO characteristics (name, value)
            VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET value=excluded.value
        ''', (name, value))
    conn.commit()
    conn.close()

    print(f'Computer {computer_name} added successfully with the following characteristics:')
    for name, value in characteristics.items():
        print(f'{name}: {value}')

if __name__ == '__main__':
    cabinet_number = input("Enter cabinet number: ")
    inventory_number = input("Enter inventory number: ")
    add_computer_to_cabinet(cabinet_number, inventory_number)
