from flask import Flask, request
from utils.twilio_helper import send_message
from services.gold_service import get_gold_price
from services.payment_service import create_payment_link
from services.portfolio_service import update_portfolio, get_portfolio
from models import init_db

app = Flask(__name__)

# Initialize DB
db_connected = init_db()

# Temporary session memory (can move to Redis later)
user_sessions = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip().lower()
    from_number = request.values.get("From", "")
    user_id = from_number

    if user_id not in user_sessions:
        user_sessions[user_id] = {"state": "menu"}

    state = user_sessions[user_id]["state"]

    # MAIN MENU
    if incoming_msg in ["hi", "hello", "menu"]:
        user_sessions[user_id]["state"] = "menu"
        return send_message(
            "Hello! 👋 What would you like to do?",
            ["Buy Gold", "Buy Scheme", "Check Portfolio"]
        )

    # BUY GOLD FLOW
    if incoming_msg == "buy gold" and state == "menu":
        gold_price = get_gold_price()
        user_sessions[user_id]["state"] = "awaiting_grams"
        user_sessions[user_id]["gold_price"] = gold_price
        return send_message(f"💰 Current Gold Price: ₹{gold_price}/gm\n\nHow many grams do you want to buy?")

    elif state == "awaiting_grams":
        try:
            grams = float(incoming_msg)
            gold_price = user_sessions[user_id]["gold_price"]
            total_amount = grams * gold_price
            user_sessions[user_id].update({"grams": grams, "amount": total_amount, "state": "payment"})
            payment_link = create_payment_link(total_amount, user_id)
            return send_message(
                f"You are buying {grams} gm for ₹{total_amount}.\n\nComplete payment here: {payment_link}\n\nType 'paid' after payment."
            )
        except ValueError:
            return send_message("❌ Please enter a valid number of grams.")

    # MOCK PAYMENT SUCCESS
    if incoming_msg == "paid" and state == "payment":
        grams = user_sessions[user_id]["grams"]
        amount = user_sessions[user_id]["amount"]
        update_portfolio(user_id, grams, amount)
        user_sessions[user_id]["state"] = "menu"
        return send_message(f"✅ Payment successful!\n{grams} gm added to your portfolio.\nType 'menu' for options.")

    # PORTFOLIO CHECK
    if incoming_msg == "check portfolio":
        portfolio = get_portfolio(user_id)
        return send_message(f"📊 Your Portfolio:\nGold: {portfolio['gold']} gm\nInvestment: ₹{portfolio['investment']}")

    return send_message("❓ I didn't understand that. Type 'menu' to see options.")

if __name__ == "__main__":
    print("Starting server...")
    app.run(port=5000, debug=True)
    print("Server started")
