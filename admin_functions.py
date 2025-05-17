import mysql.connector


def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="AH14@neena",
        database="shoe_shopdb"
    )


# Admin Account Creation
def register_admin():
    connection = create_connection()
    cursor = connection.cursor()
    print("\n--- Create Admin Account ---")
    email = input("Email: ")
    username = input("Username: ")
    password = input("Password: ")
    name = input("Name: ")
    address = input("Address: ")

    cursor.execute("""
        INSERT INTO admin (email, username, password, name, address)
        VALUES (%s, %s, %s, %s, %s)
    """, (email, username, password, name, address))
    connection.commit()
    print("Admin Created Successfully!")
    cursor.close()
    connection.close()


# Admin Login
def admin_login():
    connection = create_connection()
    cursor = connection.cursor()
    print("\n--- Admin Login ---")
    username = input("Username: ")
    password = input("Password: ")

    cursor.execute("""
        SELECT admin_id FROM admin WHERE username=%s AND password=%s
    """, (username, password))
    admin = cursor.fetchone()

    cursor.close()
    connection.close()
    if admin:
        print("Admin Login Successful!")
        return admin[0]
    else:
        print("Invalid Credentials.")
        return None


# View Products
def view_products_admin():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT product_id, name, price, quantity FROM products")
    products = cursor.fetchall()

    print("\n--- All Products ---")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}, Stock: {product[3]}")

    cursor.close()
    connection.close()


# Add Product
def add_product():
    connection = create_connection()
    cursor = connection.cursor()
    print("\n--- Add New Product ---")
    name = input("Product Name: ")
    price = float(input("Price: "))
    quantity = int(input("Quantity: "))
    production_date = input("Production Date (YYYY-MM-DD): ")

    cursor.execute("""
        INSERT INTO products (name, price, quantity, production_date)
        VALUES (%s, %s, %s, %s)
    """, (name, price, quantity, production_date))
    connection.commit()
    print("Product Added Successfully!")
    cursor.close()
    connection.close()


# Remove Product
def remove_product():
    connection = create_connection()
    cursor = connection.cursor()
    product_id = input("Enter Product ID to remove: ")

    cursor.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
    connection.commit()
    print("Product Removed Successfully.")
    cursor.close()
    connection.close()


# Update Stock
def update_stock():
    connection = create_connection()
    cursor = connection.cursor()
    product_id = input("Enter Product ID: ")
    new_stock = int(input("Enter New Stock Quantity: "))

    cursor.execute("""
        UPDATE products SET quantity=%s WHERE product_id=%s
    """, (new_stock, product_id))
    connection.commit()
    print("Stock Updated Successfully!")
    cursor.close()
    connection.close()


# Update Price
def update_price():
    connection = create_connection()
    cursor = connection.cursor()
    product_id = input("Enter Product ID: ")
    new_price = float(input("Enter New Price: "))

    cursor.execute("""
        UPDATE products SET price=%s WHERE product_id=%s
    """, (new_price, product_id))
    connection.commit()
    print("Price Updated Successfully!")
    cursor.close()
    connection.close()


# View Feedback
def view_feedback():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT cust_id, order_id, rating, timestamp FROM feedback
    """)
    feedbacks = cursor.fetchall()

    print("\n--- Customer Feedbacks ---")
    for fb in feedbacks:
        print(f"Customer ID: {fb[0]}, Order ID: {fb[1]}, Rating: {fb[2]}, Time: {fb[3]}")

    cursor.close()
    connection.close()
