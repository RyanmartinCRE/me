import streamlit as st
from openai import OpenAI
import re

# === Connect to OpenAI ===
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# === Analyze sentiment from text ===
def analyze_sentiment(email_text):
    email_text = email_text.lower()

    positive_keywords = [
        "good", "great", "excellent", "happy", "thank you", "thanks", "appreciate",
        "helpful", "awesome", "fantastic", "amazing", "best", "glad", "eager", "excited",
        "pleased", "positive"
    ]
    negative_keywords = [
        "bad", "terrible", "awful", "unhappy", "disappointed", "frustrated", "angry",
        "problem", "issue", "concern", "delay", "late", "wrong", "difficult", "not good", "never"
    ]
    neutral_keywords = [
        "information", "question", "request", "regarding", "following up", "update",
        "meeting", "schedule", "consider", "let me know", "understand"
    ]

    positive_score = sum(1 for word in positive_keywords if re.search(r'\b' + re.escape(word) + r'\b', email_text))
    negative_score = sum(1 for word in negative_keywords if re.search(r'\b' + re.escape(word) + r'\b', email_text))
    neutral_score = sum(1 for word in neutral_keywords if re.search(r'\b' + re.escape(word) + r'\b', email_text))

    total_score = positive_score - negative_score
    sentiment = "Neutral"
    if total_score > 0:
        sentiment = "Positive"
    elif total_score < 0:
        sentiment = "Negative"

    return {
        "score": total_score,
        "sentiment": sentiment,
        "positive_matches": positive_score,
        "negative_matches": negative_score,
        "neutral_matches": neutral_score
    }

# === Template-Based Reply (Classic) ===
def generate_template_reply(sentiment_result, sender_name, your_name, topic, tone="Professional"):
    if tone == "Friendly":
        return f"""Hey {sender_name},

Thanks for your message about {topic}. I’ll take a look and circle back shortly.

Appreciate the heads-up — let’s keep it moving.

Best,  
{your_name}"""

    elif tone == "Assertive":
        return f"""Hi {sender_name},

Got your note regarding {topic}. I’ll take it from here and follow up if anything else is needed.

Thanks for keeping me in the loop.

– {your_name}"""

    elif tone == "Empathetic":
        return f"""Hi {sender_name},

Thanks for flagging this about {topic}. I completely understand where you’re coming from and I’m giving it my full attention.

Appreciate your patience — I’ll keep you updated.

Warm regards,  
{your_name}"""

    elif tone == "Playful":
        return f"""Yo {sender_name},

Got your message about {topic} — loud and clear.  
I’m on it like a broker on a commission check 😎

Talk soon,  
{your_name}"""

    else:  # Professional
        return f"""Dear {sender_name},

Thank you for your message regarding {topic}. I’ll review it and respond with any necessary details or next steps shortly.

Best regards,  
{your_name}"""

# === AI-Powered Reply using GPT-3.5 ===
def generate_ai_reply(email_text, tone, your_name, sender_name, topic):
    system_prompt = f"""
You are a commercial real estate broker writing professional email replies.

Write a clear, helpful response to the email below, based on this context:
- Sender: {sender_name}
- Topic: {topic}
- Your name: {your_name}
- Desired tone: {tone.lower()}

Keep the message concise but thoughtful. DO NOT just copy the original text. Speak directly to the sender and sound human.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": email_text}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

# === Streamlit UI ===
st.set_page_config(page_title="📬 Real Estate Reply Assistant", layout="wide")
st.markdown("<h1 style='text-align: center;'>📬 Real Estate Reply Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Paste an email → Choose tone + mode → Get a smart reply.</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Email Received")
    email_text = st.text_area("Paste the email here:", height=280, label_visibility="collapsed")

    your_name = st.text_input("Your Name", value="Ryan")
    sender_name = st.text_input("Sender's Name", value="Jordan")
    topic = st.text_input("Topic / Subject", value="Lease Proposal")

    tone = st.selectbox("Tone of the Reply", ["Professional", "Friendly", "Assertive", "Empathetic", "Playful"])
    mode = st.radio("Reply Mode", ["🤖 AI-Powered", "📄 Template-Based"])

    if st.button("🚀 Generate Reply"):
        if not email_text.strip():
            st.warning("Paste an email first.")
        else:
            sentiment_result = analyze_sentiment(email_text)
            if mode == "🤖 AI-Powered":
                reply = generate_ai_reply(email_text, tone, your_name, sender_name, topic)
            else:
                reply = generate_template_reply(sentiment_result, sender_name, your_name, topic, tone)

            st.session_state["analysis"] = sentiment_result
            st.session_state["reply"] = reply

with col2:
    if "analysis" in st.session_state and "reply" in st.session_state:
        st.subheader("🔍 Sentiment Vibe")
        st.json(st.session_state["analysis"])

        st.subheader("✉️ Smart Reply")
        st.code(st.session_state["reply"], language="markdown")

        st.download_button(
            label="📋 Copy Reply (Download as .txt)",
            data=st.session_state["reply"],
            file_name="reply.txt",
            mime="text/plain"
        )
    else:
        st.markdown("Waiting for input on the left 👈")
