from models import SessionLocal, Portfolio

# In-memory fallback storage when DB is not available
memory_portfolios = {}

def update_portfolio(user_id, grams, total_amount):
    try:
        session = SessionLocal()
        portfolio = session.query(Portfolio).filter_by(user_id=user_id).first()

        if not portfolio:
            portfolio = Portfolio(user_id=user_id, gold=0, investment=0)
            session.add(portfolio)

        portfolio.gold += grams
        portfolio.investment += total_amount
        session.commit()
        session.close()
    except Exception as e:
        print(f"Database error, using memory storage: {e}")
        # Fallback to in-memory storage
        if user_id not in memory_portfolios:
            memory_portfolios[user_id] = {"gold": 0, "investment": 0}
        
        memory_portfolios[user_id]["gold"] += grams
        memory_portfolios[user_id]["investment"] += total_amount

def get_portfolio(user_id):
    try:
        session = SessionLocal()
        portfolio = session.query(Portfolio).filter_by(user_id=user_id).first()
        session.close()

        if portfolio:
            return {"gold": portfolio.gold, "investment": portfolio.investment}
        return {"gold": 0, "investment": 0}
    except Exception as e:
        print(f"Database error, using memory storage: {e}")
        # Fallback to in-memory storage
        if user_id not in memory_portfolios:
            memory_portfolios[user_id] = {"gold": 0, "investment": 0}
        return memory_portfolios[user_id]
