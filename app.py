from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from googletrans import Translator
from langdetect import detect
import json

# Load FAQ Data
with open("faq_data.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

translator = Translator()
app = Flask(__name__)

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
    return "Sorry, please contact admin office."

# --- Twilio WhatsApp Route ---
@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.form.get("Body")

    # 1) Check Tanglish shortcuts
    tanglish_reply = handle_tanglish(incoming_msg)
    if tanglish_reply:
        final_answer = tanglish_reply
    else:
        # 2) Language detect + translate
        lang = detect(incoming_msg)
        query_en = translator.translate(incoming_msg, dest="en").text
        answer_en = get_answer(query_en)
        final_answer = translator.translate(answer_en, dest=lang).text

    # 3) Send back response
    resp = MessagingResponse()
    resp.message(final_answer)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

