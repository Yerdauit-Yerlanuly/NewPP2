import psycopg2
import csv

conn = psycopg2.connect(
    host='localhost',
    dbname='Mantis',
    user='postgres',
    password='61154365',
    port=5432)
cur = conn.cursor()

id = 1
name = ""
file = ""
phone = ""
choice = 0
done = False

def create_table(dbnameing):
    query = f"""
        CREATE TABLE IF NOT EXISTS {dbnameing} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """
    cur.execute(query)
    conn.commit()
def reset_sequence(dbnameing):
    cur.execute(f"SELECT setval(pg_get_serial_sequence('{dbnameing}', 'id'), MAX(id)) FROM {dbnameing}")
    conn.commit()

def insert_into(dbnameing):
    input_name = input("Enter name: ")
    input_phone = input("Enter phone: ")
    query = f"INSERT INTO {dbnameing} (name, phone) VALUES (%s, %s)"
    cur.execute(query, (input_name, input_phone))
    conn.commit()


print("write the name of your Database: ")
dbnameing = input()
create_table(dbnameing)
reset_sequence(dbnameing)
#Создаем цикл
while not done:

    print("""
Press 1 to insert data into phonebook
Press 0 to quit
Press 2 to enter csv
""")
    choice = int(input())
    if choice == 1:
        insert_into(dbnameing)

    elif choice == 0:
        done = 1

    elif choice == 2: #Добавляем через файл
            print("Write your csv file's name: ")
            file = input()
            #Открываем файл
            try:
                with open(file, newline='') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter = ';') #Читает файл как словарь
                    for row in reader:
                        name = row['name']
                        phone = row['phone']

                        #Добавляем запись
                        insert_into
                        conn.commit()
                print("Done")
            except:
                print("Can not find csv file")

conn.commit()

cur.close()
conn.close()