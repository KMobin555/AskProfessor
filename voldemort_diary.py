import streamlit as st

# -------------------
# Page Configuration
# -------------------
st.set_page_config(page_title="Tom Riddle's Diary", layout="centered")

# -------------------
# Custom CSS for Styling
# -------------------
diary_style = """
<style>
body {
    background-color: #1c1b18;
    color: #d6c9b4;
    font-family: 'Courier New', monospace;
}

[data-testid="stAppViewContainer"] {
    background-image: url("https://i.imgur.com/sZ7NdHL.jpg");
    background-size: cover;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);
}

h1 {
    text-align: center;
    font-family: "Cinzel Decorative", cursive;
    color: #e7e0c9;
    text-shadow: 0px 0px 10px #7f5e3d;
}

.chat-row {
    background-color: rgba(28, 27, 24, 0.7);
    padding: 10px;
    margin: 10px 0;
    border-radius: 10px;
    box-shadow: 0 0 15px #3e2d1c;
    font-size: 18px;
}
</style>
"""

st.markdown(diary_style, unsafe_allow_html=True)

# -------------------
# App Title
# -------------------
st.title("🕮 Tom Riddle's Diary")

# -------------------
# Initialize Chat
# -------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------
# Display Chat History
# -------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f"<div class='chat-row'>{msg['content']}</div>", unsafe_allow_html=True)

# -------------------
# Prompt Input
# -------------------
prompt = st.chat_input("Write in the diary...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-row'>{prompt}</div>", unsafe_allow_html=True)

    # Fake magic response (replace with Gemini or GPT response here)
    response = f"*The ink fades... and appears again:*\n\n**{prompt[::-1]}**"
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(f"<div class='chat-row'>{response}</div>", unsafe_allow_html=True)
