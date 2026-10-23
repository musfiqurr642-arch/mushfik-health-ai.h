import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="Mushfik's Health AI",
    page_icon="🩺",
    layout="centered"
)

# 2. Get API Key securely from Streamlit Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    # Ekhane apnar asol AI Studio key-ti bosaben (jar shuruhat AQ... diye)
    API_KEY = "AQ.Ab8RN6iTJTM7BiMS-KwLcH74kD-EU6mHO1pU0NsT7NkFXDUnYg"

# 3. System Prompt
SYSTEM_INSTRUCTION = """
You are "Mushfik AI", an advanced, highly empathetic, and natural-sounding health and medical AI assistant. 
Your creator/developer is Mushfik. 
Always introduce yourself naturally if asked who you are, maintaining a warm, conversational, human-like tone—just like top-tier modern AIs.
You have full conversation memory of the ongoing chat. Reference previous questions and answers naturally when relevant to give a continuous, flowing discussion.
Provide advanced, evidence-based health, wellness, nutrition, and fitness insights, but always include a gentle medical disclaimer reminding users to consult a certified healthcare professional for formal diagnoses.
"""

# 4. Initialize Chat Memory in Session State (Using standard dictionary structure)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "model",
            "content": "Hello! I am **Mushfik AI**, your advanced health and wellness companion. How are you feeling today, or what health topics would you like to explore?"
        }
    ]

# 5. UI Header
st.title("🩺 Mushfik's Health AI")
st.caption("Your advanced, conversational health assistant powered by Google Gemini")

# 6. Display Chat History
for message in st.session_state.messages:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(message["content"])

# 7. Handle User Input
if user_prompt := st.chat_input("Ask me anything about health, wellness, fitness..."):
    # Append user prompt
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Initialize client fresh for request
            client = genai.Client(api_key=API_KEY)
            
            # Format contents for Gemini SDK properly
            contents_payload = []
            for msg in st.session_state.messages:
                contents_payload.append(
                    types.Content(
                        role=msg["role"],
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )

            # Generate response from model
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents_payload,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.7,
                )
            )
            
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            # Save assistant response to memory
            st.session_state.messages.append({"role": "model", "content": full_response})

        except Exception as e:
            full_response = f"⚠️ Error connecting to Gemini API: {e}"
            message_placeholder.markdown(full_response)
