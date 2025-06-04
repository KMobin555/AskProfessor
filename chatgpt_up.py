import streamlit as st

st.set_page_config(page_title="ChatGPT UI", layout="centered")

# Title
st.title("💬 ChatGPT-Like Assistant")

# Session State to Store Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Area
prompt = st.chat_input("Type your message...")

if prompt:
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Fake Assistant Response (Replace with your model/API call)
    response = f"Echo: {prompt}"  # <- Replace with real model output
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.markdown(response)
