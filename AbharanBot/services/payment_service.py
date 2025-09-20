def create_payment_link(amount, user_id):
    # TODO: integrate Razorpay/Stripe
    # For now, return a mock link
    return f"https://payments.example.com/pay?user={user_id}&amount={amount}"
