import sqlite3
conn = sqlite3.connect("library.db")

conn.execute('''
             CREATE TABLE IF NOT EXISTS books(
             b_id INTEGER PRIMARY KEY,
             bName VARCHAR(50),
             bAuth VARCHAR(30),
             bPrice INT,
             bGenre VARCHAR(20),
             bYear INT)
             ''')
conn.execute('''
             CREATE TABLE IF NOT EXISTS members(
             m_id INTEGER PRIMARY KEY,
             mName VARCHAR(30),
             mPhone INT,
             mDate INT)
             ''')
conn.execute('''
             CREATE TABLE IF NOT EXISTS customers(
             c_id INTEGER PRIMARY KEY,
             cName VARCHAR(30),
             cPhone INT,
             cDOP INT)
             ''')
conn.execute('''
             CREATE TABLE IF NOT EXISTS sales(
             s_id INTEGER PRIMARY KEY,
             b_id INT,
             c_id INT,
             qty INT,
             bPrice INT)
             ''')

def menu():
    while True:
        print("\nLibrary Management System")
        print("1. Add a Book")
        print("2. Update a Book")
        print("3. Delete a Book")
        print("4. Display All Books")
        print("5. Record a Sale")
        print("6. Exit")
        try :
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input, Please enter a number from 1-6")
            continue
        if choice == 1:
            add_book()
        elif choice == 2:
            update_book()
        elif choice == 3:
            delete_book()
        elif choice == 4:
            display_books()
        elif choice == 5:
            record_sale()
        elif choice == 6:
            print("Thank You !")
            break
        else:
            print("Invalid Choice ! ")
        cont_choice = input("\nDo you want to continue? (yes/no): ").lower()
        if cont_choice not in ("yes", "y"):
            print("Thank You !")
            break
            
def display_books():
    data = conn.execute("SELECT * FROM books")
    print("Books available: ")
    for i in data:
        print("Book Id: ",i[0],"  ","Book Name: ",i[1],"  ","Book Author: ",i[2],"  ","Book Price: ",i[3],"  ","Book Genre: ",i[4],"  ","Publication Year: ",i[5])

def add_book():
    n = int(input("Enter the no. of books you want to add: "))
    for i in range(n):
        bName = input("Enter the book name: ")
        bAuth = input("Enter the book author: ")
        bPrice = int(input("Enter the book price: "))
        bGenre = input("Enter the genre: ")
        bYear = int(input("Enter the publication year: "))
        conn.execute("INSERT INTO books (bName, bAuth, bPrice, bGenre, bYear) VALUES (?, ?, ?, ?, ?)", (bName, bAuth, bPrice, bGenre, bYear))
        conn.commit()

def update_book():
    b_id = int(input("enter the book id to update: "))
    data = conn.execute(f"SELECT bName FROM books WHERE b_id='{b_id}'")
    book_name = data.fetchone()

    if book_name:                                   
        print("You are updating:", book_name[0])
        option = input("What to update? (name/author/price/genre/year): ")
        if option == "name" :
            b_name = input("Enter updated book name: ")
            conn.execute(f"UPDATE books SET bName='{b_name}' WHERE b_id='{b_id}'")
        elif option == "author" :
            auth = input("Enter updated author's name: ")
            conn.execute(f"UPDATE books SET bAuth='{auth}' WHERE b_id='{b_id}'")
        elif option == "price" :
            price = int(input("Enter updated book price: "))
            conn.execute(f"UPDATE books SET bPrice='{price}' WHERE b_id='{b_id}'")
        elif option == "genre" :
            genre = input("Enter updated book genre: ")
            conn.execute(f"UPDATE books SET bGenre='{genre}' WHERE b_id='{b_id}'")
        elif option == "year" :
            year = int(input("Enter updated year of publication: "))
            conn.execute(f"UPDATE books SET bYear='{year}' WHERE b_id='{b_id}'")
        else :
            print("Invalid Input")
        conn.commit()
    else:
        print("Book Not Found !")
    
def delete_book():
    b_id = int(input("enter the book id to delete: "))
    data = conn.execute(f"SELECT bName FROM books WHERE b_id='{b_id}'")
    book_name = data.fetchone()
    if book_name:
        print("You are deleting:", book_name[0])
        option = input("Are you sure you want to delete (yes/no): ").lower()
        if option == "yes" or option == "Yes" :
            conn.execute(f"DELETE FROM books WHERE b_id='{b_id}'")
            conn.commit()
        else :
            print("Delete aborted !")
    else :
        print("Book Not Found !")

def record_sale():
    c_id = int(input("Enter the customer ID: "))
    b_id = int(input("Enter the book ID: "))
    qty = int(input("Enter quantity: "))
    price_data = conn.execute(f"SELECT bPrice FROM books WHERE b_id = {b_id}").fetchone()
    
    if price_data:
        bPrice = price_data[0]
        total_price = bPrice * qty
        conn.execute("INSERT INTO sales(b_id, c_id, qty, bPrice) VALUES (?, ?, ?, ?)", 
                     (b_id, c_id, qty, total_price))
        print(f"Sale recorded! Total price: {total_price}")
    else:
        print("Invalid book ID!")

menu()