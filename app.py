import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

st.set_page_config(page_title="Representation Portal", layout="centered", page_icon="⚖️")

# --- DATA: Mapped to Short Keys for reliability ---
attorney_data = {
    "ralls": {
        "full_name": "Ralls Legal Representation",
        "fee_text": """The undersigned, hereinafter (Client), retains the undersigned, hereinafter (Attorney) for representation for Personal Injuries. Attorney(s) will devote their full professional abilities to Client's case. Client understands that the claim may be handled by one or more of the members, staff, or associates of Attorney. Client shall not pay Attorney an upfront fee because Attorney shall work on a contingent fee only. For their fee, Attorney shall receive one‑third (1/3) of the total gross amount of recovery of any settlement.

Accordingly. in the event of no recovery, Client shall owe Attorney nothing for services rendered.""",
        "needs_extra": False,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#f2e1a3"
    },
    "ohio": {
        "full_name": "Ohio Injury Attorneys",
        "fee_text": """**CONTRACT FOR REPRESENTATION**

> I ("the Client") agree to retain and employ Ohio Injury Attorneys
> ("the Firm") to represent me for my injury claim. The following terms
> shall apply: 

(1) **Contingency Fee.** The Firm shall receive a contingency fee of 25% (1/4) of all funds collected for a settlement obtained without litigation. If the Client and the Firm agree to pursue litigation, the Firm shall receive a contingency fee of 33% (1/3) of all funds collected.

(2) **Expenses.** The Firm shall be reimbursed for all reasonable expenses necessary to pursue the Client's claim including, but not limited to, invoices required to obtain medical documentation, court costs, and payment for expert testimony.

> A. The Firm is not obligated advance funds on the Client's behalf. At the conclusion of representation, the Firm shall be reimbursed for case expenses.
>
> B. Expenses are not included in the Firm's contingency fee.
>
> C. The Firm shall provide an itemization of all case expenses.

(3) **Medical Bills.** The Firm is under no obligation to pay medical bills on the Client's behalf. Medical bills are the sole responsibility of the Client. At the conclusion of the case, the Firm will pay medical bills at the client's direction.

(4) **Liens.** At the conclusion of the claim, the Firm may be obligated to pay a medical lien, subrogation lien, or lien from some other third party out of the distribution of case proceeds. The Client shall contact the Firm if the Client is notified by a third party regarding a lien on the case.

(5) **Termination by Client.** Client may terminate representation at any time, but the Firm shall be compensated for the work performed. If the Firm has obtained a settlement offer, the Firm shall be compensated based on a contingency fee percentage of the highest offer prior to termination. If the Firm is terminated prior to receiving a settlement offer, Client shall compensate the Firm for work performed. No fee will be owed to the Firm if the Firm is unable to resolve the Client’s claim or if the Firm agrees in writing to waive its fee.

(6) **Termination by the Firm.** The Firm may terminate the Contract for Representation for good cause.

(7) **Medical Authorization.** When required, the Client grants the Firm permission to update any signed medical authorization in order to request and obtain necessary medical documentation. If the Firm is attempting to negotiation bill reductions, Client authorizes the Firm to disclose case information to medical providers.

(8) **Worker's Compensation.** Client permits Firm to share Client identifiers with Nager, Romaine, and Schneiberg for potential Worker's Compensation claims.

(9) **Special Terms.**
_________________________________________________________________

By signing below, the Client agrees to the terms and conditions of this contract.""",
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#a3c2f2"
    },
    "mckenzie": {
        "full_name": "Mckenzie & Snyder Legal Representation",
        "fee_text": "",  # Not used for this office
        "needs_extra": True,
        "target_email": "tgottardi@advanced-spinal-care.com",
        "color": "#a3f2b5"
    }
}

# --- DETECTION LOGIC ---
query_params = st.query_params
office_key = query_params.get("f", "ralls").lower()
if office_key not in attorney_data:
    office_key = "ralls"
office = attorney_data[office_key]

# --- APP MODES ---
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

# --- HEADER ---
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

# --- MARKETER DISPATCH ---
if app_mode == "Marketer: Generate Link":
    st.subheader("Marketer Dispatch")
    st.write(f"Generating secure link for: **{office['full_name']}**")
    base_url = "https://legal---app-fwqqgehtna457ta8badeuo.streamlit.app/"
    final_link = f"{base_url}?f={office_key}"
    st.info("Client Access Link (Copy This):")
    st.code(final_link, language=None)
    copy_html = f"""
    <div style="display: flex; justify-content: center; margin-top: 10px;">
        <style>
            .copy-btn {{
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                transition: all 0.1s ease;
            }}
            .copy-btn:hover {{ background-color: #45a049; }}
            .copy-btn:active {{ transform: scale(0.95); background-color: #3d8b40; }}
        </style>
        <button class="copy-btn" onclick="navigator.clipboard.writeText('{final_link}')">
            📋 Copy Link to Clipboard
        </button>
    </div>
    """
    st.components.v1.html(copy_html, height=80)

# --- CLIENT FORM (or intake info for McKenzie) ---
elif app_mode == "Client: Sign Form":
    if office_key == "mckenzie":
        # Show only the intake protocol information (without names)
        st.markdown(
            """
            ### Intake Team Transfer Protocol

            **Primary Contact Method:**  
            For all live transfers, connect directly to the Intake Team at:  
            **1.513.788.4699**

            **Hours of Availability:**  
            - Monday – Tuesday: 9:00 AM – 6:00 PM  
            - Wednesday – Friday: 9:00 AM – 8:00 PM  
            - Saturday – Sunday: 12:00 PM – 8:00 PM
            """
        )
    else:
        # Normal client intake form for Ralls and Ohio
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
        
        agree = st.checkbox("I confirm that I have read and agree to the terms above.")
        
        if st.button("Submit Signed Request"):
            if signature and c_name and c_phone and agree:
                with st.spinner("Submitting..."):
                    try:
                        sender_email = st.secrets["EMAIL_SENDER"]
                        sender_password = st.secrets["EMAIL_PASSWORD"]
                        
                        # --- Build HTML attachment content ---
                        html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Signed Agreement</title></head>
<body style="font-family: Arial, sans-serif; max-width: 800px; margin: 20px auto;">
    <h2 style="text-align: center; color: #2c5f8a;">SIGNED REPRESENTATION AGREEMENT</h2>
    <hr style="border: 1px solid #2c5f8a;">
    <h3>{office['full_name']}</h3>
    <div style="background-color: #f5f7fa; padding: 15px; border-left: 4px solid #2c5f8a;">
        <pre style="font-family: Arial, sans-serif; white-space: pre-wrap;">{office['fee_text']}</pre>
    </div>
    <h3>CLIENT INFORMATION</h3>
    <table style="width: 100%; border-collapse: collapse;">
        <tr><td style="padding: 6px;"><strong>Full Name:</strong></td><td>{c_name}</td>
        <tr><td style="padding: 6px;"><strong>Accident Date:</strong></td><td>{c_date_acc}</td>
        <tr><td style="padding: 6px;"><strong>Phone:</strong></td><td>{c_phone}</td>
        <tr><td style="padding: 6px;"><strong>Email:</strong></td><td>{c_email}</td>
        <tr><td style="padding: 6px;"><strong>Date of Birth:</strong></td><td>{c_dob if c_dob else 'Not provided'}</td>
        <tr><td style="padding: 6px;"><strong>Last 4 SSN:</strong></td><td>{c_ssn if c_ssn else 'Not provided'}</td>
     </table>
    <h3>SIGNATURE</h3>
    <p><strong>Signed by:</strong> {signature}</p>
    <p><strong>Date signed:</strong> {date.today().strftime('%B %d, %Y')}</p>
    <hr>
    <p style="text-align: center; color: gray;">This document was generated electronically.</p>
</body>
</html>"""
                        
                        # --- Create email ---
                        subject = f"NEW SIGNED REQUEST: {c_name} - {office['full_name']}"
                        body = f"Office: {office['full_name']}\nClient: {c_name}\nPhone: {c_phone}\nEmail: {c_email}\nAccident Date: {c_date_acc}\nDOB: {c_dob}\nSSN: {c_ssn}\n\nA signed HTML agreement is attached."
                        
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = office["target_email"]
                        msg['Subject'] = subject
                        
                        # Attach body text
                        msg.attach(MIMEText(body, 'plain'))
                        
                        # Attach the agreement as an HTML file
                        attachment = MIMEText(html_content, 'html')
                        attachment.add_header(
                            'Content-Disposition',
                            'attachment',
                            filename=f"signed_agreement_{c_name.replace(' ', '_')}.html"
                        )
                        msg.attach(attachment)
                        
                        # Send email
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.send_message(msg)
                        server.quit()
                        
                        st.success(f"Sent successfully to {office['full_name']}. An HTML copy of the signed agreement is attached.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                missing = []
                if not signature:
                    missing.append("signature")
                if not c_name:
                    missing.append("full name")
                if not c_phone:
                    missing.append("phone number")
                if not agree:
                    missing.append("agreement checkbox")
                st.error(f"Missing required fields: {', '.join(missing)}.")
