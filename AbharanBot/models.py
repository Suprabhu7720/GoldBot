from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_URL

Base = declarative_base()

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    gold = Column(Float, default=0.0)
    investment = Column(Float, default=0.0)

# DB setup
print("Creating engine...")
print(DB_URL)
engine = create_engine(
    DB_URL,
    pool_timeout=20,
    pool_recycle=3600,
    connect_args={"connect_timeout": 10}
)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    print("Initializing DB...")
    try:
        # Test connection first
        print("Testing database connection...")
        with engine.connect() as connection:
            from sqlalchemy import text
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful")
        
        # Create tables
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("⚠️ Running without database - using in-memory storage")
        # Don't raise the exception - let the app continue without DB
        return False
    return True
