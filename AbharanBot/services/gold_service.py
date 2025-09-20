import requests
from config import GOLD_PRICE_API

def get_gold_price():
    try:
        response = requests.get(GOLD_PRICE_API, timeout=5)
        if response.status_code == 200:
            # Example API returns [{"metal":"gold","currency":"USD","price":1920.55,"timestamp":...}]
            data = response.json()
            gold_price_usd = data[0]["price"]
            inr_rate = 83  # mock conversion USD→INR
            return round(gold_price_usd * inr_rate / 31.1, 2)  # per gram in INR
    except Exception as e:
        print("Error fetching gold price:", e)
    return 6000.0  # fallback mock price per gram
