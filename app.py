import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(
    page_title="Mushfik's Health AI",
    page_icon="🩺",
    layout="centered"
)

# 2. Configure Google Gemini API
GOOGLE_API_KEY = "AQ.Ab8RN6I-KbDE4MyQ6v1UuDAAapdmGcI6lgZni7eFUK_rFXYOeg"  # Ekhane apnar AI Studio API key din

genai.configure(api_key=GOOGLE_API_KEY)

# 3. System Prompt defining personality and health focus
SYSTEM_INSTRUCTION = """
You are "Mushfik AI", an advanced, highly empathetic, and natural-sounding health and medical AI assistant. 
Your creator/developer is Mushfik. 
Always introduce yourself naturally if asked who you are, maintaining a warm, conversational, human-like tone—just like top-tier modern AIs.
You have full conversation memory of the ongoing chat. Reference previous questions and answers naturally when relevant to give a continuous, flowing discussion.
Provide advanced, evidence-based health, wellness, nutrition, and fitness insights, but always include a gentle medical disclaimer reminding users to consult a certified healthcare professional for formal diagnoses.
"""

# Model configuration with system instruction
generation_config = {
    "temperature": 0.7,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=SYSTEM_INSTRUCTION
)

# 4. Initialize Chat History in Streamlit Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Initial greeting from the AI
    st.session_state.messages.append({
        "role": "model",
        "parts": ["Hello! I am **Mushfik AI**, your advanced health and wellness companion. How are you feeling today, or what health topics would you like to explore?"]
    })

# 5. UI Header
st.title("🩺 Mushfik's Health AI")
st.caption("Your advanced, conversational health assistant powered by Google Gemini")

# 6. Display Chat History
for message in st.session_state.messages:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(message["parts"][0])

# 7. Handle User Input
if user_prompt := st.chat_input("Ask me anything about health, wellness, fitness..."):
    # Append user message to memory
    st.session_state.messages.append({"role": "user", "parts": [user_prompt]})
    
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Convert Streamlit history to Gemini chat format for memory connection
            chat_history = []
            for msg in st.session_state.messages[:-1]:
                chat_history.append({
                    "role": msg["role"],
                    "parts": msg["parts"]
                })
            
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(user_prompt)
            full_response = response.text
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            full_response = f"⚠️ Error connecting to Gemini API: {e}"
            message_placeholder.markdown(full_response)

    # Save assistant response to session state memory
    st.session_state.messages.append({"role": "model", "parts": [full_response]})
