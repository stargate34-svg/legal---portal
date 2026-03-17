import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
import urllib.parse

st.set_page_config(page_title="Representation Portal", layout="centered", page_icon="⚖️")

# --- DATA: Individualized Branding for each Office ---
attorney_data = {
    "Ralls Legal Representation": {
        "fee_text": "**CONTINGENT FEE AGREEMENT**\nThe Attorney shall receive one-third (1/3) of the total gross amount of recovery.",
        "needs_extra": False,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#f2e1a3" # Gold
    },
    "Ohio Injury Attorneys": {
        "fee_text": "**AUTHORITY TO REPRESENT AND FEE AGREEMENT**\nContingency fee of 25% for out-of-court and 33% for litigation.",
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#a3c2f2" # Blue
    },
    "Mckenzie & Snyder Legal Representation": {
        "fee_text": "**CONTINGENT FEE AGREEMENT**\nClient agrees to pay Lawyer 25% of the gross recovery.",
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#a3f2b5" # Green
    }
}

# --- 1. READ URL AND DETERMINE THE APP MODE ---
query_params = st.query_params
raw_firm = query_params.get("firm", "")
url_firm = urllib.parse.unquote(raw_firm).replace("+", " ")

if "firm" in query_params and url_firm in attorney_data:
    app_mode = "Client: Sign Form"
    active_firm = url_firm
else:
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Go to:", ["Marketer: Generate Link", "Client: Sign Form"])
    
    if app_mode == "Marketer: Generate Link":
        active_firm = st.sidebar.selectbox("Select Office:", list(attorney_data.keys()))
    else:
        active_firm = "Ralls Legal Representation"

office_info = attorney_data[active_firm]

# --- 2. DRAW THE DYNAMIC HEADER ---
st.markdown(
    f"""
    <div style="background-color: #1a1a1a; padding: 25px; border-radius: 12px; text-align: center; border-bottom: 6px solid {office_info['color']}; margin-bottom: 35px; box-shadow: 2px 2px 10px rgba(0,0,0,0.5);">
        <span style="font-size: 34px; color: {office_info['color']}; font-weight: bold; font-family: 'Times New Roman', Times, serif;">
            ⚖️ {active_firm}
        </span>
        <div style="font-size: 14px; color: #ffffff; letter-spacing: 2px; text-transform: uppercase; margin-top: 8px; opacity: 0.8;">
            Professional Legal Services
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- 3. DRAW THE CONTENT ---
if app_mode == "Marketer: Generate Link":
    st.subheader("Marketer Dispatch")
    st.write(f"Generating secure link for: **{active_firm}**")
    
    base_url = "https://legal---app-fwqqgehtna457ta8badeuo.streamlit.app/"
    safe_link_name = active_firm.replace(' ', '+')
    final_link = f"{base_url}?firm={safe_link_name}"
    
    st.info("Client Access Link:")
    st.code(final_link, language=None)

elif app_mode == "Client: Sign Form":
    st.warning(office_info["fee_text"])
    
    st.subheader("Incident & Contact Details")
    c_name = st.text_input("Full Name")
    c_date_acc = st.date_input("Date of Accident", value=date.today())
    c_phone = st.text_input("Phone Number")
    c_email = st.text_input("Email Address")
    
    c_dob = ""
    c_ssn = ""
    if office_info["needs_extra"]:
        col1, col2 = st.columns(2)
        with col1:
            c_dob = st.text_input("Date of Birth (MM/DD/YYYY)")
        with col2:
            c_ssn = st.text_input("Last 4 of SSN", max_chars=4)
    
    st.subheader("Representation Authorization")
    st.write(f"By signing below, I authorize **{active_firm}** to represent me regarding my claims.")
    signature = st.text_input("Type Full Name to Sign")
    
    if st.button("Submit Signed Request"):
        if signature and c_name and c_phone:
            with st.spinner("Submitting..."):
                try:
                    sender_email = st.secrets["EMAIL_SENDER"]
                    sender_password = st.secrets["EMAIL_PASSWORD"]
                    
                    subject = f"NEW SIGNED REQUEST: {c_name} - {active_firm}"
                    body = f"""
NEW REPRESENTATION REQUEST SIGNED

Office: {active_firm}
Client Name: {c_name}
Client Phone: {c_phone}
Client Email: {c_email}
Date of Accident: {c_date_acc}
Date of Birth: {c_dob if c_dob else 'N/A'}
Last 4 SSN: {c_ssn if c_ssn else 'N/A'}

The client has electronically signed the fee agreement for this office.
                    """
                    
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = office_info["target_email"]
                    msg['Subject'] = subject
                    msg.attach(MIMEText(body, 'plain'))
                    
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
                    server.quit()
                    
                    st.success(f"Thank you, {c_name}. Your request has been sent to {active_firm}.")
                except Exception as e:
                    st.error(f"Error sending email: {e}")
        else:
            st.error("Please provide your Name, Phone, and Signature.")
