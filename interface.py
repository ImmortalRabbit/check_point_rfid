from tkinter import ttk

import psycopg2
import serial

try:
    from tkinter import *
except:
    from tkinter import *


class interface:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.com = "/dev/ttyACM0"

        self.password = StringVar()

        self.name = StringVar()
        self.surname = StringVar()
        self.code = StringVar()

        self.passLabel = Label(self.root, text='Enter your Password', font=("Arial", "14"))
        self.enteredPass = Entry(self.root, textvariable=self.password)
        self.login = Button(self.root, text="login", command=self.check_password, font=("Arial", "14"))
        self.wrongMessage = Label(self.root, text="Wrong password", font=("Arial", "14"))

        self.addUserLabel = Label(self.root, text="Add user: ", font=("Arial", "14"))
        self.addUserButton = Button(self.root, text="add", command=self.addUser, font=("Arial", "14"))
        self.nameLabel = Label(self.root, text="Name: ", font=("Arial", "14"))
        self.nameEntry = Entry(self.root, textvariable=self.name)
        self.surnameLabel = Label(self.root, text="Surname: ", font=("Arial", "14"))
        self.surnameEntry = Entry(self.root, textvariable=self.surname)
        self.codeLabel = Label(self.root, text="Code: ", font=("Arial", "14"))
        self.getActualCode = Button(self.root, text="get code", command=self.getID, font=("Arial", "14"))
        self.actualCodeLabel = Label(self.root, text=self.code, font=("Arial", "14"))

        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ("NAME", "SURNAME", "KEY")
        self.tree['show'] = 'headings'
        self.tree.column("NAME", width=70)
        self.tree.column("SURNAME", width=70)
        self.tree.column("KEY", width=70)
        self.tree.heading("NAME", text="NAME")
        self.tree.heading("SURNAME", text="SURNAME")
        self.tree.heading("KEY", text="KEY")

        self.userLabel = Label(self.root, text="Click to button and insert you key", font=("Arial", "14"))
        self.userButton = Button(self.root, text="login", command=self.check_user)

        try:
            self.connection = psycopg2.connect(user="odoo",
                                               password="odoo",
                                               host="127.0.0.1",
                                               port="5432",
                                               database="rfid")

            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("error")

        self.create_interface(user)

    def create_interface(self, user):
        self.destroyMain()
        if user == "admin":
            self.create_admin()
        else:
            self.create_user()

    def create_admin(self):
        self.passLabel.place(x=100, y=40)
        self.enteredPass.place(x=100, y=100)
        self.login.place(x=140, y=150)

    def create_user(self):
        self.userLabel.place(x=100, y=40)
        self.userButton.place(x=150, y=100)

    def check_user(self):
        self.connect()
        ls = []
        for i in range(7):
            try:
                ser = serial.Serial(self.com, 9600, timeout=100)
                content = ser.readline().decode('ascii')
                ls.append(content.split(" ")[1])
            except:
                continue

        max = ls[0]
        for i in ls:
            if len(i) > len(max):
                max = i
        key = max[:-2]
        self.cursor.execute("""SELECT * FROM users """)
        self.userLabel['text'] = "Access is restricted"
        for i in self.cursor:
            if i[2] == key:
                self.userLabel['text'] = "Welcome, " + i[0] + " " + i[1]
                ser.write(("H").encode())

    def check_password(self):
        self.wrongMessage.place(x=100, y=200)
        enteredPass = self.password.get()
        print("hello")
        if enteredPass == "admin":
            self.passLabel.destroy()
            self.enteredPass.destroy()
            self.login.destroy()
            self.wrongMessage.destroy()
            self.admin_page()

    def admin_page(self):
        self.getUsers()
        self.addUserLabel.place(x=50, y=10)
        self.nameLabel.place(x=50, y=35)
        self.nameEntry.place(x=50, y=60)
        self.surnameLabel.place(x=50, y=85)
        self.surnameEntry.place(x=50, y=110)
        self.codeLabel.place(x=50, y=135)
        self.getActualCode.place(x=120, y=135)
        self.addUserButton.place(x=150, y=10)

    def connect(self):
        try:
            self.connection = psycopg2.connect(user="odoo",
                                               password="odoo",
                                               host="127.0.0.1",
                                               port="5432",
                                               database="rfid")

            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("error")

    def getID(self):
        ls = []
        for i in range(7):
            try:
                ser = serial.Serial(self.com, 9600, timeout=100)
                content = ser.readline().decode('ascii')
                ls.append(content.split(" ")[1])
            except:
                continue

        max = ls[0]
        for i in ls:
            if len(i) > len(max):
                max = i
        max = max[:-2]
        self.code = max
        self.actualCodeLabel['text'] = max
        self.actualCodeLabel.place(x=50, y=170)
        ser.write(("H").encode())

    def addUser(self):
        try:

            self.connect()
            self.cursor.execute("""SELECT * FROM users """)
            print(self.name.get())
            print(self.surname.get())
            print(self.code)
            self.cursor.execute("""INSERT INTO users (name, surname, key) VALUES(%s,%s,%s)""",
                                (self.name.get(), self.surname.get(), self.code))
            print("working")

            self.getUsers()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("error")

    def getUsers(self):
        try:

            self.cursor.execute("""SELECT * FROM users """)

            for i in self.tree.get_children():
                self.tree.delete(i)

            for i in self.cursor:
                print(i)
                self.tree.insert("", 0, text="FETCHED --- >", values=(i[0], i[1], i[2]))

            self.tree.pack(expand=False, fill='y')
            self.tree.place(x=260, y=0)
            self.root.update()
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            # closing database connection.
            if self.connection:
                self.cursor.close()
                self.connection.close()
                print("PostgreSQL connection is closed")

    def destroyMain(self):
        admin.destroy()
        user.destroy()
        labelLogin.destroy()


def admin_auth():
    interface(root, "admin")


def user_auth():
    interface(root, "user")


if __name__ == '__main__':
    root = Tk()

    root.geometry("500x250+50+50")
    root.title('RFID MONITOR')
    root.resizable(width=False, height=False)
    labelLogin = Label(root, text='Login as:', font=("Arial", "14"))
    labelLogin.place(x=200, y=40)
    admin = Button(root, text='Admin', command=admin_auth, font=("Arial", "14"))
    admin.place(x=100, y=110)
    user = Button(root, text='User', command=user_auth, font=("Arial", "14"))
    user.place(x=300, y=110)
    root.mainloop()
