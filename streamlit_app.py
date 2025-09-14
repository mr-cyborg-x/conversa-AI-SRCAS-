import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
import json
import datetime

# Load FAQ Data from JSON
with open("faq_data.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

# ---------------- Language Helpers ----------------
def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def translate_to_english(text):
    try:
        return GoogleTranslator(source="auto", target="en").translate(text)
    except:
        return text

def translate_back(text, lang):
    if lang == "en":
        return text
    try:
        return GoogleTranslator(source="en", target=lang).translate(text)
    except:
        return text

# ---------------- Tanglish Handler ----------------
def handle_tanglish(user_input):
    text = user_input.lower()

    if "evlo" in text or "fees" in text or "fee" in text:
        return "Nanba, semester fees ₹15000 da 😎. Online pay panna mudiyum."
    elif "timetable" in text or "exam" in text or "schedule" in text:
        return "Inga da timetable link 👉 http://college.com/timetable"
    elif "hello" in text or "hi" in text or "vanakkam" in text:
        return "Vanakkam da! Enna help venum? 😇"
    elif "admission" in text or "join" in text:
        return "Admission process next month start aagum da. Apply pannunga 👉 http://college.com/admission"
    else:
        return None

# ---------------- Main Answer Logic ----------------
def get_answer(user_input):
    # 1) Tanglish shortcut check
    tanglish_reply = handle_tanglish(user_input)
    if tanglish_reply:
        return tanglish_reply

    # 2) FAQ JSON check
    user_input = user_input.lower()
    for key in faq_data:
        if key in user_input:
            return faq_data[key]

    # 3) Default fallback
    return "Sorry da, I don't know that 😅. Please contact admin office."

# ---------------- Logging ----------------
def log_conversation(user, bot):
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] USER: {user}\nBOT: {bot}\n\n")

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="College Multilingual + Tanglish Chatbot", page_icon="🎓")
st.title("🎓 Conversa AI – Multilingual + Tanglish Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if user_input := st.chat_input("Type your message..."):
    lang = detect_language(user_input)

    # Translate only if not Tanglish (Tanglish handled first)
    query_en = translate_to_english(user_input) if not handle_tanglish(user_input) else user_input

    answer_en = get_answer(query_en)
    final_answer = translate_back(answer_en, lang)

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": final_answer})
    log_conversation(user_input, final_answer)

    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(final_answer)

# Download logs
try:
    with open("chat_logs.txt", "r", encoding="utf-8") as f:
        logs = f.read()
    st.download_button("📥 Download Chat Logs", logs, file_name="chat_logs.txt")
except FileNotFoundError:
    st.info("No logs yet.")
