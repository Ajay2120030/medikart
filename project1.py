import mysql.connector


class MediStore:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="ajay",
            database="project3"
        )
        self.cursor = self.db.cursor()
        self.name = "Wellness"
        self.var1 = ""
        self.var2 = ""
        self.create_tables()

    def create_tables(self):
        users = ("create table if not exists users ("
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

        orders = (
            "CREATE TABLE IF NOT EXISTS orders ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "user_email VARCHAR(40) NOT NULL CHECK (user_email LIKE '%@%'), "
            "medicine_name VARCHAR(20) NOT NULL, "
            "quantity INT NOT NULL)"
        )
        self.cursor.execute(orders)
        self.db.commit()

    def View_Medicines(self):

        select = "select DISTINCT category from medicines"
        self.cursor.execute(select)
        categories = self.cursor.fetchall()
        if not categories:
            print("No medicines")
            return
        print("Available Categories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category[0]}")
        choice = input("Enter your choice  : ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(categories):
            print("Invalid choice")
            return

        selected_Category = categories[int(choice) - 1][0]
        select = "select name,price,stock from medicines where category=%s"
        self.cursor.execute(select, (selected_Category,))
        medicines = self.cursor.fetchall()
        if not medicines:
            print("No medicines")
            return

        print(f"\n medicines : {selected_Category}:")
        for medicine in medicines:
            print(f"{medicine[0]} : {medicine[1]} : {medicine[2]}")

    def placeOrder(self):
        self.View_Medicines()
        category = input("Enter category: ")
        medicine = input("Enter medicine name: ")
        quantity = int(input("Enter quantity: "))

        select = "SELECT stock, price FROM medicines WHERE category=%s AND name=%s"
        self.cursor.execute(select, (category, medicine))
        # self.cursor.execute("SELECT stock, price FROM medicines WHERE category={} AND name={}".format(category,medicine),
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

    def viewOrders(self):
        # select="SELECT medicine_name, quantity, order_time FROM orders WHERE user_email{}".format(self.var2)

        select = "SELECT medicine_name, quantity FROM orders WHERE user_email=%s"
        self.cursor.execute(select, (self.var2,))
        orders = self.cursor.fetchall()
        if orders:
            print("\n--- Your Orders ---")
            for med, qty in orders:
                print(f"{med} | Quantity: {qty} ")

        else:
            print("You have no past orders.")

    def User_Register(self):
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        if '@' not in email:
            print("Invalid email format.")
            return
        password = input("Enter your password: ")

        select = "SELECT * FROM users WHERE email=%s"
        self.cursor.execute(select, (email,))
        if self.cursor.fetchone():
            print("Email already registered.")
            return

        self.cursor.execute("INSERT INTO users (name, password, email) VALUES (%s, %s, %s)", (name, password, email))
        self.db.commit()
        print("Registration successful.")

    def User_login(self):
        email = input("Enter your email: ")
        if '@' not in email:
            print(f"Invalid Email")
            return

        password = input("Enter your password: ")

        self.cursor.execute("SELECT name FROM users WHERE email=%s AND password=%s", (email, password))
        result = self.cursor.fetchone()
        if result:
            self.var2 = email
            print(f"Welcome {result[0]}")
            self.user_menu()
        else:
            print("Invalid credentials.")

    def user_menu(self):
        while True:
            print("\n1. View Medicines\n2. Place Order\n3.viewOrders\n4. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.View_Medicines()
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
        password = int(input("Enter admin password: "))
        if admin_name == "ajay" and password == 1234:
            print(f"Welcome ADMIN {admin_name} ")
            self.admin_menu()
        else:
            print("Access denied.")

    def Registered_Users(self):
        select = "SELECT name, email FROM users"
        self.cursor.execute(select)
        users = self.cursor.fetchall()
        if users:
            print("\n--- Registered Users ---")
            for name, email in users:
                print(f"Name: {name} | Email: {email}")
        else:
            print("No users found.")

    def admin_menu(self):
        while True:
            print("\n--- Admin Menu ---")
            print("1. Add Medicine")
            print("2. View Medicines")
            print("3. View Orders")
            print("4. Registered Users")
            print("5. Exit")

            choice = int(input("Enter your choice: "))

            if choice == 1:
                self.Add_Medicine()
            elif choice == 2:
                self.View_Medicines()
            elif choice == 3:
                self.viewAllOrders()
            elif choice == 4:
                self.Registered_Users()
            elif choice == 5:
                print("Exiting Admin Menu...")
                break
            else:
                print("Invalid choice.")

    def viewAllOrders(self):
        self.cursor.execute(
            "SELECT user_email, medicine_name, quantity FROM orders "
        )
        orders = self.cursor.fetchall()

        if not orders:
            print("No orders found.")
            return

        print("\n--- All Orders ---")
        for user, med, qty in orders:
            print(f"User: {user} | Medicine: {med} | Qty: {qty}")

    def Add_Medicine(self):
        category = input("Enter medicine category \n"
                         "Tablets,Syrup,Injections: ")
        name = input("Enter medicine name: ")
        price = float(input("Enter price: "))
        stock = int(input("Enter stock: "))

        self.cursor.execute("INSERT INTO medicines (category, name, price, stock) VALUES (%s, %s, %s, %s)",
                            (category, name, price, stock))
        self.db.commit()
        print("Medicine added successfully.")

    def home(self):
        print(f"-----> Welcome to {self.name} by  Medikart <-----")
        while True:
            print("\n1. Admin Login\n2. User Login\n3. Register\n4. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.admin_login()
            elif choice == '2':
                self.User_login()
            elif choice == '3':
                self.User_Register()
            elif choice == '4':
                break
            else:
                print("Invalid choice.")


s = MediStore()
s.home()
