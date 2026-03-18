import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

st.set_page_config(page_title="Representation Portal", layout="centered", page_icon="⚖️")

# --- CUSTOM PROFESSIONAL STYLING ---
st.markdown("""
    <style>
    .legal-document {
        font-family: 'Times New Roman', Times, serif;
        text-align: justify;
        line-height: 1.6;
        background-color: #ffffff;
        color: #1a1a1a;
        padding: 40px;
        border: 1px solid #d3d3d3;
        border-radius: 4px;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    .signature-box {
        border: 2px solid #1a1a1a;
        padding: 20px;
        margin-top: 20px;
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        height: 3em;
        background-color: #1a1a1a;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA: Mapped to Short Keys ---
# Wording remains exactly as provided in your previous script
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
        "fee_text": """**CONTINGENT FEE AGREEMENT**

This agreement is voluntarily entered between the undersigned (Client) and McKenzie & Snyder LLP (Lawyer).

Client retains Lawyer to recover damages sustained in an accident on the date provided below.

In consideration of legal services, Client agrees to pay Lawyer **25% of the gross amount recovered**, whether by settlement or trial.

Lawyer accepts employment and will do all acts necessary to protect Client's rights.

If nothing is recovered, Lawyer receives no compensation. However, Client is obligated to pay all reasonable expenses that Client authorizes or that Lawyer deems necessary to advance the claim. Client authorizes Lawyer to deduct medical bills from the gross settlement, so that Lawyer may pay such bills on behalf of Client.

The undersigned certify that they have read and understand this agreement.""",
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#a3f2b5" # Green
    }
}

# --- 1. DETECTION LOGIC ---
query_params = st.query_params
office_key = query_params.get("f", "ralls").lower()

if office_key not in attorney_data:
    office_key = "ralls"

office = attorney_data[office_key]

# --- 2. APP MODES ---
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

# --- 3. DYNAMIC HEADER ---
if app_mode == "Client: Sign Form":
    st.markdown(
        f"""
        <div style="background-color: #1a1a1a; padding: 30px; border-radius: 8px; text-align: center; border-bottom: 8px solid {office['color']}; margin-bottom: 40px;">
            <div style="font-size: 12px; color: {office['color']}; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 10px;">Official Representation Portal</div>
            <span style="font-size: 38px; color: #ffffff; font-weight: bold; font-family: 'Times New Roman', Times, serif;">
                {office['full_name'].upper()}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f"""
        <div style="background-color: #1a1a1a; padding: 30px; border-radius: 8px; text-align: center; border-bottom: 8px solid #888888; margin-bottom: 40px;">
            <span style="font-size: 32px; color: #ffffff; font-weight: bold; font-family: 'Times New Roman', Times, serif;">
                ⚖️ Marketer Dispatch Console
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- 4. MARKETER DISPATCH ---
if app_mode == "Marketer: Generate Link":
    st.subheader("Link Configuration")
    st.write(f"Generating professional access link for: **{office['full_name']}**")
    
    base_url = "https://legal---app-fwqqgehtna457ta8badeuo.streamlit.app/"
    final_link = f"{base_url}?f={office_key}"
    
    st.info("Direct Client URL:")
    st.code(final_link, language=None)
    
    copy_html = f"""
    <div style="display: flex; justify-content: center; margin-top: 10px;">
        <style>
            .copy-btn {{
                background-color: #1a1a1a;
                border: 1px solid #ffffff;
                color: white;
                padding: 12px 30px;
                text-align: center;
                font-size: 14px;
                cursor: pointer;
                border-radius: 4px;
                transition: 0.2s;
            }}
            .copy-btn:active {{ transform: scale(0.98); opacity: 0.8; }}
        </style>
        <button class="copy-btn" onclick="navigator.clipboard.writeText('{final_link}')">
            COPY LINK TO CLIPBOARD
        </button>
    </div>
    """
    st.components.v1.html(copy_html, height=80)

# --- 5. CLIENT FORM ---
elif app_mode == "Client: Sign Form":
    # Styled Legal Agreement Container
    st.markdown(f'<div class="legal-document">{office["fee_text"]}</div>', unsafe_allow_html=True)
    
    with st.container():
        st.subheader("Step 1: Contact Information")
        col_a, col_b = st.columns(2)
        with col_a:
            c_name = st.text_input("Legal Full Name")
            c_email = st.text_input("Email Address")
        with col_b:
            c_phone = st.text_input("Mobile Phone Number")
            c_date_acc = st.date_input("Date of Incident", value=date.today())
        
        c_dob = ""
        c_ssn = ""
        if office["needs_extra"]:
            st.subheader("Step 2: Verification Details")
            col1, col2 = st.columns(2)
            with col1:
                c_dob = st.text_input("Date of Birth (MM/DD/YYYY)")
            with col2:
                c_ssn = st.text_input("Last 4 of SSN", max_chars=4)
        
        st.markdown('<div class="signature-box">', unsafe_allow_html=True)
        st.subheader("Step 3: Execution of Agreement")
        st.write(f"By typing your name below, you are electronically signing this agreement and authorizing **{office['full_name']}** to represent you.")
        signature = st.text_input("Electronic Signature (Type Full Name)")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("") # Spacer
        if st.button("EXECUTE & SUBMIT AGREEMENT"):
            if signature and c_name and c_phone:
                with st.spinner("Processing Secure Submission..."):
                    try:
                        sender_email = st.secrets["EMAIL_SENDER"]
                        sender_password = st.secrets["EMAIL_PASSWORD"]
                        
                        subject = f"EXECUTED AGREEMENT: {c_name} - {office['full_name']}"
                        body = f"Office: {office['full_name']}\nClient: {c_name}\nPhone: {c_phone}\nEmail: {c_email}\nAccident Date: {c_date_acc}\nDOB: {c_dob}\nSSN: {c_ssn}\nSignature: {signature}"
                        
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
                        st.success(f"Agreement successfully executed and sent to {office['full_name']}.")
                    except Exception as e:
                        st.error(f"Transmission Error: {e}")
            else:
                st.error("Please complete all required fields and provide your signature.")
