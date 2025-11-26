import re
from datetime import datetime
from typing import Optional, Dict, Any

class ParserService:
    def __init__(self):
        # Regex patterns for common transaction formats
        # Example: "Rs. 150.00 spent on Zomato"
        # Example: "Debited Rs 500.00 from A/c ... for UBER"
        self.patterns = [
            r"(?i)(?:rs\.?|inr)\s*([\d,]+\.?\d*)\s*(?:spent|debited|paid)\s*(?:on|to|for)?\s*([a-zA-Z0-9\s]+)",
            r"(?i)(?:spent|paid)\s*(?:rs\.?|inr)\s*([\d,]+\.?\d*)\s*(?:on|to|for)?\s*([a-zA-Z0-9\s]+)",
            r"(?i)transaction\s*of\s*(?:rs\.?|inr)\s*([\d,]+\.?\d*)\s*at\s*([a-zA-Z0-9\s]+)",
        ]

    def parse_email(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extracts transaction details from email text.
        Returns a dictionary with amount, merchant, date, etc.
        """
        # Normalize text
        text = text.replace("\n", " ").strip()
        
        for pattern in self.patterns:
            match = re.search(pattern, text)
            if match:
                amount_str = match.group(1).replace(",", "")
                merchant = match.group(2).strip()
                
                # Basic cleanup of merchant name
                merchant = merchant.split(" on ")[0].split(" using ")[0].strip()
                
                try:
                    amount = float(amount_str)
                except ValueError:
                    continue
                
                return {
                    "amount": amount,
                    "description": merchant,
                    "category": self.predict_category(merchant),
                    "type": "expense", # Default to expense
                    "payment_method": "Unknown", # Could be extracted
                    "date": datetime.utcnow() # Default to now, or extract date
                }
        return None

    def predict_category(self, merchant: str) -> str:
        merchant = merchant.lower()
        if any(x in merchant for x in ["zomato", "swiggy", "food", "restaurant", "cafe"]):
            return "Food"
        if any(x in merchant for x in ["uber", "ola", "rapido", "fuel", "petrol"]):
            return "Travel"
        if any(x in merchant for x in ["amazon", "flipkart", "myntra", "shopping"]):
            return "Shopping"
        if any(x in merchant for x in ["jio", "airtel", "vodafone", "bill", "electricity"]):
            return "Bills"
        return "General"

parser_service = ParserService()
