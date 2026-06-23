import random
import json
import os
import stdiomask
from datetime import datetime

ACCOUNTS_FILE = "accounts.json"

# Password Validation
def validate_password(password):
    """
    Validate password strength.
    Requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 digit
    - At least 1 special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least 1 uppercase letter."
    if not any(char.islower() for char in password):
        return False, "Password must contain at least 1 lowercase letter."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least 1 digit."
    if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?" for char in password):
        return False, "Password must contain at least 1 special character (!@#$%^&* etc)."
    return True, "Password is strong."

# File Management
def load_accounts():
    """Load accounts from JSON file."""
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_accounts(accounts):
    """Save accounts to JSON file."""
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts, f, indent=4)

def account_exists(username):
    """Check if username already exists."""
    accounts = load_accounts()
    return username in accounts

# Initial Greeting
def greeting(start=1):
    count = start
    while True:
        yield f"user{count:06d}"
        count += random.randint(1, 9999)

# Welcome Greeting
def welcome(username):
    """Display welcome message for returning user."""
    print(f"\nWelcome back to Apụnanwụ Bank, {username}!")

# Account Creation
def account_creation():
    """Create a new bank account."""
    print("\n" + "=" * 40)
    print("CREATE NEW ACCOUNT")
    print("=" * 40)
    
    accounts = load_accounts()
    
    fname = str(input("First Name: ")).strip().capitalize()
    lname = str(input("Last Name: ")).strip().capitalize()
    
    username = input("Create username: ").lower()
    
    if account_exists(username):
        print("Username already exists! Please try a different username.")
        return False
    
    while True:
        password = stdiomask.getpass("Create password: ")
        is_valid, message = validate_password(password)
        
        if is_valid:
            confirm_password = stdiomask.getpass("Confirm password: ")
            if password == confirm_password:
                break
            else:
                print("Passwords don't match. Try again.")
        else:
            print(f"{message}")
    
    # Create new account
    accounts[username] = {
        "first_name": fname,
        "last_name": lname,
        "password": password,
        "balance": 0.0,
        "transactions": [
            {"type": "ACCOUNT_CREATED", "amount": 0, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        ]
    }
    
    save_accounts(accounts)
    print(f"\nAccount created successfully! Welcome, {fname}!")
    return True

# Login
def login():
    """Login to existing account."""
    print("\n" + "=" * 40)
    print("LOGIN")
    print("=" * 40)
    
    accounts = load_accounts()
    attempts = 0
    
    while attempts < 3:
        username = input("Username: ").lower()
        
        if username not in accounts:
            print("Username not found!")
            attempts += 1
            continue
        
        password = stdiomask.getpass("Password: ")
        
        if accounts[username]["password"] == password:
            print(f"\nLogin successful! Welcome, {accounts[username]['first_name']}!")
            return username
        else:
            print("Incorrect password!")
            attempts += 1
            
        if attempts == 3:
            print("Too many failed login attempts!")
            break
    
    return None

# Deposit Money
def deposit_money(username):
    """Deposit money into account."""
    print("\n" + "=" * 40)
    print("DEPOSIT MONEY")
    print("=" * 40)
    
    accounts = load_accounts()
    
    try:
        amount = float(input("Enter amount to deposit (₦): "))
        if amount <= 0:
            print("Amount must be greater than zero!")
            return
        
        accounts[username]["balance"] += amount
        accounts[username]["transactions"].append({
            "type": "DEPOSIT",
            "amount": amount,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        save_accounts(accounts)
        print(f"Successfully deposited ₦{amount:,.2f}")
        print(f"New Balance: ₦{accounts[username]['balance']:,.2f}")
    except ValueError:
        print("Invalid amount! Please enter a number.")

# Withdraw Money
def withdraw_money(username):
    """Withdraw money from account."""
    print("\n" + "=" * 40)
    print("WITHDRAW MONEY")
    print("=" * 40)
    
    accounts = load_accounts()
    current_balance = accounts[username]["balance"]
    
    try:
        amount = float(input("Enter amount to withdraw (₦): "))
        if amount <= 0:
            print("Amount must be greater than zero!")
            return
        
        if amount > current_balance:
            print(f"Insufficient funds! Your balance: ₦{current_balance:,.2f}")
            return
        
        accounts[username]["balance"] -= amount
        accounts[username]["transactions"].append({
            "type": "WITHDRAWAL",
            "amount": amount,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        save_accounts(accounts)
        print(f"Successfully withdrawn ₦{amount:,.2f}")
        print(f"New Balance: ₦{accounts[username]['balance']:,.2f}")
    except ValueError:
        print("Invalid amount! Please enter a number.")

# Transfer Funds
def transfer_funds(username):
    """Transfer funds to another account."""
    print("\n" + "=" * 40)
    print("TRANSFER FUNDS")
    print("=" * 40)
    
    accounts = load_accounts()
    current_balance = accounts[username]["balance"]
    
    recipient = input("Enter recipient username: ").lower()
    
    if recipient == username:
        print("Cannot transfer to your own account!")
        return
    
    if recipient not in accounts:
        print("Recipient account not found!")
        return
    
    try:
        amount = float(input("Enter amount to transfer (₦): "))
        if amount <= 0:
            print("Amount must be greater than zero!")
            return
        
        if amount > current_balance:
            print(f"Insufficient funds! Your balance: ₦{current_balance:,.2f}")
            return
        
        # Process transfer
        accounts[username]["balance"] -= amount
        accounts[recipient]["balance"] += amount
        
        accounts[username]["transactions"].append({
            "type": "TRANSFER_SENT",
            "recipient": recipient,
            "amount": amount,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        accounts[recipient]["transactions"].append({
            "type": "TRANSFER_RECEIVED",
            "sender": username,
            "amount": amount,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        save_accounts(accounts)
        print(f"Successfully transferred ₦{amount:,.2f} to {accounts[recipient]['first_name']} {accounts[recipient]['last_name']}")
        print(f"Your new balance: ₦{accounts[username]['balance']:,.2f}")
    except ValueError:
        print("Invalid amount! Please enter a number.")

# View Account Details
def view_account_details(username):
    """Display account details."""
    accounts = load_accounts()
    account = accounts[username]
    
    print("\n" + "=" * 40)
    print("ACCOUNT DETAILS")
    print("=" * 40)
    print(f"Name: {account['first_name']} {account['last_name']}")
    print(f"Username: {username}")
    print(f"Current Balance: ₦{account['balance']:,.2f}")
    print("=" * 40)

# Generate Bank Statement
def generate_statement(username):
    """Generate transaction summary."""
    accounts = load_accounts()
    account = accounts[username]
    
    print("\n" + "=" * 50)
    print(f"ACCOUNT STATEMENT - {account['first_name']} {account['last_name']}")
    print("=" * 50)
    print(f"Username: {username}")
    print(f"Current Balance: ₦{account['balance']:,.2f}")
    print("\nTransaction History:")
    print("-" * 50)
    
    if account['transactions']:
        for i, transaction in enumerate(account['transactions'], 1):
            trans_type = transaction['type']
            timestamp = transaction['timestamp']
            
            if trans_type == "ACCOUNT_CREATED":
                print(f"{i}. {timestamp} - Account Created")
            elif trans_type == "DEPOSIT":
                print(f"{i}. {timestamp} - DEPOSIT: ₦{transaction['amount']:,.2f}")
            elif trans_type == "WITHDRAWAL":
                print(f"{i}. {timestamp} - WITHDRAWAL: ₦{transaction['amount']:,.2f}")
            elif trans_type == "TRANSFER_SENT":
                print(f"{i}. {timestamp} - TRANSFER SENT to {transaction['recipient']}: ₦{transaction['amount']:,.2f}")
            elif trans_type == "TRANSFER_RECEIVED":
                print(f"{i}. {timestamp} - TRANSFER RECEIVED from {transaction['sender']}: ₦{transaction['amount']:,.2f}")
    else:
        print("No transactions yet.")
    
    print("-" * 50)