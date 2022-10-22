from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import env_vars

PG_USERNAME = env_vars.PG_USERNAME
PG_PASSWORD = env_vars.PG_PASSWORD
PG_HOSTNAME = env_vars.PG_HOSTNAME
PG_DB_NAME = env_vars.PG_DB_NAME

SQLALCHEMY_DATABASE_URL = \
    f"postgresql://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOSTNAME}/{PG_DB_NAME}"

engine = create_engine(url=SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
