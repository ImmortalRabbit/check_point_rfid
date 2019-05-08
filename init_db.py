import psycopg2

if __name__ == '__main__':
    try:
        connection = psycopg2.connect(user="odoo",
                                      password="odoo",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="rfid")
        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE users (NAME TEXT NOT NULL, SURNAME TEXT NOT NULL, KEY TEXT NOT NULL); ''')
        cursor.execute('''INSERT INTO users (NAME, SURNAME, KEY) VALUES(%s,%s,%s)''', ("Demezhan", "Marikov", "9898A1232"))
        cursor.execute('''SELECT * FROM users ''')

        for i in cursor:
            print(i)

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # closing database connection.

        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
