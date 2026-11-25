import streamlit as st
from groq import Groq

# ==============================
# PAGE CONFIGURATION
# ==============================
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ==============================
# GROQ API KEY
# ==============================
# 👇 PUT YOUR GROQ API KEY HERE
GROQ_API_KEY = "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"

# Create Groq client
client = Groq(api_key=GROQ_API_KEY)

# ==============================
# CHATBOT UI
# ==============================
st.title("🤖 AI Chatbot")
st.caption("Powered by Streamlit + Groq")

# ==============================
# CHAT HISTORY
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==============================
# USER INPUT
# ==============================
user_prompt = st.chat_input("Ask me anything...")

if user_prompt:

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    # ==============================
    # GROQ API CALL
    # ==============================
    try:
        with st.chat_message("assistant"):

            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Answer clearly and accurately."
                    },
                    *st.session_state.messages
                ],
                temperature=0.7,
                max_tokens=1024
            )

            ai_response = response.choices[0].message.content

            st.markdown(ai_response)

        # Save AI response
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response
        })

    except Exception as e:
        st.error(f"Error: {e}")


# ==============================
# CLEAR CHAT BUTTON
# ==============================
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()