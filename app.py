import streamlit as st
from googletrans import Translator
from langdetect import detect
import json
import datetime

# Load FAQ Data
with open("faq_data.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

translator = Translator()

# --- Tanglish Handler ---
def handle_tanglish(query):
    text = query.lower()
    if "evlo" in text or "fees" in text or "fee" in text:
        return "Nanba, semester fees ₹15000 da 😎. Online pay panna mudiyum."
    elif "timetable" in text or "exam" in text or "schedule" in text:
        return "Inga da timetable link 👉 http://college.com/timetable"
    elif "hello" in text or "hi" in text or "vanakkam" in text:
        return "Vanakkam da! Enna help venum? 😇"
    elif "admission" in text or "join" in text:
        return "Admission process next month start aagum da. Apply pannunga 👉 http://college.com/admission"
    return None

# --- FAQ Answer Logic ---
def get_answer(query):
    query = query.lower()
    for key in faq_data:
        if key in query:
            return faq_data[key]
    return "Sorry da 😅, please contact admin office."

# --- Logging ---
def log_conversation(user, bot):
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] USER: {user}\nBOT: {bot}\n\n")

# --- Streamlit UI ---
st.set_page_config(page_title="College Chatbot", page_icon="🎓")
st.title("🎓 Conversa AI – Multilingual + Tanglish Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if user_input := st.chat_input("Type your message..."):
    tanglish_reply = handle_tanglish(user_input)

    if tanglish_reply:
        final_answer = tanglish_reply
    else:
        lang = detect(user_input)
        query_en = translator.translate(user_input, dest="en").text
        answer_en = get_answer(query_en)
        final_answer = translator.translate(answer_en, dest=lang).text

    # Store chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": final_answer})
    log_conversation(user_input, final_answer)

    # Display current chat
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

