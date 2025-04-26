import psycopg2
import csv

#измени строку подключения к своей bd
def connect():
    return psycopg2.connect(
        dbname="Mantis",
        user="postgres",
        password="61154365",
        host="localhost",
        port="5432"
    )



def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)
    conn.commit()
    conn.close()

def insert_from_csv(file_path):
    conn = connect()
    cur = conn.cursor()
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            name, phone = row
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    conn.close()


def insert_from_input():
    name = input("Enter your name: ")
    phone = input("Enter your phone number: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    conn.close()


def update_user(name, new_phone=None, new_name=None):
    conn = connect()
    cur = conn.cursor()
    if new_phone:
        cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, name))
    if new_name:
        cur.execute("UPDATE phonebook SET name = %s WHERE name = %s", (new_name, name))
    conn.commit()
    conn.close()


def search_by_name(name_part):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s", (f"%{name_part}%",))
    results = cur.fetchall()
    for row in results:
        print(row)
    conn.close()


def delete_user_by_name_or_phone(value):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE name = %s OR phone = %s", (value, value))
    conn.commit()
    conn.close()

#можно убрать # для того что бы активировать нужную нам команду 
if __name__ == "_main_":
    connect()
    #create_table()
    insert_from_input()
    insert_from_csv("phoneBook.csv")
    #update_user("Aliya", new_phone="87001234567")
    #search_by_name("Ali")
    #delete_user_by_name_or_phone("Aliya")