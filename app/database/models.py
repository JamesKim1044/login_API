from pydantic import BaseModel, Field
from sqlalchemy import BIGINT, TEXT, Boolean, Column, ForeignKey, Integer, String, UniqueConstraint, false, DateTime
from .database import Base
import datetime

class User(Base):
    __tablename__ = "studio_user"

    account_id = Column(Integer, primary_key = True, index = True)
    user_id = Column(String(16), unique = True, index = True)
    password = Column(String(100))
    key = Column(String(10))
    
    create_dt = Column(DateTime, default = datetime.datetime.now())
    last_mod_dt = Column(DateTime, default = datetime.datetime.now())

class Project(Base):
    __tablename__ = "studio_project"
    project_id = Column(Integer, primary_key= True, index=True)
    
    article_id = Column(Integer, ForeignKey("medicon_article.article_id"))
    account_id = Column(Integer, ForeignKey("studio_user.account_id"))
    project_key = Column(String(10), unique= True) 
    
    project_title = Column(String(20))
    article_title = Column(String(200))
    journal_title = Column(String(200))
    authors = Column(String(500))
    corresp = Column(String(100))
    keywords = Column(String(300))
    abstract = Column(TEXT)
    images = Column(TEXT)
    
    create_dt = Column(DateTime, default= datetime.datetime.now())
    last_mod_dt = Column(DateTime, default=datetime.datetime.now()) 
       
class Metadata(Base):
    __tablename__ = "medicon_article"
    article_id = Column(Integer, primary_key = True, index = True)
    
    article_title = Column(String(500))
    journal_title = Column(String(500))
    authors = Column(TEXT)
    corresp = Column(String(200))
    published = Column(String(200))
    publication = Column(String(200))
    doi = Column(String(500), unique = True)
    copyright = Column(String(500))
    keywords = Column(TEXT)
    abstract = Column(TEXT)
    images = Column(TEXT)
    
    create_dt = Column(DateTime, default=datetime.datetime.now()) 
    last_mod_dt = Column(DateTime, default=datetime.datetime.now()) 
       
