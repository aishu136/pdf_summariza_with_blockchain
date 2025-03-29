import streamlit as st
import requests

st.title("📄 PDF Summarization App with Blockchain")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
store_on_blockchain = st.checkbox("Store Summary on Blockchain")

# Model selection
model = st.selectbox("Choose Summarization Model", ["transformers", "ollama", "langchain"])

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    params = {"model": model, "store_on_blockchain": store_on_blockchain}
    
    response = requests.post("http://127.0.0.1:8001/upload/", files=files, params=params)
    
    if response.status_code == 200:
        result = response.json()
        st.write("**Summary:**", result["summary"])
        if store_on_blockchain:
            st.write("**Blockchain Tx Hash:**", result["tx_hash"])
    else:
        st.error("Error processing the request.")

