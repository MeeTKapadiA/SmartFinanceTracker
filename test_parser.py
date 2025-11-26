from app.services.parser_service import parser_service

def test_parser():
    samples = [
        "Rs. 150.00 spent on Zomato for lunch",
        "Debited Rs 500.00 from A/c 1234 for UBER",
        "Transaction of INR 1,200.50 at Amazon India",
        "Paid Rs. 200 to Swiggy",
        "No transaction here"
    ]
    
    print("Testing Parser Logic:")
    for sample in samples:
        result = parser_service.parse_email(sample)
        print(f"Input: {sample}")
        if result:
            print(f"Output: {result['amount']} - {result['description']} ({result['category']})")
        else:
            print("Output: No match")
        print("-" * 20)

if __name__ == "__main__":
    test_parser()
