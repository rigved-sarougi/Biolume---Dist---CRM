import streamlit as st
from database import create_tables, add_user, add_order, update_order_status, fetch_orders, fetch_users
from utils import authenticate_user

# Initialize Database
create_tables()

# Authentication Section
st.sidebar.title("Login")
user_role = st.sidebar.radio("Login As", ["Admin", "Distributor"])
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login = st.sidebar.button("Login")

if login:
    user_authenticated, user_info = authenticate_user(username, password, user_role)
    if user_authenticated:
        st.sidebar.success(f"Welcome {user_info['name']} ({user_role})")

        if user_role == "Admin":
            st.title("Admin Dashboard")

            # Section to create distributor accounts
            st.subheader("Add Distributor")
            dist_name = st.text_input("Distributor Name")
            dist_username = st.text_input("Distributor Username")
            dist_password = st.text_input("Distributor Password", type="password")
            if st.button("Add Distributor"):
                add_user(dist_name, dist_username, dist_password, "Distributor")
                st.success("Distributor added successfully!")

            # Section to register orders
            st.subheader("Register Order")
            distributor = st.selectbox("Select Distributor", fetch_users("Distributor"))
            product_name = st.text_input("Product Name")
            quantity = st.number_input("Quantity", min_value=1)
            if st.button("Add Order"):
                add_order(distributor, product_name, quantity)
                st.success("Order registered successfully!")

            # View orders
            st.subheader("All Orders")
            orders = fetch_orders()
            st.table(orders)

        elif user_role == "Distributor":
            st.title("Distributor Dashboard")

            # View assigned orders
            st.subheader("My Orders")
            orders = fetch_orders(username)
            st.table(orders)

            # Update order status
            st.subheader("Update Order Status")
            order_id = st.selectbox("Select Order ID", [order["id"] for order in orders])
            status = st.radio("Status", ["Payment Received", "Order Dispatched", "Order Delivered", "Order Canceled", "Other Issue"])
            remarks = ""
            if status == "Other Issue":
                remarks = st.text_area("Remarks")
            if st.button("Update Status"):
                update_order_status(order_id, status, remarks)
                st.success("Order status updated successfully!")
    else:
        st.sidebar.error("Invalid credentials. Please try again.")
