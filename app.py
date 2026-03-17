import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

# Set up page config
st.set_page_config(
    page_title="Legal Representation Portal",
    layout="centered",
    page_icon="⚖️"
)

# --- DATA: Professional Attorney Agreements (Individualized Branding) ---
attorney_data = {
    "Ralls Legal Representation": {
        "fee_text": """**CONTINGENT FEE AGREEMENT**
The Attorney shall receive one-third (1/3) of the total gross amount of recovery. 
In the event of no recovery, Client shall owe Attorney nothing for services rendered.""",
        "needs_extra": False,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "header_color": "#f2e1a3" # Gold
    },
    "Brian Duffy Legal Representation": {
        "fee_text": """**AUTHORITY TO REPRESENT AND FEE AGREEMENT**
Client agrees to pay Attorney a contingency fee of 25% (1/4) for any out-of-court settlement. 
If litigation is pursued, the fee shall be 33% (1/3) of the gross recovery. 
Client remains responsible for expenses and medical bills.""",
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "header_color": "#a3c2f2" # Blue
    },
    "Mckenzie & Snyder Legal Representation": {
        "fee_text": """**CONTINGENT FEE AGREEMENT**
Client agrees to pay Lawyer 25% of the gross amount of the recovery. 
If nothing is recovered, Lawyer shall receive no compensation. 
Lawyer is authorized to incur reasonable costs in the handling of this claim.""",
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "header_color": "#a3f2b5" # Green
    }
}

# --- EMAIL FUNCTION ---
def send_notification(firm_name, client_name, client_phone, client_email, accident_date, dob, ssn, target_email):
    try:
        sender_email = st.secrets["EMAIL_SENDER"]
        sender_password = st.secrets["EMAIL_PASSWORD"]
        
        subject = f"NEW SIGNED REQUEST: {client_name} - {firm_name}"
        body = f"""
NEW REPRESENTATION REQUEST SIGNED

Office: {firm_name}
Client Name: {client_name}
Client Phone: {client_phone}
Client Email: {client_email}
Date of Accident: {accident_date}
Date of Birth: {dob if dob else 'N/A'}
Last 4 SSN: {ssn if ssn else 'N/A'}

The client has electronically signed the fee agreement for this office.
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

# --- DYNAMIC HEADER & LOGO ---
query_params = st.query_params
firm_param = query_params.get("firm", "Ralls Legal Representation").replace("+", " ")

# Safety fallback if link is broken
if firm_param not in attorney_data:
    firm_param = "Ralls Legal Representation"

office_branding = attorney_data[firm_param]

# This creates the custom logo box for EACH specific firm
st.markdown(
    f"""
    <div style="background-color: #1a1a1a; padding: 25px; border-radius: 12px; text-align: center; border-bottom: 6px solid {office_branding['header_color']}; margin-bottom: 35px; box-shadow: 2px 2px 10px rgba(0,0,0,0.5);">
        <span style="font-size: 34px; color: {office_branding['header_color']}; font-weight: bold; font-family: 'Times New Roman', Times, serif;">
            ⚖️ {firm_param}
        </span>
        <div style="font-size: 14px; color: #ffffff; letter-spacing: 2px; text-transform: uppercase; margin-top: 8px; opacity: 0.8;">
            Professional Legal Services
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- NAVIGATION ---
if "firm" in query_params:
    app_mode = "Client: Sign Form"
else:
    app_mode = st.sidebar.radio("Navigation", ["Marketer: Generate Link", "Client: Sign Form"])

# --- MODE 1: MARKETER ---
if app_mode == "Marketer: Generate Link":
    st.subheader("Marketer Dispatch")
    selected_atty = st.selectbox("Select Office to Generate Link", list(attorney_data.keys()))
    base_url = "https://legal---app-fwqqgehtna457ta8badeuo.streamlit.app/"
    query_param = f"?firm={selected_atty.replace(' ', '+')}"
    st.info(f"Link for {selected_atty}:")
    st.code(base_url + query_param, language=None)

# --- MODE 2: CLIENT ---
elif app_mode == "Client: Sign Form":
    st.warning(office_branding["fee_text"])
    
    st.subheader("Incident & Contact Details")
    c_name = st.text_input("Full Name")
    c_date_acc = st.date_input("Date of Accident", value=date.today())
    c_phone = st.text_input("Phone Number")
    c_email = st.text_input("Email Address")
    
    c_dob = ""
    c_ssn = ""
    if office_branding["needs_extra"]:
        col1, col2 = st.columns(2)
        with col1:
            c_dob = st.text_input("Date of Birth (MM/DD/YYYY)")
        with col2:
            c_ssn = st.text_input("Last 4 of SSN", max_chars=4)
    
    st.subheader("Representation Authorization")
    st.write(f"By signing below, I authorize **{firm_param}** to represent me regarding my claims.")
    signature = st.text_input("Type Full Name to Sign")
    
    if st.button("Submit Signed Request"):
        if signature and c_name and c_phone:
            with st.spinner("Submitting to office..."):
                success = send_notification(
                    firm_param, c_name, c_phone, c_email, c_date_acc, c_dob, c_ssn, 
                    office_branding["target_email"]
                )
                if success:
                    st.success(f"Form submitted successfully to {firm_param}.")
        else:
            st.error("Please provide your Name, Phone, and Signature.")
