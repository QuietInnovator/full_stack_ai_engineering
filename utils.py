# Empty both utils and main
# Import streamlit and openai in utils
# 4 functions in utils: get text input , get select box, get business info, generate tagline
# Load the openai key at the beginning of the app
# This will get us ready for the whole app
import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_text_input():
    return st.text_input("Enter your text here")

def get_tone_select_box():
    return st.selectbox("Please select the tone of your tagline", ["Professional", "Funny", "Inspiring", "Motivational", "Educational", "Engaging", "Entertaining", "Informative", "Persuasive", "Creative", "Unique", "Catchy", "Memorable", "Engaging", "Entertaining", "Informative", "Persuasive", "Creative", "Unique", "Catchy", "Memorable"])

def get_business_info():
    return st.text_input("Enter your business info here")

def generate_tagline():
    return st.text_input("Enter your tagline here")

def get_business_info():


    st.subheader("Business Info")
    with st.expander("Business Info"):
        business_name = st.text_input("Business Name")
        business_description = st.text_area("Business Description")
        business_industry = st.text_input("Business Industry")
        business_unique_selling_point = st.text_input("Business Unique selling point")
        business_audience = st.text_input("Business Audience")

    st.subheader("Tagline Tone")
    tagline_tone = get_tone_select_box()

    return { "business_name": business_name, "business_description": business_description, "business_industry": business_industry, "business_unique_selling_point": business_unique_selling_point, "business_audience": business_audience, "tagline_tone": tagline_tone }


def generate_tagline(business_info):
    prompt = f"""
    Generate a tagline for the following business:
    Business Name: {business_info["business_name"]}
    Business Description: {business_info["business_description"]}
    Business Industry: {business_info["business_industry"]}
    Business Unique Selling Point: {business_info["business_unique_selling_point"]}
    Business Audience: {business_info["business_audience"]}
    Tagline Tone: {business_info["tagline_tone"]}

    Return the tagline in the following format:
    be concise and to the point
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content