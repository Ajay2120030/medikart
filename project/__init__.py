import mysql.connector
from unicodedata import category


class MediStore:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="ajay",
            database="project2"
        )
        self.cursor = self.db.cursor()
        self.name = "Knowledge"
        self.var1 = ""
        self.var2 = ""
        self.create_tables()

    def create_tables(self):
        users = ("create table if not exists Users ("
                 "name varchar(20) not null,\n"
                 "password varchar(20) not null,\n"
                 "email varchar(20) not null check (email like '%@%'))")
        self.cursor.execute(users)
        self.db.commit()

        medicines = (
            "create table if not exists medicines("
            "id int auto_increment primary key ,\n"
            "category varchar(20) not null,\n"
            "name varchar(20) not null,\n"
            "price decimal (10,2) not null,\n"
            "stock int not null \n)")
        self.cursor.execute(medicines)
        self.db.commit()

        orders = ("create table if not exists orders("
                  "id int auto_increment primary key ,\n"
                  "user_email varchar(40) not null check (user_email like '%@%'),\n"
                  "medicine_name varchar(20) not null,\n"
                  "quantity int not null ,\n"
                  "order_time DATETIME DEFAULT CURRENT_TIMESTAMP)")
        self.cursor.execute(orders)
        self.db.commit()

    def displayMedicines(self):
       

        self.cursor.execute("SELECT DISTINCT category FROM medicines")
        categories = [c[0] for c in self.cursor.fetchall()]
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")

        choice = input("Select category: ")
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            category = categories[int(choice) - 1]
            self.cursor.execute("SELECT name, price, stock FROM medicines WHERE category=%s", (category,))
            medicines = self.cursor.fetchall()
            for med in medicines:
                print(f"---> {med[0]} | Price: ₹{med[1]} | Stock: {med[2]}")

        else:
            print("Invalid choice.")

    def placeOrder(self):
        self.displayMedicines()
        # category = input("Enter category: ")
        medicine = input("Enter medicine name: ")
        quantity = int(input("Enter quantity: "))

        # Check availability
        self.cursor.execute("SELECT stock, price FROM medicines WHERE category=%s AND name=%s", (category, medicine))
        result = self.cursor.fetchone()
        if result:
            stock, price = result
            if stock >= quantity:
                total = price * quantity
                self.cursor.execute("INSERT INTO orders (user_email, medicine_name, quantity) VALUES (%s, %s, %s)",
                                    (self.var2, medicine, quantity))
                self.cursor.execute("UPDATE medicines SET stock = stock - %s WHERE category=%s AND name=%s",
                                    (quantity, category, medicine))
                self.db.commit()
                print(f"Order placed successfully for {quantity} unit(s) of {medicine}. Total: ₹{total}")
            else:
                print("Insufficient stock.")
        else:
            print("Medicine not found.")

    def register(self):
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        if '@' not in email:
            print("Invalid email format.")
            return
        password = input("Enter your password: ")

        self.cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if self.cursor.fetchone():
            print("Email already registered.")
            return

        self.cursor.execute("INSERT INTO users (name, password, email) VALUES (%s, %s, %s)", (name, password, email))
        self.db.commit()
        print("Registration successful.")

    def login(self):
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        self.cursor.execute("SELECT name FROM users WHERE email=%s AND password=%s", (email, password))
        result = self.cursor.fetchone()
        if result:
            self.var2 = email  # store email for orders
            print(f"Welcome {result[0]}")
            self.user_menu()
        else:
            print("Invalid credentials.")

    def user_menu(self):
        while True:
            print("\n1. View Medicines\n2. Place Order\n 3.viewOrders\n4. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.displayMedicines()
            elif choice == '2':
                self.placeOrder()

            elif choice == '3':
                self.viewOrders()
            elif choice == '4':
                print("Thank you for visiting MediStore.")

                break
            else:
                print("Invalid choice.")

    def admin_login(self):
        admin_name = input("Enter admin username: ")
        password = input("Enter admin password: ")
        if admin_name == "admin" and password == "admin123":
            print("Welcome, Admin!")
            self.admin_menu()
        else:
            print("Access denied.")

    def admin_menu(self):
        while True:
            print("\n1. Add Medicine\n2. View Medicines\n3.viewOrders\n4. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.addMedicine()
            elif choice == '2':
                self.displayMedicines()
            elif choice == '3':
                self.viewAllOrders()

            elif choice == '4':
                break
            else:
                print("Invalid choice.")

    def viewAllOrders(self):
        self.cursor.execute(
            "SELECT user_email, medicine_name, quantity, order_time FROM orders ORDER BY order_time DESC")
        for user, med, qty, time in self.cursor.fetchall():
            print(f"User: {user} | Medicine: {med} | Qty: {qty} | Time: {time}")

    def addMedicine(self):
        category = input("Enter medicine category: ")
        name = input("Enter medicine name: ")
        price = float(input("Enter price: "))
        stock = int(input("Enter stock: "))
        self.cursor.execute("INSERT INTO medicines (category, name, price, stock) VALUES (%s, %s, %s, %s)",
                            (category, name, price, stock))
        self.db.commit()
        print("Medicine added successfully.")

    def viewOrders(self):
        self.cursor.execute("SELECT medicine_name, quantity, order_time FROM orders WHERE user_email=%s", (self.var2,))
        orders = self.cursor.fetchall()
        if orders:
            print("\n--- Your Orders ---")
            for med, qty, time in orders:
                print(f"{med} | Quantity: {qty} | Ordered on: {time}")

        else:
            print("You have no past orders.")

    def home(self):
        print(f"-----> Welcome to {self.name} MediStore <-----")
        while True:
            print("\n1. Admin Login\n2. User Login\n3. Register\n4. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.admin_login()
            elif choice == '2':
                self.login()
            elif choice == '3':
                self.register()
            elif choice == '4':
                break
            else:
                print("Invalid choice.")


# if __name__ == "__main__":
#     app = MediStore()
#     app.home()
s=MediStore()
s.home()
