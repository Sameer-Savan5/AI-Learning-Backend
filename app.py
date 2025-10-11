import streamlit as st
import requests

# -----------------------------
# CONFIG
# -----------------------------
# Replace this URL with your deployed backend
API_URL = "http://127.0.0.1:10000"  # ✅ deployed FastAPI backend URL

st.set_page_config(page_title="AI Learning", page_icon="🤖", layout="wide")

# -----------------------------
# TITLE
# -----------------------------
st.title("🤖 AI Learning Platform (Debug Mode)")

# -----------------------------
# TEST CONNECTION
# -----------------------------
try:
    res = requests.get(f"{API_URL}/")
    if res.status_code == 200:
        st.success("✅ Connected to FastAPI backend successfully!")
        st.json(res.json())
    else:
        st.error(f"❌ Connection failed with status: {res.status_code}")
except Exception as e:
    st.error(f"Error connecting to backend: {e}")

# -----------------------------
# MANUAL TEST TABS
# -----------------------------
tabs = st.tabs(["Courses", "Chat", "Generate Text"])

# --- Courses ---
with tabs[0]:
    st.subheader("Courses")
    try:
        res = requests.get(f"{API_URL}/courses")
        if res.status_code == 200:
            st.json(res.json())
        else:
            st.error("Failed to load courses.")
    except Exception as e:
        st.error(f"Error: {e}")

# --- Chat ---
with tabs[1]:
    st.subheader("Chat with AI")
    msg = st.text_input("Enter message:")
    if st.button("Send"):
        res = requests.post(f"{API_URL}/chat", json={"message": msg})
        st.write(res.json())

# --- Generate Text ---
with tabs[2]:
    st.subheader("Generate Text")
    prompt = st.text_area("Enter prompt:")
    if st.button("Generate"):
        res = requests.post(f"{API_URL}/generate-text", json={"prompt": prompt})
        st.write(res.json())