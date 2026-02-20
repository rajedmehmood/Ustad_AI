import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Ustad AI - Exam Helper",
    page_icon="📚",
    layout="centered"
)

# --- HEADER & STYLE ---
st.title("📚 Ustad AI")
st.subheader("Tera Personal Tutor for Matric & FSc!")
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.write("Upload a picture of your textbook (Physics, Bio, Chem, etc.), and I will explain it in **Roman Urdu** with desi examples!")

# --- API SETUP (SECURE) ---
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        st.error("🚨 API Key configuration error. Please set GOOGLE_API_KEY in Hugging Face Settings > Secrets.")
        st.stop()

# Configure the AI model
try:
    genai.configure(api_key=api_key)
    # SWITCHING TO GEMINI 2.5 FLASH TO USE A DIFFERENT QUOTA BUCKET
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"Error configuring API: {e}")
    st.stop()

# --- THE SYSTEM PROMPT ---
system_prompt = """
You are 'Ustad AI', a friendly, encouraging, and witty tutor for Pakistani Matric/FSc students.

RULES:
1. **Language:** Explain primarily in **Roman Urdu** (Urdu written in English script) mixed with simple English terms.
2. **Tone:** Be like a supportive older brother or a favorite teacher. Use phrases like "Beta," "Fikar na karo," or "Samjh aya?".
3. **Analogy Rule:** You MUST explain concepts using **Pakistani cultural examples**.
    - Cricket (Babar Azam, Shaheen Afridi)
    - Food (Biryani, Nihari, Chai, Dhaba)
    - Daily Life (Rickshaws, Traffic, Load shedding, Metro Bus)
4. **Structure:**
    - **Concept:** One line definition in English.
    - **Asaan Urdu Mein:** Detailed explanation in Roman Urdu.
    - **Desi Misal (Analogy):** The cultural example.
    - **Exam Tip:** A pro tip for scoring marks.

GOAL: Make the student smile and understand the concept instantly.
"""

# --- IMAGE UPLOAD SECTION ---
uploaded_file = st.file_uploader("📸 Upload Textbook Page or Diagram", type=["jpg", "png", "jpeg", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Your Textbook Page', use_column_width=True)

    user_question = st.text_input("Koi khaas sawal hai? (Optional)", placeholder="E.g., Is diagram ko samjha den...")

    if st.button("Ustad Ji, Samjha Dein! 🚀"):
        with st.spinner("Ustad Ji is thinking... (Analyzing Image) 👓"):
            try:
                if user_question:
                    final_prompt = f"{system_prompt}\n\nStudent asks: {user_question}"
                else:
                    final_prompt = f"{system_prompt}\n\nExplain the main concept in this image."

                response = model.generate_content([final_prompt, image])
                
                st.markdown("### 📝 Ustad AI ka Jawab")
                st.write(response.text)
                st.balloons()

            except Exception as e:
                st.error(f"Something went wrong: {e}")
                if "429" in str(e):
                    st.warning("⚠️ High Traffic: The AI is busy. Please create a NEW Google API Key with a different Google Account to fix this instantly.")

# --- FOOTER ---
st.markdown("---")
st.caption("Built for HEC GenAI Hackathon | Powered by Google Gemini 2.5 Flash")
