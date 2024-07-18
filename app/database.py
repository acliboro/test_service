from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://sidservice:pass1234@casfs-plus-node-prod-ph-amiel-liboro-fastapi.cnp5tdzehhhs.us-east-2.rds.amazonaws.com/fastapi'
SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://amiel:pass1234@postgres:5432/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()