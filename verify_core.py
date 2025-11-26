import requests
import sys

BASE_URL = "http://127.0.0.1:8001/api/v1"

def verify_core():
    # 1. Health Check
    try:
        r = requests.get("http://127.0.0.1:8001/health")
        if r.status_code != 200:
            print(f"Health check failed: {r.status_code} {r.text}")
            return
        print("Health check passed")
    except Exception as e:
        print(f"Server not running? {e}")
        return

    # 2. Register User
    email = "test@example.com"
    password = "password123"
    user_data = {
        "email": email,
        "password": password,
        "full_name": "Test User"
    }
    
    # Check if user exists or create
    # For simplicity in this script, we'll try to login first, if fail then register
    
    token = None
    
    print("Attempting login...")
    login_data = {"username": email, "password": password}
    r = requests.post(f"{BASE_URL}/login/access-token", data=login_data)
    
    if r.status_code == 200:
        token = r.json()["access_token"]
        print("Login successful")
    else:
        print("Login failed, attempting registration...")
        r = requests.post(f"{BASE_URL}/users/", json=user_data)
        if r.status_code == 200:
            print("Registration successful")
            # Login again
            r = requests.post(f"{BASE_URL}/login/access-token", data=login_data)
            token = r.json()["access_token"]
            print("Login successful after registration")
        else:
            print(f"Registration failed: {r.text}")
            return

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create Transaction
    print("Creating transaction...")
    tx_data = {
        "amount": 150.0,
        "category": "Food",
        "description": "Lunch at Cafe",
        "type": "expense",
        "payment_method": "UPI"
    }
    r = requests.post(f"{BASE_URL}/transactions/", json=tx_data, headers=headers)
    if r.status_code == 200:
        print("Transaction created")
    else:
        print(f"Transaction creation failed: {r.text}")
        return

    # 4. List Transactions
    print("Listing transactions...")
    r = requests.get(f"{BASE_URL}/transactions/", headers=headers)
    if r.status_code == 200:
        txs = r.json()
        print(f"Found {len(txs)} transactions")
        print(txs)
    else:
        print(f"List transactions failed: {r.text}")

if __name__ == "__main__":
    verify_core()
