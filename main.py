from customer_functions import *
from admin_functions import *


def customer_menu(cust_id):
    while True:
        print("\n--- Customer Menu ---")
        print("1. View Products")
        print("2. View Shopping History")
        print("3. Add to Cart")
        print("4. View Cart")
        print("5. Checkout")
        print("6. Rate a Product")
        print("7. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_products()
        elif choice == "2":
            view_shopping_history(cust_id)
        elif choice == "3":
            product_id = int(input("Enter Product ID to add: "))
            quantity = int(input("Enter Quantity: "))
            add_to_cart(cust_id, product_id, quantity)
        elif choice == "4":
            view_cart(cust_id)
        elif choice == "5":
            checkout(cust_id)
        elif choice == "6":
            rate_product(cust_id)
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")


def admin_menu(admin_id):
    while True:
        print("\n--- Admin Menu ---")
        print("1. View Products")
        print("2. Add Product")
        print("3. Remove Product")
        print("4. Update Stock")
        print("5. Update Price")
        print("6. View Feedback")
        print("7. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_products_admin()
        elif choice == "2":
            add_product()
        elif choice == "3":
            remove_product()
        elif choice == "4":
            update_stock()
        elif choice == "5":
            update_price()
        elif choice == "6":
            view_feedback()
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")


def main():
    while True:
        print("\n=== Shoe Shop Management System ===")
        print("1. Customer Login")
        print("2. Customer Register")
        print("3. Admin Login")
        print("4. Admin Register")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            cust_id = customer_login()
            if cust_id:
                customer_menu(cust_id)
        elif choice == "2":
            register_customer()
        elif choice == "3":
            admin_id = admin_login()
            if admin_id:
                admin_menu(admin_id)
        elif choice == "4":
            register_admin()
        elif choice == "5":
            print("Exiting System. Thank you!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
