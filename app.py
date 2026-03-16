import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Setup page config
st.set_page_config(page_title="Representation Portal", layout="centered")

# --- DATA: Attorney Specifics ---
attorney_data = {
    "Kylee Nizuryn": {
        "fee_text": "The Attorney shall receive one-third (1/3) of the total gross amount of recovery. In the event of no recovery, Client shall owe Attorney nothing.",
        "needs_ssn": False,
        "target_email": "tgottardi@advanced-spinal-care.com"
    },
    "Brian Duffy": {
        "fee_text": "Contingency Fee: 25% (1/4) for out-of-court settlement; 33% (1/3) if litigation is pursued.",
        "needs_ssn": True,
        "target_email": "tgottardi@advanced-spinal-care.com"
    },
    "McKenzie & Snyder": {
        "fee_text": "Client agrees to pay Lawyer 25% of the gross amount of the recovery. If nothing is recovered, Lawyer shall receive no compensation.",
        "needs_ssn": True,
        "target_email": "tgottardi@advanced-spinal-care.com"
    }
}

# --- EMAIL FUNCTION ---
def send_notification(firm_name, client_name, client_phone, client_email, target_email):
    try:
        sender_email = st.secrets["EMAIL_SENDER"]
        sender_password = st.secrets["EMAIL_PASSWORD"]
        
        subject = f"NEW SIGNED REQUEST: {client_name} for {firm_name}"
        body = f"A new representation request has been signed.\n\nAttorney: {firm_name}\nClient: {client_name}\nPhone: {client_phone}\nEmail: {client_email}"
        
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

# --- NAVIGATION ---
query_params = st.query_params
if "firm" in query_params:
    app_mode = "Client: Sign Form"
else:
    app_mode = st.sidebar.radio("Navigation", ["Marketer: Generate Link", "Client: Sign Form"])

# --- MODE 1: MARKETER ---
if app_mode == "Marketer: Generate Link":
    st.title("Marketer Dispatch")
    selected_atty = st.selectbox("Assigning Attorney", list(attorney_data.keys()))
    base_url = "https://legal---app-fwqqgehtna457ta8badeuo.streamlit.app/"
    query_param = f"?firm={selected_atty.replace(' ', '+')}"
    final_link = base_url + query_param
    st.code(final_link, language=None)

# --- MODE 2: CLIENT ---
elif app_mode == "Client: Sign Form":
    default_firm = query_params.get("firm", "Kylee Nizuryn").replace("+", " ")
    st.title("Request for Representation")
    st.warning(attorney_data[default_firm]["fee_text"])
    
    c_name = st.text_input("Full Name")
    c_phone = st.text_input("Phone Number")
    c_email = st.text_input("Email Address")
    signature = st.text_input("Type Full Name to Sign")
    
    if st.button("Submit Signed Request"):
        if signature and c_name:
            with st.spinner("Sending to attorney..."):
                success = send_notification(default_firm, c_name, c_phone, c_email, attorney_data[default_firm]["target_email"])
                if success:
                    st.success(f"Thank you, {c_name}. Your request has been sent to {default_firm}.")
        else:
            st.error("Please provide your name and signature.")
