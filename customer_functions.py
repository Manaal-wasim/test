import mysql.connector
from datetime import datetime


def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="AH14@neena",
        database="shoe_shopdb"
    )


# Customer Account Creation
def register_customer():
    connection = create_connection()
    cursor = connection.cursor()
    print("\n--- Create New Account ---")
    name = input("Name: ")
    phone = input("Phone: ")
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    address = input("Address: ")

    cursor.execute("""
        INSERT INTO customers (name, phone_no, username, password, email, address)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, phone, username, password, email, address))
    connection.commit()
    print("Account Created Successfully!")
    cursor.close()
    connection.close()


# Customer Login
def customer_login():
    connection = create_connection()
    cursor = connection.cursor()
    print("\n--- Customer Login ---")
    username = input("Username: ")
    password = input("Password: ")

    cursor.execute("""
        SELECT cust_id FROM customers WHERE username=%s AND password=%s
    """, (username, password))
    user = cursor.fetchone()

    cursor.close()
    connection.close()
    if user:
        print("Login Successful!")
        return user[0]
    else:
        print("Invalid Credentials.")
        return None


# View Products
def view_products():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT product_id, name, price, quantity FROM products")
    products = cursor.fetchall()

    print("\n--- Available Products ---")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}, Stock: {product[3]}")

    cursor.close()
    connection.close()


# Add to Cart
def add_to_cart(cust_id, product_id, quantity):
    connection = create_connection()
    cursor = connection.cursor()

    # Check if product exists and stock is available
    cursor.execute("SELECT price, quantity FROM products WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()

    if product and product[1] >= quantity:
        price = product[0]
        total_price = price * quantity
        cursor.execute("""
            INSERT INTO shopping_cart (cust_id, product_id, quantity, total_price)
            VALUES (%s, %s, %s, %s)
        """, (cust_id, product_id, quantity, total_price))
        connection.commit()
        print("Product added to cart!")
    else:
        print("Not enough stock available.")

    cursor.close()
    connection.close()


# View Cart
def view_cart(cust_id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT product_id, quantity, total_price FROM shopping_cart WHERE cust_id=%s
    """, (cust_id,))
    items = cursor.fetchall()

    print("\n--- Your Cart ---")
    for item in items:
        print(f"Product ID: {item[0]}, Quantity: {item[1]}, Total: {item[2]}")

    cursor.close()
    connection.close()


# Checkout
def checkout(cust_id):
    connection = create_connection()
    cursor = connection.cursor()

    address = input("Enter Shipping Address: ")
    payment_status = "Paid"
    order_status = "Processing"
    order_date = datetime.now()

    # Insert order
    cursor.execute("""
        INSERT INTO orders (cust_id, order_date, payment_status, order_status, shipping_address)
        VALUES (%s, %s, %s, %s, %s)
    """, (cust_id, order_date, payment_status, order_status, address))
    order_id = cursor.lastrowid

    # Move cart items to order
    cursor.execute("""
        SELECT product_id, quantity FROM shopping_cart WHERE cust_id=%s
    """, (cust_id,))
    cart_items = cursor.fetchall()

    for product_id, quantity in cart_items:
        cursor.execute("""
            INSERT INTO shopping_history (cust_id, order_id, order_details, purchase_date)
            VALUES (%s, %s, %s, %s)
        """, (cust_id, order_id, f"Product {product_id}, Quantity {quantity}", order_date))

        # Update product stock
        cursor.execute("""
            UPDATE products SET quantity = quantity - %s WHERE product_id = %s
        """, (quantity, product_id))

    # Empty the cart
    cursor.execute("""
        DELETE FROM shopping_cart WHERE cust_id=%s
    """, (cust_id,))

    connection.commit()
    print("Order Placed Successfully!")
    cursor.close()
    connection.close()


# View Shopping History
def view_shopping_history(cust_id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT order_id, order_details, purchase_date FROM shopping_history WHERE cust_id=%s
    """, (cust_id,))
    history = cursor.fetchall()

    print("\n--- Shopping History ---")
    for item in history:
        print(f"Order ID: {item[0]}, Details: {item[1]}, Date: {item[2]}")

    cursor.close()
    connection.close()


# Rate a Product (only if purchased)

def rate_product(cust_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT o.order_id, p.product_id, p.name
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            WHERE o.cust_id = %s
        """, (cust_id,))
        orders = cursor.fetchall()

        if not orders:
            print("You haven't purchased any products yet.")
            return

        print("\nYour Orders:")
        for order in orders:
            print(f"Order ID: {order[0]}, Product ID: {order[1]}, Product: {order[2]}")

        order_id = int(input("Enter Order ID to rate: "))
        valid_ids = [o[0] for o in orders]
        if order_id not in valid_ids:
            print("Invalid Order ID.")
            return

        rating = int(input("Enter Rating (1–5): "))
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5.")
            return

        timestamp = datetime.now()

        cursor.execute("""
            INSERT INTO feedback (cust_id, order_id, rating, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (cust_id, order_id, rating, timestamp))
        connection.commit()
        print("Feedback Submitted.")

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
