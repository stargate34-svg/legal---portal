import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

st.set_page_config(page_title="Representation Portal", layout="centered", page_icon="⚖️")

# --- DATA: The Source of Truth ---
attorney_data = {
    "ralls": {
        "full_name": "Ralls Legal Representation",
        "fee_text": "**CONTINGENT FEE AGREEMENT**\nThe Attorney shall receive one-third (1/3) of the total gross amount of recovery.",
        "needs_extra": False,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#f2e1a3" # Gold
    },
    "ohio": {
        "full_name": "Ohio Injury Attorneys",
        "fee_text": "**AUTHORITY TO REPRESENT AND FEE AGREEMENT**\nContingency fee of 25% for out-of-court and 33% for litigation.",
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#a3c2f2" # Blue
    },
    "mckenzie": {
        "full_name": "Mckenzie & Snyder Legal Representation",
        "fee_text": "**CONTINGENT FEE AGREEMENT**\nClient agrees to pay Lawyer 25% of the gross recovery.",
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#a3f2b5" # Green
    }
}

# --- 1. DETERMINE MODE ---
# Check if the URL has a firm code (e.g., ?f=ohio)
query_params = st.query_params
office_code = query_params.get("f", None)

if office_code and office_code.lower() in attorney_data:
    app_mode = "Client"
    active_key = office_code.lower()
else:
    app_mode = "Marketer"
    active_key = None

# --- 2. DRAW THE HEADER ---
if app_mode == "Marketer":
    # Generic header for your internal team
    header_title = "Legal Representation Portal"
    header_color = "#ffffff"
else:
    # Specific branding for the client
    header_title = attorney_data[active_key]["full_name"]
    header_color = attorney_data[active_key]["color"]

st.markdown(
    f"""
    <div style="background-color: #1a1a1a; padding: 25px; border-radius: 12px; text-align: center; border-bottom: 6px solid {header_color}; margin-bottom: 35px;">
        <span style="font-size: 34px; color: {header_color}; font-weight: bold; font-family: 'Times New Roman', Times, serif;">
            ⚖️ {header_title}
        </span>
        <div style="font-size: 14px; color: #ffffff; letter-spacing: 2px; text-transform: uppercase; margin-top: 8px; opacity: 0.8;">
            Professional Legal Services
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- 3. PAGE CONTENT ---

if app_mode == "Marketer":
    st.subheader("Marketer Dispatch Center")
    st.write("Select an office to generate a secure client link.")
    
    # Selection for marketers
    selected_name = st.selectbox(
        "Choose Law Firm:", 
        [v["full_name"] for v in attorney_data.values()]
    )
    
    # Get the short code for the selected name
    selected_key = [k for k, v in attorney_data.items() if v["full_name"] == selected_name][0]
    
    # Generate Link
    base_url = "https://legal---app-fwqqgehtna457ta8badeuo.streamlit.app/"
    final_link = f"{base_url}?f={selected_key}"
    
    st.info(f"Generated Link for {selected_name}:")
    st.code(final_link, language=None)
    
    if st.button("📋 Copy Link"):
        st.write(f'<script>navigator.clipboard.writeText("{final_link}");</script>', unsafe_allow_html=True)
        st.success("Link copied!")

elif app_mode == "Client":
    office = attorney_data[active_key]
    
    st.warning(office["fee_text"])
    
    st.subheader("Contact Information")
    c_name = st.text_input("Full Name")
    c_phone = st.text_input("Phone Number")
    c_email = st.text_input("Email Address")
    
    c_dob = ""
    c_ssn = ""
    if office["needs_extra"]:
        col1, col2 = st.columns(2)
        with col1:
            c_dob = st.text_input("Date of Birth")
        with col2:
            c_ssn = st.text_input("Last 4 SSN", max_chars=4)
            
    st.subheader("Authorization")
    st.write(f"I authorize **{office['full_name']}** to represent me.")
    sig = st.text_input("Type Name to Sign")
    
    if st.button("Submit Signed Form"):
        if sig and c_name and c_phone:
            # Email logic (simplified for brevity)
            st.success("Your request has been submitted!")
        else:
            st.error("Please fill in all required fields.")
