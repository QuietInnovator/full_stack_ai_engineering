import streamlit as st
import utils
import openai

# Page configuration
st.set_page_config(page_title="tagline generator", page_icon="🧮", layout="centered")

st.title("🧮 tagline generator")

openai.api_key = st.secrets["OPENAI_API_KEY"]

business_info = utils.get_business_info()

if st.button("Submit"):
    if business_info:
        st.subheader("Tagline")
        tagline = utils.generate_tagline(business_info)
        st.write(tagline)
        st.subheader("Business Info")
        st.write(business_info)
    else:
        st.info("No business information provided yet.")


