import requests
import sys

BASE_URL = "http://127.0.0.1:8001/api/v1"

def verify_analytics():
    # Login
    email = "test@example.com"
    password = "password123"
    login_data = {"username": email, "password": password}
    
    r = requests.post(f"{BASE_URL}/login/access-token", data=login_data)
    if r.status_code != 200:
        print(f"Login failed: {r.text}")
        return
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get Dashboard
    print("Fetching Dashboard Data...")
    r = requests.get(f"{BASE_URL}/analytics/dashboard", headers=headers)
    if r.status_code == 200:
        data = r.json()
        print(f"Total Expense: {data['total_expense']}")
        print(f"Total Income: {data['total_income']}")
        print(f"Net Savings: {data['net_savings']}")
        print(f"Category Breakdown: {data['category_breakdown']}")
    else:
        print(f"Dashboard failed: {r.status_code} {r.text}")

if __name__ == "__main__":
    verify_analytics()
