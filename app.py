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

# Predefined Products from the Bill
def predefined_products():
    return [
        {"item": "5 - Step Facial - Radiance Revival", "qty": 10, "mrp": 325.00, "discount": 50.00, "after_discount": 162.50, "total": 1625},
        {"item": "5 - Step Facial - Derma Lumin", "qty": 10, "mrp": 325.00, "discount": 50.00, "after_discount": 162.50, "total": 1625},
        {"item": "5 - Step Facial - Cobalin B12", "qty": 10, "mrp": 325.00, "discount": 50.00, "after_discount": 162.50, "total": 1625},
        {"item": "5 - Step Facial - Mucin Glow", "qty": 10, "mrp": 325.00, "discount": 50.00, "after_discount": 162.50, "total": 1625},
        {"item": "De Tan Single Use - 12 Gms (10 Pcs)", "qty": 10, "mrp": 599.00, "discount": 65.00, "after_discount": 209.65, "total": 2097},
        {"item": "4 Step Cleanup - Gold Sheen", "qty": 10, "mrp": 199.00, "discount": 65.00, "after_discount": 69.65, "total": 697},
        {"item": "4 Step Cleanup - Aqua Splash", "qty": 10, "mrp": 199.00, "discount": 65.00, "after_discount": 69.65, "total": 697},
        {"item": "4Step CleanUp - Charcoal Splash", "qty": 10, "mrp": 199.00, "discount": 65.00, "after_discount": 69.65, "total": 697},
        {"item": "4 Step Cleanup - Acne Heel", "qty": 10, "mrp": 199.00, "discount": 65.00, "after_discount": 69.65, "total": 697},
        {"item": "4 Step Cleanup - Radiat Youth", "qty": 10, "mrp": 199.00, "discount": 65.00, "after_discount": 69.65, "total": 697}
    ]

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

    # Register new order
    register_order()

    # View all orders and assign to a distributor
    st.header("View All Orders")
    orders = session.query(Order).all()
    for order in orders:
        st.write(order)

    # Assign order to distributor
    st.header("Assign Order to Distributor")
    distributors = session.query(User).filter(User.role == "Distributor").all()
    distributor_options = [distributor.username for distributor in distributors]
    selected_distributor = st.selectbox("Select Distributor", distributor_options)

    order_id = st.text_input("Enter Order ID to Assign")
    if st.button("Assign Order"):
        order = session.query(Order).filter(Order.id == order_id).first()
        if order:
            distributor = session.query(User).filter(User.username == selected_distributor).first()
            order.distributor_id = distributor.id
            session.commit()
            st.success(f"Order {order_id} assigned to {selected_distributor}")
        else:
            st.error("Order ID not found")

# Distributor Dashboard
def distributor_dashboard():
    st.title("Distributor Dashboard")
    
    # View orders assigned to distributor
    st.header("Assigned Orders")
    orders = session.query(Order).filter(Order.distributor_id == st.session_state.user_id).all()
    for order in orders:
        st.write(order)

# Register Order (as before)
def register_order():
    st.header("Register New Order")

    # Pre-fill the products from the bill
    products = predefined_products()
    for product in products:
        st.write(f"**Item:** {product['item']}")
        st.write(f"**Quantity:** {product['qty']}")
        st.write(f"**MRP:** {product['mrp']}")
        st.write(f"**Discount:** {product['discount']}")
        st.write(f"**Total after Discount:** {product['after_discount']}")
        st.write(f"**Total Price:** {product['total']}")

    client_name = st.text_input("Client Name")
    salon_name = st.text_input("Salon Name")
    contact = st.text_input("Contact")
    address = st.text_area("Address")

    if st.button("Register Order"):
        total_price = sum([product['total'] for product in products])
        new_order = Order(
            client_name=client_name,
            salon_name=salon_name,
            contact=contact,
            address=address,
            total_price=total_price,
            order_date=datetime.now()
        )
        session.add(new_order)
        session.commit()

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
        st.success("Order Registered Successfully!")
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
