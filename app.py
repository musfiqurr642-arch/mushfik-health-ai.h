import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(
    page_title="Mushfik's Health AI",
    page_icon="🩺",
    layout="centered"
)

# 2. Initialize xAI Grok Client
# Replace with your actual xAI API Key or set it as an environment variable (XAI_API_KEY)
# Get your key from: https://console.x.ai/
XAI_API_KEY = "your_xai_api_key_here"  # Or use os.getenv("XAI_API_KEY")

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",  # xAI official API endpoint
)

# 3. System Prompt defining personality, memory capability, and health focus
SYSTEM_PROMPT = """
You are "Mushfik AI", an advanced, highly empathetic, and natural-sounding health and medical AI assistant. 
Your creator/developer is Mushfik. 
Always introduce yourself naturally if asked who you are, maintaining a warm, conversational, human-like tone—just like top-tier modern AIs.
You have full conversation memory of the ongoing chat. Reference previous questions and answers naturally when relevant to give a continuous, flowing discussion.
Provide advanced, evidence-based health, wellness, nutrition, and fitness insights, but always include a gentle medical disclaimer reminding users to consult a certified healthcare professional for formal diagnoses.
"""

# 4. Initialize Chat History in Streamlit Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    # Initial greeting from the AI to set the persona
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I am **Mushfik AI**, your advanced health and wellness companion. How are you feeling today, or what health topics would you like to explore?"
    })

# 5. UI Header
st.title("🩺 Mushfik's Health AI")
st.caption("Your advanced, conversational health assistant powered by Grok")

# 6. Display Chat History (Skipping the system prompt visual display)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 7. Handle User Input
if user_prompt := st.chat_input("Ask me anything about health, wellness, fitness..."):
    # Append user message to state memory
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate response from Grok API with full history context
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Call Grok model (grok-beta or grok-2)
            completion = client.chat.completions.create(
                model="grok-2-latest",  # You can also use "grok-beta"
                messages=st.session_state.messages,
                temperature=0.7,
            )
            
            full_response = completion.choices[0].message.content
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            full_response = f"⚠️ Error connecting to Grok API: {e}"
            message_placeholder.markdown(full_response)

    # Save assistant response to session state memory
    st.session_state.messages.append({"role": "assistant", "content": full_response})
