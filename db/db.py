from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:123qweasdZXC@localhost:5432/fastapi")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
