import mysql.connector
# import getpass

class Library:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ajay",
            database="project1"
        )
        self.cursor = self.db.cursor()
        self.name = "Knowledge"
        self.var1 = ""
        self.var2 = ""
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name VARCHAR(100),
            password VARCHAR(100),
            email VARCHAR(100) UNIQUE
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            section VARCHAR(100),
            title VARCHAR(255)
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowed_books (
            book_title VARCHAR(255),
            borrowed_by VARCHAR(100)
        )""")
        self.db.commit()

    def regi(self):
        name = input("Enter your name to register : ")
        if name.isdigit():
            print("  x-x-x-x  print valid name  x-x-x-x  ")
            return
        mail = input("Enter your E-mail :")
        if "@gmail.com" not in mail:
            print("  x-x-x-x  Enter valid E-mail  x-x-x-x  ")
            return
        self.cursor.execute("SELECT * FROM users WHERE email = %s", (mail,))
        if self.cursor.fetchone():
            print("  x-x-x-x  This E-mail is already registered  x-x-x-x  ")
            return
        password = ("Create password : ")
        self.cursor.execute("INSERT INTO users (name, password, email) VALUES (%s, %s, %s)", (name, password, mail))
        self.db.commit()
        print("Your registration completed successfully.")

    def librarian_login(self):
        self.var1 = input("Enter your name : ")
        if self.var1.lower() == "ajay":
            password = "Enter password : "
            if password == "1234":
                print("----->| Welcome librarian |<-----")
                while True:
                    print("....................")
                    print("\n1.DisplayBook \n2.AddBook \n3.DeleteBook  \n4.BorrowedBook \n5.Users  \n6:exit ")
                    print("....................")
                    choice2 = input("Enter your choice : ")
                    if choice2 == "1":
                        self.displayBooks()
                    elif choice2 == "2":
                        self.addBook()
                    elif choice2 == "3":
                        self.deleteBook()
                    elif choice2 == "4":
                        self.cursor.execute("SELECT * FROM borrowed_books")
                        records = self.cursor.fetchall()
                        if not records:
                            print("No one borrowed a book")
                        else:
                            for record in records:
                                print(record)
                    elif choice2 == "5":
                        self.cursor.execute("SELECT name FROM users")
                        for user in self.cursor.fetchall():
                            print(user[0])
                    elif choice2 == "6":
                        break
                    else:
                        print("  x-x-x-x  Enter valid choice  x-x-x-x  ")
            else:
                print("  x-x-x-x  Incorrect Password  x-x-x-x  ")
        else:
            print("  x-x-x-x  Enter valid name   x-x-x-x  ")

    def user_login(self):
        mail = input("Enter your Gmail : ")
        if "@gmail.com" not in mail:
            print("  x-x-x-x  Enter valid E-mail  x-x-x-x  ")
            return
        self.cursor.execute("SELECT name, password FROM users WHERE email=%s", (mail,))
        result = self.cursor.fetchone()
        if result:
            self.var2 = result[0]
            password = ("Enter password : ")
            if password == result[1]:
                print(f"----->| Welcome {self.var2} |<-----")
                while True:
                    print("....................")
                    print("1:DisplayBook  \n2:BorrowBook  \n3.ReturnBook \n4:exit ")
                    print("....................")
                    choice1 = input("Enter your choice : ")
                    if choice1 == "1":
                        self.displayBooks()
                    elif choice1 == "2":
                        self.BorrowBook()
                    elif choice1 == "3":
                        self.returnBook()
                    elif choice1 == "4":
                        print("Thank you for visiting the library")
                        break
                    else:
                        print("  x-x-x-x  Enter valid choice  x-x-x-x   ")
            else:
                print("  x-x-x-x  Incorrect Password   x-x-x-x  ")
        else:
            print("  x-x-x-x  Email not registered  x-x-x-x  ")

    def displayBooks(self):
        self.cursor.execute("SELECT DISTINCT section FROM books")
        sections = [s[0] for s in self.cursor.fetchall()]
        for i, section in enumerate(sections, start=1):
            print(f"{i}. {section}")
        choice = input("Select section: ")
        if choice.isdigit() and 1 <= int(choice) <= len(sections):
            section = sections[int(choice) - 1]
            self.cursor.execute("SELECT title FROM books WHERE section=%s", (section,))
            books = self.cursor.fetchall()
            for book in books:
                print("-->", book[0])
        else:
            print("  x-x-x-x  Enter valid choice  x-x-x-x  ")

    def BorrowBook(self):
        self.displayBooks()
        section = input("Enter section: ")
        book = input("Enter book name: ")
        self.cursor.execute("SELECT title FROM books WHERE section=%s AND title=%s", (section, book))
        if self.cursor.fetchone():
            self.cursor.execute("SELECT * FROM borrowed_books WHERE book_title=%s", (book,))
            if self.cursor.fetchone():
                print("Book is already being used.")
            else:
                self.cursor.execute("DELETE FROM books WHERE section=%s AND title=%s", (section, book))
                self.cursor.execute("INSERT INTO borrowed_books (book_title, borrowed_by) VALUES (%s, %s)", (book, self.var2))
                self.db.commit()
                print(f"You can take the {book} book now")
        else:
            print("  x-x-x-x  There is no book available with this name in section  x-x-x-x  ")

    def returnBook(self):
        section = input("Enter section to return book to: ")
        book = input("Enter book name: ")
        self.cursor.execute("SELECT * FROM borrowed_books WHERE book_title=%s AND borrowed_by=%s", (book, self.var2))
        if self.cursor.fetchone():
            self.cursor.execute("INSERT INTO books (section, title) VALUES (%s, %s)", (section, book))
            self.cursor.execute("DELETE FROM borrowed_books WHERE book_title=%s", (book,))
            self.db.commit()
            print("Your book has been returned successfully")
        else:
            print("  x-x-x-x You have not borrowed this book  x-x-x-x  ")

    def addBook(self):
        section = input("Enter section: ")
        book = input("Enter book name: ")
        self.cursor.execute("SELECT * FROM books WHERE section=%s AND title=%s", (section, book))
        if self.cursor.fetchone():
            print("  x-x-x-x  Book already exists  x-x-x-x  ")
        else:
            self.cursor.execute("INSERT INTO books (section, title) VALUES (%s, %s)", (section, book))
            self.db.commit()
            print("Book has been added to the library")

    def deleteBook(self):
        section = input("Enter section: ")
        book = input("Enter book name: ")
        self.cursor.execute("SELECT * FROM books WHERE section=%s AND title=%s", (section, book))
        if self.cursor.fetchone():
            self.cursor.execute("DELETE FROM books WHERE section=%s AND title=%s", (section, book))
            self.db.commit()
            print("Book has been removed from the library")
        else:
            print("  x-x-x-x  Book not found  x-x-x-x  ")

    def home(self):
        print(f"\n----->|  Welcome to {self.name} library  |<-----")
        while True:
            print("....................")
            print("1:librarian_Login \n2:User_login \n3:Register \n4.exit")
            print("....................")
            choice = input("Enter your choice : ")
            if choice == "1":
                self.librarian_login()
            elif choice == "2":
                self.user_login()
            elif choice == "3":
                self.regi()
            elif choice == "4":
                break
            else:
                print("  x-x-x-x  Enter valid choice  x-x-x-x   ")
s = Library()
s.home()
