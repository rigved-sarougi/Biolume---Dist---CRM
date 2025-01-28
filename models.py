from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base  # Assuming you're using a Base class for SQLAlchemy

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_description = Column(String, nullable=False)
    qty = Column(Integer, nullable=False)
    mrp = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    after_discount = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    
    # New field for distributor assignment
    distributor_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationship with User (Distributor)
    distributor = relationship("User", back_populates="orders")
    
    client_name = Column(String, nullable=False)
    salon_name = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    address = Column(String, nullable=False)


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    
    # Relationship with Order
    orders = relationship("Order", back_populates="distributor")
