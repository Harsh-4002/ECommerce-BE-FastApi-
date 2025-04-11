from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



SQLALCHEMY_DB_URL='sqlite:///./product.db'


engine=create_engine(SQLALCHEMY_DB_URL,connect_args={
    "check_same_thread":False
})

SessionLocal =sessionmaker(bind=engine,autocommit=False,autoflush=False)
Base=declarative_base()

def get_dB():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close() 