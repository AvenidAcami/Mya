import os
import sqlite3
import psutil
import platform
import subprocess
import datetime
import random
import cpuinfo

def get_computer_name():
    system = platform.system()
    if system == "Windows" or system == "Linux":
        try:
            output = subprocess.check_output("hostname", shell=True).decode().strip()
        except Exception as e:
            output = f"Error getting computer name: {str(e)}"
    else:
        output = "Unsupported OS"
    return output

def get_cpu_model():
    try:
        cpu_info = cpuinfo.get_cpu_info()
        cpu_model = cpu_info['brand_raw']
    except Exception as e:
        cpu_model = f"Error getting CPU model: {str(e)}"
    return cpu_model

def generate_computer_name(inventory_number):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    random_number = random.randint(1000, 9999)
    return f'Computer_{inventory_number}_{timestamp}_{random_number}'

def init_main_db():
    if not os.path.exists('cabinets.db'):
        conn = sqlite3.connect('cabinets.db')
        cursor = conn.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS cabinets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        ) ''')
        conn.commit()
        conn.close()

def init_cabinet_db(cabinet_name):
    db_name = f'cabinets/{cabinet_name}.db'
    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS computers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL
        ) ''')
        conn.commit()
        conn.close()

def init_computer_db(cabinet_name, computer_name):
    db_name = f'cabinets/{cabinet_name}_{computer_name}.db'
    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS characteristics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL
        ) ''')
        conn.commit()
        conn.close()

def add_computer_to_cabinet(cabinet_number, inventory_number):
    cabinet_name = f'{cabinet_number}'
    computer_name = get_computer_name()
    cpu_model = get_cpu_model()
    ram_info = f'{psutil.virtual_memory().total // (1024 * 1024)} MB'
    disk_info = f'{psutil.disk_usage("/").total // (1024 * 1024 * 1024)} GB'

    init_main_db()
    init_cabinet_db(cabinet_name)

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

    init_computer_db(cabinet_name, computer_name)

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
            INSERT INTO characteristics (name, value) VALUES (?, ?)
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