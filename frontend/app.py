import streamlit as st
import requests

st.title("📄 PDF Summarization App with Blockchain")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
store_on_blockchain = st.checkbox("Store Summary on Blockchain")

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post("http://127.0.0.1:8001/upload/", files=files, params={"store_on_blockchain": store_on_blockchain})
    
    if response.status_code == 200:
        result = response.json()
        st.write("API Response:", result)  # Debugging line
        if "summary" in result:
            st.write("**Summary:**", result["summary"])
        else:
            st.error("No summary found in response.")
        if store_on_blockchain and "tx_hash" in result:
            st.write("**Blockchain Tx Hash:**", result["tx_hash"])
    else:
        st.error(f"Error: {response.status_code}, {response.text}")

