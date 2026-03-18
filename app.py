import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

st.set_page_config(page_title="Representation Portal", layout="centered", page_icon="⚖️")

# --- GLOBAL STYLE ---
st.markdown("""
<style>
body {
    background-color: #f4f6f9;
}
.block-container {
    padding-top: 2rem;
    max-width: 700px;
}
div[data-testid="stTextInput"] input {
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- DATA ---
attorney_data = {
    "ralls": {
        "full_name": "Ralls Legal Representation",
        "fee_text": """**CONTINGENT FEE AGREEMENT**

The undersigned (Client) retains the undersigned (Attorney) for representation regarding personal injuries. Attorney will devote their professional abilities to the case, which may be handled by one or more members, staff, or associates.

Client shall pay no upfront fee. Attorney shall work on a contingent fee basis and shall receive **one-third (1/3) of the total gross amount recovered** from any settlement or judgment.

In the event of no recovery, Client owes Attorney nothing for services rendered.""",
        "needs_extra": False,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#f2e1a3"
    },
    "ohio": {
        "full_name": "Ohio Injury Attorneys",
        "fee_text": """**AUTHORITY TO REPRESENT AND FEE AGREEMENT**

1. **Contingency Fee.** The Firm shall receive a contingency fee of **25% (1/4)** of all funds collected for an out-of-court settlement. If litigation is pursued, the fee shall be **33% (1/3)** of all funds collected.

2. **Expenses.** Expenses (investigation, records, court fees, etc.) are the sole responsibility of the Client. They will not be included in the Firm's contingency fee. Any funds advanced by the Firm shall be reimbursed from settlement proceeds.

3. **Medical Bills.** Medical bills are the Client's responsibility. At Client's direction, the Firm will pay medical bills out of any settlement.

4. **Liens & Subrogation.** The Firm may be obligated to pay any liens or subrogation interests out of settlement. Client must inform the Firm of any third-party interests.

5. **Termination.** Either party may terminate the agreement. If Client terminates, the Firm shall be compensated for work performed unless a waiver is agreed in writing.

6. **Medical Authorization.** By signing below, Client grants permission to obtain and update medical records and to disclose case information to providers for bill negotiation.

By signing below, Client agrees to these terms.""",
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#a3c2f2"
    },
    "mckenzie": {
        "full_name": "Mckenzie & Snyder Legal Representation",
        "fee_text": """**CONTINGENT FEE AGREEMENT**

This agreement is voluntarily entered between the undersigned (Client) and McKenzie & Snyder LLP (Lawyer).

Client retains Lawyer to recover damages sustained in an accident on the date provided below.

In consideration of legal services, Client agrees to pay Lawyer **25% of the gross amount recovered**, whether by settlement or trial.

Lawyer accepts employment and will do all acts necessary to protect Client's rights.

If nothing is recovered, Lawyer receives no compensation. However, Client is obligated to pay all reasonable expenses that Client authorizes or that Lawyer deems necessary to advance the claim. Client authorizes Lawyer to deduct medical bills from the gross settlement, so that Lawyer may pay such bills on behalf of Client.

The undersigned certify that they have read and understand this agreement.""",
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#a3f2b5"
    }
}

# --- DETECTION ---
query_params = st.query_params
office_key = query_params.get("f", "ralls").lower()

if office_key not in attorney_data:
    office_key = "ralls"

office = attorney_data[office_key]

# --- MODE ---
if "f" in query_params:
    app_mode = "Client: Sign Form"
else:
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Go to:", ["Marketer: Generate Link", "Client: Sign Form"])

    if app_mode == "Marketer: Generate Link":
        selected_display = st.sidebar.selectbox(
            "Select Office:",
            [attorney_data[k]["full_name"] for k in attorney_data]
        )
        for k, v in attorney_data.items():
            if v["full_name"] == selected_display:
                office_key = k
                office = v

# --- HEADER (unchanged structure, refined style) ---
st.markdown(f"""
<div style="
background-color: #1a1a1a;
padding: 25px;
border-radius: 12px;
text-align: center;
border-bottom: 5px solid {office['color']};
margin-bottom: 25px;
box-shadow: 0 3px 10px rgba(0,0,0,0.25);
">
<span style="
font-size: 30px;
color: {office['color']};
font-weight: bold;
font-family: 'Times New Roman', serif;
">
⚖️ {office['full_name']}
</span>
<div style="
font-size: 12px;
color: #ffffff;
letter-spacing: 2px;
text-transform: uppercase;
margin-top: 6px;
opacity: 0.85;
">
Professional Legal Services
</div>
</div>
""", unsafe_allow_html=True)

# --- MARKETER ---
if app_mode == "Marketer: Generate Link":

    st.subheader("Marketer Dispatch")
    st.write(f"Generating secure link for: **{office['full_name']}**")

    base_url = "https://legal---app-fwqqgehtna457ta8badeuo.streamlit.app/"
    final_link = f"{base_url}?f={office_key}"

    st.info("Client Access Link (Copy This):")
    st.code(final_link)

# --- CLIENT FORM ---
elif app_mode == "Client: Sign Form":

    # Agreement (FIXED DESIGN ONLY)
    st.markdown(f"""
    <div style="
    background-color: #ffffff;
    padding: 22px;
    border-radius: 10px;
    border: 1px solid #d1d5db;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    font-size: 14.5px;
    line-height: 1.6;
    margin-bottom: 20px;
    ">
    {office["fee_text"]}
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Incident & Contact Details")

    # Better alignment (same fields)
    col1, col2 = st.columns(2)
    with col1:
        c_name = st.text_input("Full Name")
        c_phone = st.text_input("Phone Number")
    with col2:
        c_email = st.text_input("Email Address")
        c_date_acc = st.date_input("Date of Accident", value=date.today())

    c_dob = ""
    c_ssn = ""

    if office["needs_extra"]:
        col3, col4 = st.columns(2)
        with col3:
            c_dob = st.text_input("Date of Birth (MM/DD/YYYY)")
        with col4:
            c_ssn = st.text_input("Last 4 of SSN", max_chars=4)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Representation Authorization")
    st.write(f"By signing below, I authorize **{office['full_name']}** to represent me regarding my claims.")

    signature = st.text_input("Type Full Name to Sign")

    # Button styling only
    st.markdown(f"""
    <style>
    div.stButton > button {{
        background-color: #1a1a1a;
        color: white;
        font-size: 16px;
        padding: 12px;
        border-radius: 8px;
        width: 100%;
        border-bottom: 4px solid {office['color']};
    }}
    </style>
    """, unsafe_allow_html=True)

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
