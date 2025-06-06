import streamlit as st
import utils

# Page configuration
st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")

st.title("🧮 Simple Calculator")

st.markdown("Enter two numbers, then click **Compute** to see the arithmetic results.")

# Input fields
col1, col2 = st.columns(2)
with col1:
    a = st.number_input("First number", value=0, step=1, format="%d", key="num_a")
with col2:
    b = st.number_input("Second number", value=0, step=1, format="%d", key="num_b")

# Compute button
if st.button("Compute"):
    st.subheader("Results")
    st.write(f"{a} + {b} = {utils.add(a, b)}")
    st.write(f"{a} - {b} = {utils.subtract(a, b)}")
    st.write(f"{a} × {b} = {utils.multiply(a, b)}")

    # Handle division by zero gracefully
    if b == 0:
        st.error("Cannot divide by zero.")
    else:
        st.write(f"{a} ÷ {b} = {utils.divide(a, b)}")