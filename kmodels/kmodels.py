from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.schema import FetchedValue 

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    color = Column(String(80))
    title = Column(String(800), nullable=False)
    description = Column(Text, nullable=False)
    
class Category(db.Model):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    name = Column(String(100), nullable=False)
    fullname = Column(Text, nullable=False)