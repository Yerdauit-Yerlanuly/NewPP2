import psycopg2, csv

# Параметры подключения
conn = psycopg2.connect(
    host = "localhost",
    port = 5432,            #Стандартный порт PostgreSQL
    database = "phonebook11", #Имя базы данных
    user = "postgres",      #Имя пользователя
    password = "61154365"           #Пароль
)

#Создаем курсор
cursor = conn.cursor()

#Переменные
limit = 0
offset = 0
id = 1
name = ""
surname = ""
file = ""
phone = ""
choice = 0
done = False
listOfUsers = []

#Создаем цикл
while not done:
    print("""
Press 1 to insert/update data into phonebook
Press 2 to return all records based on a pattern
Press 3 to query data with pagination
Press 4 to delete data from phonebook
Press 5 to see all records
Press 0 to quit
""")
    choice = int(input())



    if choice == 1: #Чтобы добавить запись
        print("""
Press 1 to insert/update data through console
Press 2 to insert data through csv file
Press 3 to insert many data through console
Press 0 to quit
""")
        choice = int(input())

        if choice == 1: #Чтобы добавить или обновить мнфу
            print("Name: ")
            name = input()

            print("Surname: ")
            surname = input()

            print("Phone number: ")
            phone = input()

            #Вызываем процедуру
            cursor.execute("""
                CALL insertorupdate(%s, %s, %s);
            """, (name, surname, phone))
            conn.commit()

            print("Done")



        elif choice == 2: #Добавляем через файл
            print("Write your csv file's name: ")
            file = input()

            #Открываем файл
            try:
                with open(f"{file}.csv", newline = '') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter = ';') #Читает файл как словарь
                    for row in reader:
                        name = row['name']
                        surname = row['surname']
                        phone = row['number']

                        #Вызываем функцию
                        cursor.execute("""
                            CALL insertorupdate(%s, %s, %s);
                        """, (name, surname, phone))
                        conn.commit() #Коммитим
                
                print("Done")
            except:
                print("Can not find csv file")



        elif choice == 3: #Добавляем несколько людей
            print("Amount of users: ")
            count = int(input())

            for i in range(count):
                print("Name: ")
                name = input()

                print("Surname: ")
                surname = input()

                print("Phone number: ")
                phone = input()

                tuple = (name, surname, phone, len(phone))
                listOfUsers.append(tuple)

                print()

            #Это тип данных, которую я использую при вызове процедуры manyusers
            #CREATE TYPE userinput AS (inname TEXT, insurname TEXT, innumber TEXT, len INT);
            cursor.execute("""
                CALL manyusers(%s::userinput[]);
            """, (listOfUsers,))
            conn.commit()

            if conn.notices: #Есть ли какое то замечание
                print(conn.notices[0].strip())
            else:
                print("Done")
        else: #Если нажали ноль или что то еще
            done = True





    elif choice == 2: #Чтобы отфильтровать
        print("""
Press 1 to return all records based on name pattern
Press 2 to return all records based on surname pattern
Press 3 to return all records based on phone number pattern
Press 0 to quit
""")
        choice = int(input())
        print("Pattern: ")

        if choice == 1: #По имени
            name = input()

            #Вызываем функцию
            cursor.execute("""
                SELECT * FROM searchByPattern(%s, NULL, NULL);
            """, (name,))
            info = cursor.fetchall()

            if info:
                for data in info:
                    print("ID: " + str(data[0]) + "; Name: " + str(data[1]) + "; Surname: " + str(data[2]) + "; Phone number: " + str(data[3]))
            else:
                print("Not found")

        
        elif choice == 2: #По фамилии
            surname = input()

            cursor.execute("""
                SELECT * FROM searchByPattern(NULL, %s, NULL);
            """, (surname,))
            info = cursor.fetchall()

            if info:
                for data in info:
                    print("ID: " + str(data[0]) + "; Name: " + str(data[1]) + "; Surname: " + str(data[2]) + "; Phone number: " + str(data[3]))
            else:
                print("Not found")

        
        elif choice == 3: #По номеру
            phone = input()

            cursor.execute("""
                SELECT * FROM searchByPattern(NULL, NULL, %s);
            """, (phone,))
            info = cursor.fetchall()

            if info:
                for data in info:
                    print("ID: " + str(data[0]) + "; Name: " + str(data[1]) + "; Surname: " + str(data[2]) + "; Phone number: " + str(data[3]))
            else:
                print("Not found")


        else:
            done = True





    elif choice == 3: #Чтобы вывести с учетом лиммита и оффсета
        print("Limit: ")
        limit = int(input())

        print("Offset: ")
        offset = int(input())

        #Вызываем функцию
        cursor.execute("""
            SELECT * FROM pagination(%s, %s)
        """, (limit, offset))
        info = cursor.fetchall()

        if info:
            for data in info:
                print("ID: " + str(data[0]) + "; Name: " + str(data[1]) + "; Surname: " + str(data[2]) + "; Phone number: " + str(data[3]))
        else:
            print("Nothing found")
        




    elif choice == 4: #Чтобы удалить инфу
        cursor.execute("""
            SELECT * FROM phonebook;
        """)
        info = cursor.fetchall()

        if info:
            #Выводим инфу
            for data in info:
                print("ID: " + str(data[0]) + "; Name: " + str(data[1]) + "; Surname: " + str(data[2]) + "; Phone number: " + str(data[3]))
            
            print("""
Press 1 to delete by name
Press 2 to delete by phone number
Press 0 to quit
""")
            choice = int(input())

            if choice == 1: #Чтобы удалить по имени
                print("Name: ")
                name = input()

                cursor.execute("""
                    SELECT * FROM phonebook
                    WHERE name = %s;
                """, (name,))
                info = cursor.fetchall()

                if len(info) > 1: #Если в таблице несколько похожих имен
                    for data in info:
                        print("ID: " + str(data[0]) + "; Name: " + str(data[1]) + "; Surname: " + str(data[2]) + "; Phone number: " + str(data[3]))

                    print("There exists some records with the same name")

                    print("Phone number: ")
                    phone = input()

                    cursor.execute("""
                        SELECT * FROM phonebook
                        WHERE name = %s AND number = %s;
                    """, (name, phone))
                    info = cursor.fetchone()

                    if info:
                        #Вызываем процедуру
                        cursor.execute("""
                            CALL deletefromtable(%s, %s);
                        """, (name, phone))
                        conn.commit()

                        print("Done")
                    else:
                        print("The entry not found")
                else:
                    #Вызываем процедуру
                    cursor.execute("""
                        CALL deletefromtable(%s, NULL);
                    """, (name,))
                    conn.commit()

                    print("Done")


            elif choice == 2: #Чтобы удалить по номеру
                print("Phone number: ")
                phone = input()

                cursor.execute("""
                    SELECT * FROM phonebook
                    WHERE number = %s;
                """, (phone,))
                info = cursor.fetchone()

                if info:
                    #Вызываем процедуру
                    cursor.execute("""
                        CALL deletefromtable(NULL, %s);
                    """, (phone,))
                    conn.commit()

                    print("Done")
                else:
                    print("Not found")
            else:
                done = True
        else: #Если в таблице ничего нет
            print("Nothing to delete")





    elif choice == 5: #Чтобы вывыести всю таблицу
        cursor.execute("""
            SELECT * FROM phonebook;
        """)
        info = cursor.fetchall()

        if info:
            for data in info:
                print("ID: " + str(data[0]) + "; Name: " + str(data[1]) + "; Surname: " + str(data[2]) + "; Phone number: " + str(data[3]))
        else:
            print("Empty")





    else: #Если нажали 0
        done = True

# Закрываем соединение
cursor.close()
conn.close()