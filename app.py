import streamlit as st
from datetime import datetime
from database import session
from models import User, Order, Notification  # Assuming Notification model exists

def register_order():
    st.title("Register Order")
    
    # Inputs for order registration
    product = st.selectbox("Select Product", ["5 Step Facial - Radiance Revival", "5 Step Facial - Derma Lumin", 
                                              "5 Step Facial - Cobalin B12", "5 Step Facial - Mucin Glow",
                                              "De Tan Single Use - 12 Gms (10 Pcs)", "4 Step Cleanup - Gold Sheen", 
                                              "4 Step Cleanup - Aqua Splash", "4Step CleanUp - Charcoal Splash", 
                                              "4 Step Cleanup - Acne Heel", "4 Step Cleanup - Radiat Youth"])
    
    qty = st.number_input("Quantity", min_value=1, step=1)
    mrp = st.number_input("MRP", min_value=0.0, step=0.01)
    discount = st.number_input("Discount", min_value=0.0, step=0.01)
    after_discount = mrp - discount
    total = after_discount * qty

    client_name = st.text_input("Client Name")
    salon_name = st.text_input("Salon Name")
    contact = st.text_input("Contact")
    address = st.text_area("Address")

    # Distributor selection
    assigned_distributor = st.selectbox("Assign to Distributor", ["distributor1", "distributor2"])

    # Save Order to Database
    if st.button("Register Order"):
        selected_distributor = session.query(User).filter(User.username == assigned_distributor).first()

        if selected_distributor:
            new_order = Order(
                item_description=product,
                qty=qty,
                mrp=mrp,
                discount=discount,
                after_discount=after_discount,
                total=total,
                order_date=datetime.now(),
                client_name=client_name,
                salon_name=salon_name,
                contact=contact,
                address=address,
                distributor_id=selected_distributor.id  # Ensure distributor_id is passed correctly
            )
            session.add(new_order)
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
        else:
            st.error("Invalid Distributor selected!")

# Main function to run the Streamlit app
def main():
    admin_user = User(username="admin", password="admin123", role="Admin")
    distributor1 = User(username="distributor1", password="distributor123", role="Distributor")
    distributor2 = User(username="distributor2", password="distributor123", role="Distributor")

    # Add default users manually
    session.add(admin_user)
    session.add(distributor1)
    session.add(distributor2)
    session.commit()

    # Admin dashboard to register orders
    if st.sidebar.selectbox("Select Role", ["Admin", "Distributor"]) == "Admin":
        register_order()

if __name__ == "__main__":
    main()
