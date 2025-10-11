from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace with your actual DB connection string:
# For MySQL:
# DATABASE_URL = "mysql+pymysql://username:password@host/dbname"
# For Supabase (Postgres):
# DATABASE_URL = "postgresql+psycopg2://username:password@host:5432/postgres"

DATABASE_URL = "sqlite:///./test.db"  # ✅ temporary local DB so you can test

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()