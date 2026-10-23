import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(
    page_title="Mushfik's Health AI",
    page_icon="🩺",
    layout="centered"
)

# 2. Direct Groq API Key
GROQ_API_KEY = "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"

# 3. Initialize Client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# 4. System Prompt
SYSTEM_PROMPT = """
You are "Mushfik AI", an advanced, highly empathetic, and natural-sounding health and medical AI assistant. 
Your creator/developer is Mushfik. 
Always introduce yourself naturally if asked who you are, maintaining a warm, conversational, human-like tone—just like top-tier modern AIs.
You have full conversation memory of the ongoing chat. Reference previous questions and answers naturally when relevant to give a continuous, flowing discussion.
Provide advanced, evidence-based health, wellness, nutrition, and fitness insights, but always include a gentle medical disclaimer reminding users to consult a certified healthcare professional for formal diagnoses.
"""

# 5. Initialize Conversation Memory in Streamlit Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "assistant",
            "content": "Hello! I am **Mushfik AI**, your advanced health and wellness companion. How are you feeling today, or what health topics would you like to explore?"
        }
    ]

# 6. UI Header
st.title("🩺 Mushfik's Health AI")
st.caption("Your advanced, conversational health assistant powered by Groq")

# 7. Display Chat History
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 8. Handle User Input
if user_prompt := st.chat_input("Ask me anything about health, wellness, fitness..."):
    # Append user prompt to memory
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Using the stable, universally supported classic Groq model
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=st.session_state.messages,
                temperature=0.7,
            )
            
            full_response = completion.choices[0].message.content
            message_placeholder.markdown(full_response)
            
            # Save model response to memory
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            error_msg = f"⚠️ Connection Error: {e}"
            message_placeholder.markdown(error_msg)
