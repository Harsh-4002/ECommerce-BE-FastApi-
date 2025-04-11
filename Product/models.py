from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from database import Base
# create tables and attributes mainly connected with database
class Product(Base):
    __tablename__='products'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    description=Column(String)
    price=Column(Integer)
    seller_id=Column(Integer,ForeignKey('sellers.id'))
    seller=relationship('Seller',back_populates='products')



class Seller(Base):
    __tablename__='sellers'
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String)
    email=Column(String)
    password=Column(String)
    products=relationship('Product',back_populates='seller')