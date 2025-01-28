from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Order Table
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    item_description = Column(String)
    qty = Column(Integer)
    mrp = Column(Float)
    discount = Column(Float)
    after_discount = Column(Float)
    total = Column(Float)
    order_date = Column(DateTime)
    client_name = Column(String)
    salon_name = Column(String)
    contact = Column(String)
    address = Column(String)

# Subordinate Table
class Subordinate(Base):
    __tablename__ = 'subordinates'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)

# Notification Table
class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    subordinate_id = Column(Integer)
    message = Column(String)
    is_read = Column(Boolean, default=False)
    timestamp = Column(DateTime)

# Create an engine and session
engine = create_engine('sqlite:///salon_orders.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)
