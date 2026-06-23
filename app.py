from modules import *

def main_menu():
    """Display main menu and handle user options."""
    while True:
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        print("=" * 50)
        
        option = input("Choose an option (1-3): ").strip()
        
        if option == "1":
            account_creation()
        elif option == "2":
            login_menu()
        elif option == "3":
            print("\nThank you for using Apụnanwụ Bank. Goodbye!")
            break
        else:
            print(" Invalid option! Please choose 1, 2, or 3.")

def login_menu():
    """Handle login and display user menu."""
    username = login()
    
    if username is None:
        return
    
    user_logged_in = True
    while user_logged_in:
        print("\n" + "=" * 50)
        print(f"ACCOUNT MENU - {username}")
        print("=" * 50)
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Transfer Funds")
        print("4. View Account Details")
        print("5. Generate Bank Statement")
        print("6. Logout")
        print("=" * 50)
        
        option = input("Choose an option (1-6): ").strip()
        
        if option == "1":
            deposit_money(username)
        elif option == "2":
            withdraw_money(username)
        elif option == "3":
            transfer_funds(username)
        elif option == "4":
            view_account_details(username)
        elif option == "5":
            generate_statement(username)
        elif option == "6":
            print(f"\nLogged out successfully. Thank you, {username}!")
            user_logged_in = False
        else:
            print(" Invalid option! Please choose 1-6.")

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("WELCOME TO APỤNANWỤ BANK")
    print("=" * 50)
    main_menu()