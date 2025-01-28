from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)

    orders = relationship("Order", back_populates="distributor")
    notifications = relationship("Notification", back_populates="user")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    item_description = Column(String(100))
    qty = Column(Integer)
    mrp = Column(Float)
    discount = Column(Float)
    after_discount = Column(Float)
    total = Column(Float)
    order_date = Column(DateTime, default=datetime.utcnow)
    client_name = Column(String(100))
    salon_name = Column(String(100))
    contact = Column(String(50))
    address = Column(String(200))
    distributor_id = Column(Integer, ForeignKey('users.id'))

    distributor = relationship("User", back_populates="orders")

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(String(200))
    is_read = Column(Integer, default=0)  # 0 for unread, 1 for read
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")

# Database connection
engine = create_engine('sqlite:///salon_orders.db')
Base.metadata.create_all(engine)
