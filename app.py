import streamlit as st
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User, Order, Notification  # Assuming models are saved in models.py

# Set up SQLAlchemy session
engine = create_engine('sqlite:///salon_orders.db')
Session = sessionmaker(bind=engine)
session = Session()

# Manually add Admin and Distributor credentials
def add_initial_credentials():
    # Check if there are already users to avoid duplicate entries
    existing_users = session.query(User).all()
    if len(existing_users) == 0:
        admin_user = User(username="admin", password="admin123", role="Admin")
        distributor1 = User(username="distributor1", password="distributor123", role="Distributor")
        distributor2 = User(username="distributor2", password="distributor123", role="Distributor")

        session.add(admin_user)
        session.add(distributor1)
        session.add(distributor2)
        session.commit()
        st.info("Initial admin and distributor users have been added.")
    else:
        st.info("Users already exist. Skipping the initial user creation.")

# Login function
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = session.query(User).filter(User.username == username, User.password == password).first()
        if user:
            if user.role == "Admin":
                st.session_state.role = "Admin"
                st.session_state.user_id = user.id
                st.success("Logged in as Admin")
                admin_dashboard()
            elif user.role == "Distributor":
                st.session_state.role = "Distributor"
                st.session_state.user_id = user.id
                st.success("Logged in as Distributor")
                distributor_dashboard()
        else:
            st.error("Invalid credentials")

# Admin Dashboard
def admin_dashboard():
    st.title("Admin Dashboard")
    
    # Register new order (same as before)
    register_order()

    # View all orders
    st.header("View All Orders")
    orders = session.query(Order).all()
    for order in orders:
        st.write(order)

# Distributor Dashboard
def distributor_dashboard():
    st.title("Distributor Dashboard")
    
    # View orders assigned to distributor (same as before)
    st.header("Assigned Orders")
    orders = session.query(Order).all()  # Adjust this query to show orders assigned to this distributor
    for order in orders:
        st.write(order)

# Register Order (as before)
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
        
        # Notify Distributor
        distributors = session.query(User).filter(User.role == "Distributor").all()
        for distributor in distributors:
            notification = Notification(
                user_id=distributor.id,
                message=f"New order registered for {salon_name} - {client_name}",
                is_read=False,
                timestamp=datetime.now()
            )
            session.add(notification)
        session.commit()
        st.info("Notifications Sent to Distributors.")

def main():
    # Add initial credentials if they don't exist
    add_initial_credentials()

    if "role" not in st.session_state:
        login()
    else:
        if st.session_state.role == "Admin":
            admin_dashboard()
        elif st.session_state.role == "Distributor":
            distributor_dashboard()

if __name__ == '__main__':
    main()
