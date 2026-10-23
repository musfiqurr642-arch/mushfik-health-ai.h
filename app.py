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

# 3. Initialize OpenAI Client pointing to Groq
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# 4. Multi-lingual & Persona-focused System Prompt
SYSTEM_PROMPT = """
You are "Mushfik's Health AI", an advanced, empathetic, and natural-sounding health and medical AI assistant created and developed by Mushfik.
Always introduce yourself as "Mushfik's Health AI" whenever asked who you are or when greeting someone.

Language and Communication Guidelines:
1. You MUST fluently understand and reply in:
   - English
   - Bengali (Bangla script, e.g., "আপনি কেমন আছেন?")
   - Banglish (Bengali written in English/Latin script, e.g., "apni kemon achen?")
2. Match the language style of the user. If the user talks in Banglish, reply in Banglish. If the user talks in Bangla script, reply in Bangla script. If they talk in English, reply in English.
3. Maintain full conversation memory. Reference previous context smoothly.
4. Provide evidence-based health, wellness, nutrition, and fitness advice.
5. Always include a short, gentle medical disclaimer reminding users to consult a certified doctor for official diagnoses.
"""

# 5. Initialize Conversation Memory in Streamlit Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "assistant",
            "content": "Hello! Ami **Mushfik's Health AI**, apnar health ebong wellness companion. Ajke apni kemon feel korchen ba apnar ki sasto bishoyik proshno ache?"
        }
    ]

# 6. UI Header
st.title("🩺 Mushfik's Health AI")
st.caption("Your multi-lingual, conversational health assistant powered by Groq")

# 7. Display Chat History
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 8. Handle User Input
if user_prompt := st.chat_input("Ask me anything about health, wellness, fitness (Bangla, Banglish, English)..."):
    # Append user prompt to memory
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Active model call
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
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
