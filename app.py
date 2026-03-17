import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

st.set_page_config(page_title="Representation Portal", layout="centered", page_icon="⚖️")

# --- DATA: Individualized Branding for each Office ---
attorney_data = {
    "Ralls Legal Representation": {
        "fee_text": "**CONTINGENT FEE AGREEMENT**\nThe Attorney shall receive one-third (1/3) of the total gross amount of recovery.",
        "needs_extra": False,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#f2e1a3"
    },
    "Brian Duffy Legal Representation": {
        "fee_text": "**AUTHORITY TO REPRESENT AND FEE AGREEMENT**\nContingency fee of 25% for out-of-court and 33% for litigation.",
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#a3c2f2"
    },
    "Mckenzie & Snyder Legal Representation": {
        "fee_text": "**CONTINGENT FEE AGREEMENT**\nClient agrees to pay Lawyer 25% of the gross recovery.",
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#a3f2b5"
    }
}

# --- GET THE OFFICE FROM THE LINK ---
# This looks at the URL and picks the right office name immediately
query_params = st.query_params
firm_name = query_params.get("firm", "Ralls Legal Representation").replace("+", " ")

# Final check: If the link is weird or empty, default to Ralls
if firm_name not in attorney_data:
    firm_name = "Ralls Legal Representation"

office_info = attorney_data[firm_name]

# --- DYNAMIC HEADER: This will now change for every office ---
st.markdown(
    f"""
    <div style="background-color: #1a1a1a; padding: 25px; border-radius: 12px; text-align: center; border-bottom: 6px solid {office_info['color']}; margin-bottom: 35px;">
        <span style="font-size: 34px; color: {office_info['color']}; font-weight: bold; font-family: 'Times New Roman', Times, serif;">
            ⚖️ {firm_name}
        </span>
        <div style="font-size: 14px; color: #ffffff; letter-spacing: 2px; text-transform: uppercase; margin-top: 8px;">
            Professional Legal Services
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- APP MODES ---
if "firm" in query_params:
    app_mode = "Client: Sign Form"
else:
    app_mode = st.sidebar.radio("Navigation", ["Marketer: Generate Link", "Client: Sign Form"])

if app_mode == "Marketer: Generate Link":
    st.subheader("Marketer Dispatch")
    selected = st.selectbox("Select Office", list(attorney_data.keys()))
    base_url = "https://legal---app-fwqqgehtna457ta8badeuo.streamlit.app/"
    st.info(f"Send this link for {selected}:")
    st.code(f"{base_url}?firm={selected.replace(' ', '+')}", language=None)

elif app_mode == "Client: Sign Form":
    st.warning(office_info["fee_text"])
    c_name = st.text_input("Full Name")
    c_date = st.date_input("Date of Accident", value=date.today())
    c_phone = st.text_input("Phone Number")
    
    if office_info["needs_extra"]:
        col1, col2 = st.columns(2)
        with col1: dob = st.text_input("Date of Birth")
        with col2: ssn = st.text_input("Last 4 SSN", max_chars=4)
    
    st.write(f"I authorize **{firm_name}** to represent me.")
    sig = st.text_input("Type Name to Sign")
    
    if st.button("Submit Signed Request"):
        if sig and c_name:
            st.success(f"Sent to {firm_name}!")
