import psycopg2
import csv

# Connect to PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    dbname='Mantis',
    user='postgres',
    password='61154365',
    port=5432
)
cur = conn.cursor()

def create_table(table_name):
    query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """
    cur.execute(query)
    conn.commit()
def reset_sequence(table_name):
    cur.execute(f"""
        SELECT setval(
            pg_get_serial_sequence('{table_name}', 'id'),
            COALESCE((SELECT MAX(id) FROM {table_name}), 1),
            true
        )
    """)
    conn.commit()

def insert_into(table_name, name, phone):
    query = f"INSERT INTO {table_name} (name, phone) VALUES (%s, %s)"
    cur.execute(query, (name, phone))
    conn.commit()

def insert_from_csv(table_name, filename):
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                name = row['name']
                phone = row['phone']
                cur.execute(f"INSERT INTO {table_name} (name, phone) VALUES (%s, %s)", (name, phone))
            conn.commit()
        print("CSV data inserted successfully.")
    except FileNotFoundError:
        print("Cannot find the CSV file.")
    except Exception as e:
        print(f"Error reading CSV: {e}")

def delete_entry(table_name):
    print("Delete by:\n1. Name\n2. Phone")
    option = input("Choose option (1/2): ")

    if option == "1":
        name = input("Enter name to delete: ")
        cur.execute(f"DELETE FROM {table_name} WHERE name = %s", (name,))
    elif option == "2":
        phone = input("Enter phone to delete: ")
        cur.execute(f"DELETE FROM {table_name} WHERE phone = %s", (phone,))
    else:
        print("Invalid option.")
        return

    conn.commit()
    print("Entry deleted (if it existed).")

def update_entry(table_name):
    print("Update by:\n1. Name\n2. Phone")
    option = input("Choose option (1/2): ")

    if option == "1":
        old_name = input("Enter current name: ")
        new_name = input("Enter new name: ")
        cur.execute(f"UPDATE {table_name} SET name = %s WHERE name = %s", (new_name, old_name))

    elif option == "2":
        old_phone = input("Enter current phone: ")
        new_phone = input("Enter new phone: ")
        cur.execute(f"UPDATE {table_name} SET phone = %s WHERE phone = %s", (new_phone, old_phone))

    else:
        print("Invalid option.")
        return

    conn.commit()
    print("Entry updated.")

def view_sorted(table_name):
    print("Sort by:\n1. ID\n2. Name\n3. Phone")
    option = input("Choose option (1/2/3): ")

    if option == "1":
        sort_field = "id"
    elif option == "2":
        sort_field = "name"
    elif option == "3":
        sort_field = "phone"
    else:
        print("Invalid option.")
        return

    try:
        cur.execute(f"SELECT * FROM {table_name} ORDER BY {sort_field}")
        rows = cur.fetchall()

        print(f"\n--- Data sorted by {sort_field.upper()} ---")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    except Exception as e:
        print("Error displaying sorted data:", e)

def query_entries(table_name):
    print("""
Query Options:
1. View all entries
2. Search by name
3. Search by phone
""")
    option = input("Choose option (1/2/3): ")

    if option == "1":
        cur.execute(f"SELECT * FROM {table_name}")
    elif option == "2":
        name = input("Enter name to search: ")
        cur.execute(f"SELECT * FROM {table_name} WHERE name ILIKE %s", (f"%{name}%",))
    elif option == "3":
        phone = input("Enter phone to search: ")
        cur.execute(f"SELECT * FROM {table_name} WHERE phone LIKE %s", (f"%{phone}%",))
    else:
        print("Invalid option.")
        return

    results = cur.fetchall()
    if results:
        print("\nResults:")
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No matching records found.")


print("Enter the name of the table to use (e.g. phonebook):")
table_name = input()
create_table(table_name)
reset_sequence(table_name)

done = False
while not done:
    print("""
Press 1 to insert data into phonebook
Press 2 to load data from CSV
Press 3 to delete entry
Press 4 to update entry
Press 5 to view sorted 
Press 6 to search/query entries
Press 0 to quit
""")
    try:
        choice = int(input("Your choice: "))
    except ValueError:
        print("Please enter a number.")
        continue

    if choice == 1:
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        insert_into(table_name, name, phone)

    elif choice == 2:
        filename = input("Enter the name of the CSV file (with extension, e.g. phoneBook.csv): ")
        insert_from_csv(table_name, filename)
    
    elif choice == 3:
        delete_entry(table_name)

    elif choice == 4:
        update_entry(table_name)

    elif choice == 0:
        done = True

    elif choice == 5:
        view_sorted(table_name)
    
    elif choice == 6:
        query_entries(table_name)

    else:
        print("Invalid option. Try again.")

cur.close()
conn.close()
