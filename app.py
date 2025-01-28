import streamlit as st
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Order, Subordinate, Notification  # Assuming models are saved in models.py

# Set up SQLAlchemy session
engine = create_engine('sqlite:///salon_orders.db')
Session = sessionmaker(bind=engine)
session = Session()

# Add order
def register_order():
    st.header("Register New Order")
    
    # Inputs for Order Details
    item_description = st.text_input("Item Description")
    qty = st.number_input("Quantity", min_value=1)
    mrp = st.number_input("MRP", min_value=0.0, format="%.2f")
    discount = st.number_input("Discount", min_value=0.0, format="%.2f")
    after_discount = mrp - discount
    total = after_discount * qty
    
    order_date = st.date_input("Order Date", min_value=datetime.today())
    
    client_name = st.text_input("Client Name")
    salon_name = st.text_input("Salon Name")
    contact = st.text_input("Contact")
    address = st.text_area("Address")
    
    # Save Order to Database
    if st.button("Register Order"):
        new_order = Order(
            item_description=item_description,
            qty=qty,
            mrp=mrp,
            discount=discount,
            after_discount=after_discount,
            total=total,
            order_date=datetime.now(),
            client_name=client_name,
            salon_name=salon_name,
            contact=contact,
            address=address
        )
        session.add(new_order)
        session.commit()
        st.success("Order Registered Successfully!")
        
        # Notify Subordinates
        subordinates = session.query(Subordinate).all()
        for sub in subordinates:
            notification = Notification(
                subordinate_id=sub.id,
                message=f"New order registered for {salon_name} - {client_name}",
                is_read=False,
                timestamp=datetime.now()
            )
            session.add(notification)
        session.commit()
        st.info("Notifications Sent to Subordinates.")

# Subordinate Dashboard
def subordinate_dashboard():
    st.header("Subordinate Dashboard")
    subordinates = session.query(Subordinate).all()
    
    for sub in subordinates:
        st.subheader(f"Orders for {sub.name}")
        
        notifications = session.query(Notification).filter(Notification.subordinate_id == sub.id, Notification.is_read == False).all()
        for notification in notifications:
            st.write(notification.message)
            if st.button(f"Mark as Read for {sub.name}"):
                notification.is_read = True
                session.commit()
                st.success(f"Marked notification as read for {sub.name}")
    
# Main Menu
def main():
    menu = ["Register Order", "Subordinate Dashboard"]
    choice = st.sidebar.selectbox("Select an Option", menu)
    
    if choice == "Register Order":
        register_order()
    elif choice == "Subordinate Dashboard":
        subordinate_dashboard()

if __name__ == '__main__':
    main()
