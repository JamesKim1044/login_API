from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import os
from sqlalchemy.engine.url import URL
import pymysql
pymysql.install_as_MySQLdb()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETE_FILE = os.path.join(BASE_DIR, 'secrets.json')

secrets = json.loads(open(SECRETE_FILE).read())

DB = {
    'drivername': 'mariadb',
    'host': secrets['DB']['host'],
    'port': secrets['DB']['port'],
    'username': secrets['DB']['user'],
    'password': secrets['DB']['password'],
    'database': secrets['DB']['database'],
    'query': {'charset':'utf8'}

}

engine = create_engine(URL(**DB), pool_size = 20, max_overflow = 10, pool_recycle=5*60, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        