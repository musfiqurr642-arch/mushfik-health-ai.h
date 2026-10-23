import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(
    page_title="Mushfik's Health AI",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Mushfik's Health AI")
st.caption("Your advanced, conversational health assistant powered by Grok")

# 2. Sidebar API Key Input (For easy testing without secrets issue)
st.sidebar.header("⚙️ Settings")
api_key_input = st.sidebar.text_input(
    "Enter xAI API Key:", 
    type="password", 
    placeholder="xai-..."
)

# Fallback to Streamlit secrets if sidebar is empty
if not api_key_input:
    try:
        api_key_input = st.secrets["XAI_API_KEY"]
    except Exception:
        api_key_input = ""

# 3. System Prompt defining personality and health focus
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
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I am **Mushfik AI**, your advanced health and wellness companion. How are you feeling today, or what health topics would you like to explore?"
    })

# 5. Display Chat History
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. Handle User Input
if user_prompt := st.chat_input("Ask me anything about health, wellness, fitness..."):
    if not api_key_input:
        st.error("⚠️ Prothom e sidebar theke apnar xAI API key-ti din!")
    else:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Initialize OpenAI client with dynamic key
                client = OpenAI(
                    api_key=api_key_input,
                    base_url="https://api.x.ai/v1",
                )
                
                completion = client.chat.completions.create(
                    model="grok-2-latest",
                    messages=st.session_state.messages,
                    temperature=0.7,
                )
                full_response = completion.choices[0].message.content
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                full_response = f"⚠️ Error connecting to Grok API: {e}"
                message_placeholder.markdown(full_response)

        st.session_state.messages.append({"label": "assistant", "role": "assistant", "content": full_response})
