import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

st.set_page_config(page_title="Representation Portal", layout="centered", page_icon="⚖️")

# --- DATA: Mapped to Short Keys for reliability ---
# We use short "slugs" (ralls, ohio, mckenzie) for the URL
attorney_data = {
    "ralls": {
        "full_name": "Ralls Legal Representation",
        "fee_text": """**CONTINGENT FEE AGREEMENT**

The undersigned (Client) retains the undersigned (Attorney) for representation regarding personal injuries. Attorney will devote their professional abilities to the case, which may be handled by one or more members, staff, or associates.

Client shall pay no upfront fee. Attorney shall work on a contingent fee basis and shall receive **one‑third (1/3) of the total gross amount recovered** from any settlement or judgment.

In the event of no recovery, Client owes Attorney nothing for services rendered.""",
        "needs_extra": False,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#f2e1a3" # Gold
    },
    "ohio": {
        "full_name": "Ohio Injury Attorneys",
        "fee_text": """**AUTHORITY TO REPRESENT AND FEE AGREEMENT**

1. **Contingency Fee.** The Firm shall receive a contingency fee of **25% (1/4)** of all funds collected for an out‑of‑court settlement. If litigation is pursued, the fee shall be **33% (1/3)** of all funds collected.

2. **Expenses.** Expenses (investigation, records, court fees, etc.) are the sole responsibility of the Client. They will not be included in the Firm's contingency fee. Any funds advanced by the Firm shall be reimbursed from settlement proceeds.

3. **Medical Bills.** Medical bills are the Client's responsibility. At Client's direction, the Firm will pay medical bills out of any settlement.

4. **Liens & Subrogation.** The Firm may be obligated to pay any liens or subrogation interests out of settlement. Client must inform the Firm of any third‑party interests.

5. **Termination.** Either party may terminate the agreement. If Client terminates, the Firm shall be compensated for work performed unless a waiver is agreed in writing.

6. **Medical Authorization.** By signing below, Client grants permission to obtain and update medical records and to disclose case information to providers for bill negotiation.

By signing below, Client agrees to these terms.""",
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

# --- 1. DETECTION LOGIC ---
query_params = st.query_params
# We look for '?f=' in the URL
office_key = query_params.get("f", "ralls").lower()

# Safety fallback: If key isn't found, default to ralls
if office_key not in attorney_data:
    office_key = "ralls"

# Get the full data for the active office
office = attorney_data[office_key]

# --- 2. APP MODES ---
if "f" in query_params:
    app_mode = "Client: Sign Form"
else:
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Go to:", ["Marketer: Generate Link", "Client: Sign Form"])
    
    if app_mode == "Marketer: Generate Link":
        # Let marketers pick by the full name
        selected_display = st.sidebar.selectbox(
            "Select Office:", 
            [attorney_data[k]["full_name"] for k in attorney_data]
        )
        # Find the key that matches that display name
        for k, v in attorney_data.items():
            if v["full_name"] == selected_display:
                office_key = k
                office = v

# --- 3. DYNAMIC HEADER BASED ON MODE ---
if app_mode == "Client: Sign Form":
    st.markdown(
        f"""
        <div style="background-color: #1a1a1a; padding: 25px; border-radius: 12px; text-align: center; border-bottom: 6px solid {office['color']}; margin-bottom: 35px; box-shadow: 2px 2px 10px rgba(0,0,0,0.5);">
            <span style="font-size: 34px; color: {office['color']}; font-weight: bold; font-family: 'Times New Roman', Times, serif;">
                ⚖️ {office['full_name']}
            </span>
            <div style="font-size: 14px; color: #ffffff; letter-spacing: 2px; text-transform: uppercase; margin-top: 8px; opacity: 0.8;">
                Professional Legal Services
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
elif app_mode == "Marketer: Generate Link":
    st.markdown(
        f"""
        <div style="background-color: #1a1a1a; padding: 25px; border-radius: 12px; text-align: center; border-bottom: 6px solid #888888; margin-bottom: 35px; box-shadow: 2px 2px 10px rgba(0,0,0,0.5);">
            <span style="font-size: 34px; color: #888888; font-weight: bold; font-family: 'Times New Roman', Times, serif;">
                ⚖️ Legal Representations Portal
            </span>
            <div style="font-size: 14px; color: #ffffff; letter-spacing: 2px; text-transform: uppercase; margin-top: 8px; opacity: 0.8;">
                Marketer Access
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- 4. MARKETER DISPATCH ---
if app_mode == "Marketer: Generate Link":
    st.subheader("Marketer Dispatch")
    st.write(f"Generating secure link for: **{office['full_name']}**")
    
    base_url = "https://legal---app-fwqqgehtna457ta8badeuo.streamlit.app/"
    final_link = f"{base_url}?f={office_key}"
    
    st.info("Client Access Link (Copy This):")
    st.code(final_link, language=None)
    
    # Add a reliable copy button using st.components.v1.html
    copy_html = f"""
    <div style="display: flex; justify-content: center; margin-top: 10px;">
        <button onclick="navigator.clipboard.writeText('{final_link}').then(() => alert('Link copied to clipboard!')).catch(() => alert('Failed to copy.'))" 
                style="background-color: #4CAF50; border: none; color: white; padding: 10px 24px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 8px;">
            📋 Copy Link to Clipboard
        </button>
    </div>
    """
    st.components.v1.html(copy_html, height=80)

# --- 5. CLIENT FORM ---
elif app_mode == "Client: Sign Form":
    st.warning(office["fee_text"])
    
    st.subheader("Incident & Contact Details")
    c_name = st.text_input("Full Name")
    c_date_acc = st.date_input("Date of Accident", value=date.today())
    c_phone = st.text_input("Phone Number")
    c_email = st.text_input("Email Address")
    
    c_dob = ""
    c_ssn = ""
    if office["needs_extra"]:
        col1, col2 = st.columns(2)
        with col1:
            c_dob = st.text_input("Date of Birth (MM/DD/YYYY)")
        with col2:
            c_ssn = st.text_input("Last 4 of SSN", max_chars=4)
    
    st.subheader("Representation Authorization")
    st.write(f"By signing below, I authorize **{office['full_name']}** to represent me regarding my claims.")
    signature = st.text_input("Type Full Name to Sign")
    
    if st.button("Submit Signed Request"):
        if signature and c_name and c_phone:
            with st.spinner("Submitting..."):
                try:
                    sender_email = st.secrets["EMAIL_SENDER"]
                    sender_password = st.secrets["EMAIL_PASSWORD"]
                    
                    subject = f"NEW SIGNED REQUEST: {c_name} - {office['full_name']}"
                    body = f"Office: {office['full_name']}\nClient: {c_name}\nPhone: {c_phone}\nEmail: {c_email}\nAccident Date: {c_date_acc}\nDOB: {c_dob}\nSSN: {c_ssn}"
                    
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = office["target_email"]
                    msg['Subject'] = subject
                    msg.attach(MIMEText(body, 'plain'))
                    
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
                    server.quit()
                    st.success(f"Sent successfully to {office['full_name']}.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("Missing required fields.")
