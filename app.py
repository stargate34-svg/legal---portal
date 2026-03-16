import streamlit as st

# Setup page config for a professional look on mobile
st.set_page_config(page_title="Representation Portal", layout="centered")

# --- DATA: Attorney Specifics ---
# These are pulled from your uploaded PDF contracts
attorney_data = {
    "Kylee Nizuryn": {
        "fee_text": "The Attorney shall receive one-third (1/3) of the total gross amount of recovery. In the event of no recovery, Client shall owe Attorney nothing for services rendered.",
        "needs_ssn": False
    },
    "Brian Duffy": {
        "fee_text": "Contingency Fee: 25% (1/4) for out-of-court settlement; 33% (1/3) if litigation is pursued. Expenses and medical bills are the sole responsibility of the Client.",
        "needs_ssn": True
    },
    "McKenzie & Snyder": {
        "fee_text": "Client agrees to pay Lawyer 25% of the gross amount of the recovery. If nothing is recovered, Lawyer shall receive no compensation.",
        "needs_ssn": True
    }
}

# --- NAVIGATION ---
# In a live app, you'd send the client a link that automatically selects "Client Mode"
app_mode = st.sidebar.radio("Navigation", ["Marketer: Generate Link", "Client: Sign Form"])

# ---------------------------------------------------------
# MODE 1: MARKETER GENERATES THE LINK
# ---------------------------------------------------------
if app_mode == "Marketer: Generate Link":
    st.title("Marketer Dispatch")
    st.write("Select the attorney the victim has requested to generate the SMS link.")
    
    selected_atty = st.selectbox("Assigning Attorney", list(attorney_data.keys()))
    
    # Generate the link (Replace 'your-app.streamlit.app' with your actual URL once deployed)
    base_url = "https://your-app.streamlit.app/"
    query_param = f"?firm={selected_atty.replace(' ', '+')}"
    final_link = base_url + query_param
    
    st.subheader("Link for SMS")
    st.info("Copy the link below and paste it into your text message to the victim.")
    st.code(final_link, language=None)

# ---------------------------------------------------------
# MODE 2: CLIENT FILLS OUT THE FORM
# ---------------------------------------------------------
elif app_mode == "Client: Sign Form":
    # Logic to auto-select the firm based on the link (if applicable)
    query_params = st.query_params
    default_firm = query_params.get("firm", "Kylee Nizuryn").replace("+", " ")
    
    st.title("Request for Representation")
    st.write(f"Form for: **{default_firm}**")
    
    # Show the specific legal terms
    st.warning(attorney_data[default_firm]["fee_text"])
    
    st.subheader("Your Information")
    c_name = st.text_input("Full Name")
    
    # Only show SSN/DOB if the specific attorney requires it
    if attorney_data[default_firm]["needs_ssn"]:
        col1, col2 = st.columns(2)
        with col1:
            c_dob = st.date_input("Date of Birth", value=None)
        with col2:
            c_ssn = st.text_input("Social Security Number (Last 4)")
            
    c_accident_date = st.date_input("Date of Accident")
    c_phone = st.text_input("Phone Number")
    c_email = st.text_input("Email Address")
    
    st.markdown("---")
    st.subheader("Electronic Signature")
    st.write(f"By signing below, I am requesting that {default_firm} represent me regarding my accident.")
    
    signature = st.text_input("Type Full Name to Sign")
    
    if st.button("Submit Signed Request"):
        if signature and c_name:
            st.success("Thank you. Your request has been submitted successfully.")
        else:
            st.error("Please provide your name and signature.")