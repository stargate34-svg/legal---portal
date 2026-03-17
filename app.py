import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Representation Portal", layout="centered")

# --- DATA: Professional Attorney Agreements ---
attorney_data = {
    "Ralls Attorney Intake Form": {
        "fee_text": """**CONTINGENT FEE AGREEMENT**
The Attorney shall receive one-third (1/3) of the total gross amount of recovery. 
In the event of no recovery, Client shall owe Attorney nothing for services rendered.""",
        "needs_extra": False,
        "target_email": "tgottardi@advanced-spinal-care.com"
    },
    "Brian Duffy": {
        "fee_text": """**AUTHORITY TO REPRESENT AND FEE AGREEMENT**
Client agrees to pay Attorney a contingency fee of 25% (1/4) for any out-of-court settlement. 
If litigation is pursued, the fee shall be 33% (1/3) of the gross recovery. 
Client remains responsible for expenses and medical bills.""",
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com"
    },
    "McKenzie & Snyder": {
        "fee_text": """**CONTINGENT FEE AGREEMENT**
Client agrees to pay Lawyer 25% of the gross amount of the recovery. 
If nothing is recovered, Lawyer shall receive no compensation. 
Lawyer is authorized to incur reasonable costs in the handling of this claim.""",
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com"
    }
}

# --- EMAIL FUNCTION ---
def send_notification(firm_name, client_name, client_phone, client_email, dob, ssn, target_email):
    try:
        sender_email = st.secrets["EMAIL_SENDER"]
        sender_password = st.secrets["EMAIL_PASSWORD"]
        
        subject = f"NEW SIGNED REQUEST: {client_name} for {firm_name}"
        body = f"""
NEW REPRESENTATION REQUEST SIGNED

Attorney/Form: {firm_name}
Client Name: {client_name}
Client Phone: {client_phone}
Client Email: {client_email}
Date of Birth: {dob if dob else 'N/A'}
Last 4 SSN: {ssn if ssn else 'N/A'}

The client has electronically signed the fee agreement for this intake.
        """
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = target_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# --- NAVIGATION & ERROR HANDLING ---
query_params = st.query_params
firm_param = query_params.get("firm", "Ralls Attorney Intake Form").replace("+", " ")

# Safety Check: If the firm in the link doesn't exist, default to Ralls
if firm_param not in attorney_data:
    firm_param = "Ralls Attorney Intake Form"

if "firm" in query_params:
    app_mode = "Client: Sign Form"
else:
    app_mode = st.sidebar.radio("Navigation", ["Marketer: Generate Link", "Client: Sign Form"])

# --- MODE 1: MARKETER ---
if app_mode == "Marketer: Generate Link":
    st.title("Marketer Dispatch")
    selected_atty = st.selectbox("Assigning Intake Form", list(attorney_data.keys()))
    # Updated Base URL
    base_url = "https://legal---app-fwqqgehtna457ta8badeuo.streamlit.app/"
    query_param = f"?firm={selected_atty.replace(' ', '+')}"
    st.info(f"Send this link to the client for {selected_atty}:")
    st.code(base_url + query_param, language=None)

# --- MODE 2: CLIENT ---
elif app_mode == "Client: Sign Form":
    st.title("Request for Representation")
    st.markdown(f"### {firm_param}")
    st.warning(attorney_data[firm_param]["fee_text"])
    
    st.subheader("Your Information")
    c_name = st.text_input("Full Name")
    c_phone = st.text_input("Phone Number")
    c_email = st.text_input("Email Address")
    
    c_dob = ""
    c_ssn = ""
    if attorney_data[firm_param]["needs_extra"]:
        col1, col2 = st.columns(2)
        with col1:
            c_dob = st.text_input("Date of Birth (MM/DD/YYYY)")
        with col2:
            c_ssn = st.text_input("Last 4 of SSN", max_chars=4)
    
    st.subheader("Electronic Signature")
    st.write(f"By signing below, I am requesting representation via the {firm_param}.")
    signature = st.text_input("Type Full Name to Sign")
    
    if st.button("Submit Signed Request"):
        if signature and c_name and c_phone:
            with st.spinner("Submitting..."):
                success = send_notification(
                    firm_param, c_name, c_phone, c_email, c_dob, c_ssn, 
                    attorney_data[firm_param]["target_email"]
                )
                if success:
                    st.success(f"Thank you. Your request has been sent via the {firm_param}.")
        else:
            st.error("Please fill in your name, phone, and signature.")
