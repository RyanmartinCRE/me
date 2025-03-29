import streamlit as st
import re

# === Sentiment Analyzer ===
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
    neutral_score  = sum(1 for word in neutral_keywords  if re.search(r'\b' + re.escape(word) + r'\b', email_text))

    total_score = positive_score - negative_score

    if total_score > 0:
        sentiment = "Positive"
    elif total_score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "score": total_score,
        "sentiment": sentiment,
        "positive_matches": positive_score,
        "negative_matches": negative_score,
        "neutral_matches": neutral_score
    }

# === Real Estate Pro Reply Generator ===
def generate_reply(sentiment_result, sender_name, your_name, topic, tone="Professional"):
    sentiment = sentiment_result["sentiment"]

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

    else:  # Professional (default)
        return f"""Dear {sender_name},

Thank you for your message regarding {topic}. I’ll review it and respond with any necessary details or next steps shortly.

Best regards,  
{your_name}"""

# === Streamlit UI ===
st.set_page_config(page_title="📬 Real Estate Reply Assistant", layout="centered")

st.title("📬 Real Estate Reply Assistant")
st.write("Drop in an email from your team or client. Get a reply in your chosen tone — fast and clean.")

email_text = st.text_area("✉️ Paste the email you received:", height=200)

your_name = st.text_input("Your Name", value="Ryan")
sender_name = st.text_input("Sender's Name", value="Jordan")
topic = st.text_input("What’s this about?", value="Lease Proposal")

tone = st.selectbox("Tone of your reply", ["Professional", "Friendly", "Assertive", "Empathetic", "Playful"])

if st.button("Analyze & Generate Reply"):
    if not email_text.strip():
        st.warning("Paste an email to analyze first.")
    else:
        result = analyze_sentiment(email_text)
        reply = generate_reply(result, sender_name, your_name, topic, tone)

        st.subheader("🔍 Sentiment Vibe")
        st.json(result)

        st.subheader("💬 Suggested Reply")
        st.code(reply)

        st.download_button(
            label="📋 Copy Reply (as .txt)",
            data=reply,
            file_name="reply.txt",
            mime="text/plain"
        )
