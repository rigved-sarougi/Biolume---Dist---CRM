import streamlit as st
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User, Order, Notification, OrderDetail  # Assuming models are updated accordingly

# Set up SQLAlchemy session
engine = create_engine('sqlite:///salon_orders.db')
Session = sessionmaker(bind=engine)
session = Session()

# List of available products
products = [
    "5 Step Facial - Radiance Revival",
    "5 Step Facial - Derma Lumin",
    "5 Step Facial - Cobalin B12",
    "5 Step Facial - Mucin Glow",
    "De Tan Single Use - 12 Gms (10 Pcs)",
    "4 Step Cleanup - Gold Sheen",
    "4 Step Cleanup - Aqua Splash",
    "4Step CleanUp - Charcoal Splash",
    "4 Step Cleanup - Acne Heel",
    "4 Step Cleanup - Radiat Youth"
]

# Register Order (Updated to handle multiple products)
def register_order():
    st.header("Register New Order")
    
    # Order details (like client info)
    client_name = st.text_input("Client Name")
    salon_name = st.text_input("Salon Name")
    contact = st.text_input("Contact")
    address = st.text_area("Address")
    
    order_date = st.date_input("Order Date", min_value=datetime.today())
    
    # Admin can add multiple products
    order_items = []
    
    with st.expander("Add Products to Order"):
        product_count = st.number_input("How many products to add?", min_value=1, max_value=10, value=1)
        
        for i in range(product_count):
            st.subheader(f"Product {i + 1}")
            
            product = st.selectbox(f"Select Product {i + 1}", products, key=f"product_{i}")
            qty = st.number_input(f"Quantity for Product {i + 1}", min_value=1, key=f"qty_{i}")
            mrp = st.number_input(f"MRP for Product {i + 1}", min_value=0.0, format="%.2f", key=f"mrp_{i}")
            discount = st.number_input(f"Discount for Product {i + 1}", min_value=0.0, format="%.2f", key=f"discount_{i}")
            after_discount = mrp - discount
            total = after_discount * qty
            
            order_items.append({
                "product": product,
                "qty": qty,
                "mrp": mrp,
                "discount": discount,
                "after_discount": after_discount,
                "total": total
            })
    
    # Select Distributor to assign the order
    distributors = session.query(User).filter(User.role == "Distributor").all()
    distributor_options = [distributor.username for distributor in distributors]
    assigned_distributor = st.selectbox("Assign to Distributor", distributor_options)
    
    if st.button("Register Order"):
        selected_distributor = session.query(User).filter(User.username == assigned_distributor).first()
        
        # Create a new order (header record)
        new_order = Order(
            order_date=datetime.now(),
            client_name=client_name,
            salon_name=salon_name,
            contact=contact,
            address=address,
            distributor_id=selected_distributor.id
        )
        session.add(new_order)
        session.commit()
        
        # Add order details (items)
        for item in order_items:
            new_order_detail = OrderDetail(
                order_id=new_order.id,
                item_description=item["product"],
                qty=item["qty"],
                mrp=item["mrp"],
                discount=item["discount"],
                after_discount=item["after_discount"],
                total=item["total"]
            )
            session.add(new_order_detail)
        
        session.commit()
        
        st.success("Order Registered Successfully!")
        
        # Notify Distributor
        notification = Notification(
            user_id=selected_distributor.id,
            message=f"New order registered for {salon_name} - {client_name}",
            is_read=False,
            timestamp=datetime.now()
        )
        session.add(notification)
        session.commit()
        st.info("Notification Sent to Distributor.")

# Update Order Detail model
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class OrderDetail(Base):
    __tablename__ = 'order_details'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    item_description = Column(String)
    qty = Column(Integer)
    mrp = Column(Float)
    discount = Column(Float)
    after_discount = Column(Float)
    total = Column(Float)
    
    order = relationship("Order", back_populates="order_details")

# Add relationship to the Order model
class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    order_date = Column(String)
    client_name = Column(String)
    salon_name = Column(String)
    contact = Column(String)
    address = Column(String)
    distributor_id = Column(Integer, ForeignKey('users.id'))
    
    distributor = relationship("User", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")

# Update User model to include relationship
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    role = Column(String)
    
    orders = relationship("Order", back_populates="distributor")
