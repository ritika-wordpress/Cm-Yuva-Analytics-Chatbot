import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CM YUVA AI Agent",
    layout="wide"
)

st.title("CM YUVA AI Analytics Agent")

# ---------------------------------------------------
# Upload CSV Files
# ---------------------------------------------------

st.sidebar.header("Upload CSV Files")

certification = st.sidebar.file_uploader(
    "Certification CSV",
    type=["csv"]
)

loan = st.sidebar.file_uploader(
    "Loan CSV",
    type=["csv"]
)

fraud = st.sidebar.file_uploader(
    "Fraud CSV",
    type=["csv"]
)

# ---------------------------------------------------
# Upload Button
# ---------------------------------------------------

if st.sidebar.button("Upload Data"):

    if certification and loan and fraud:

        files = {

            "certification": (
                certification.name,
                certification,
                "text/csv"
            ),

            "loan": (
                loan.name,
                loan,
                "text/csv"
            ),

            "fraud": (
                fraud.name,
                fraud,
                "text/csv"
            )
        }

        with st.spinner("Uploading and processing data..."):

            try:

                response = requests.post(
                    f"{API_URL}/upload-data",
                    files=files,
                    timeout=120
                )

                result = response.json()

                st.sidebar.success(result["message"])

            except Exception as e:

                st.sidebar.error(str(e))

# ---------------------------------------------------
# AI CHATBOT
# ---------------------------------------------------

st.header("AI Analytics Chatbot")

query = st.text_area(
    "Ask any business or analytics question"
)

if st.button("Generate Insights"):

    if not query.strip():

        st.warning("Please enter a question")

    else:

        with st.spinner("Generating insights..."):

            try:

                response = requests.post(

                    f"{API_URL}/chat",

                    json={
                        "question": query
                    },

                    timeout=120
                )

                result = response.json()

                st.write(result["response"])

            except Exception as e:

                st.error(str(e))