import streamlit as st
from api_utils import get_api_response
import time
from datetime import datetime

def display_chat_interface():
    # Custom CSS for better styling
    st.markdown("""
    <style>
        /* Remove default streamlit styling */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 100%;
        }
        
        /* Hide streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Minimal session info styling */
        .session-info {
            background: rgba(102, 126, 234, 0.05);
            padding: 0.8rem 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            font-size: 0.9rem;
            color: #6c757d;
            border: 1px solid rgba(102, 126, 234, 0.1);
        }
        
        /* Chat container - remove white background */
        .chat-container {
            max-height: 60vh;
            overflow-y: auto;
            padding: 1rem;
            background: transparent;
            border-radius: 15px;
            margin-bottom: 1rem;
        }
        
        /* Custom scrollbar */
        .chat-container::-webkit-scrollbar {
            width: 8px;
        }
        
        .chat-container::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        .chat-container::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 4px;
        }
        
        .chat-container::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #5a6fd8, #6a4190);
        }
        
        /* Message bubbles */
        .user-message {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 1rem;
            animation: slideInRight 0.3s ease-out;
        }
        
        .assistant-message {
            display: flex;
            justify-content: flex-start;
            margin-bottom: 1rem;
            animation: slideInLeft 0.3s ease-out;
        }
        
        .message-bubble {
            max-width: 75%;
            padding: 1rem 1.5rem;
            border-radius: 20px;
            word-wrap: break-word;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            position: relative;
        }
        
        .user-bubble {
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: white;
            border-bottom-right-radius: 5px;
        }
        
        .assistant-bubble {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            border-bottom-left-radius: 5px;
        }
        
        .error-bubble {
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
            color: white;
            border-bottom-left-radius: 5px;
        }
        
        .message-header {
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
            opacity: 0.9;
        }
        
        .message-content {
            line-height: 1.5;
            font-size: 1rem;
        }
        
        .message-time {
            font-size: 0.75rem;
            opacity: 0.7;
            margin-top: 0.5rem;
            text-align: right;
        }
        
        /* Welcome screen - transparent background */
        .welcome-container {
            text-align: center;
            padding: 3rem 2rem;
            background: rgba(102, 126, 234, 0.05);
            border-radius: 20px;
            border: 2px dashed rgba(102, 126, 234, 0.3);
            margin: 2rem 0;
        }
        
        .welcome-title {
            color: #667eea;
            font-size: 2.5rem;
            margin-bottom: 1rem;
            font-weight: 700;
        }
        
        .welcome-subtitle {
            color: #6c757d;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        
        .suggestions-box {
            background: black;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1.5rem auto;
            max-width: 900px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        
        .suggestions-title {
            color: #495057;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        .suggestions-list {
            text-align: left;
            color: #6c757d;
            list-style: none;
            padding: 0;
        }
        
        .suggestions-list li {
            padding: 0.5rem 0;
            border-bottom: 1px solid #f8f9fa;
        }
        
        .suggestions-list li:last-child {
            border-bottom: none;
        }
        
        .suggestions-list li:before {
            content: "💡";
            margin-right: 0.5rem;
        }
        
        /* Chat input styling - improved */
        .stChatInput {
            position: relative;
        }
        
        .stChatInput > div {
            border-radius: 25px !important;
            border: 2px solid #e9ecef !important;
            background: black !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
            transition: all 0.3s ease !important;
            overflow: hidden !important;
        }
        
        .stChatInput > div:focus-within {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15), 0 4px 20px rgba(0, 0, 0, 0.15) !important;
            transform: translateY(-1px) !important;
        }
        
        .stChatInput input {
            font-size: 1rem !important;
            padding: 1rem 1.5rem !important;
            border: none !important;
            background: transparent !important;
            width: 100% !important;
        }
        
        .stChatInput input::placeholder {
            color: #adb5bd !important;
            font-style: italic !important;
        }
        
        /* Hide any white overlay or button inside input */
        .stChatInput > div > div {
            background: transparent !important;
        }
        
        .stChatInput button {
            background: transparent !important;
            border: none !important;
            padding: 0.5rem !important;
        }
        
        /* Animations */
        @keyframes slideInRight {
            from { 
                transform: translateX(100%); 
                opacity: 0; 
            }
            to { 
                transform: translateX(0); 
                opacity: 1; 
            }
        }
        
        @keyframes slideInLeft {
            from { 
                transform: translateX(-100%); 
                opacity: 0; 
            }
            to { 
                transform: translateX(0); 
                opacity: 1; 
            }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .pulse-animation {
            animation: pulse 2s infinite;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .message-bubble {
                max-width: 90%;
            }
            
            .welcome-container {
                padding: 2rem 1rem;
            }
            
            .welcome-title {
                font-size: 2rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Session info (minimal, only if exists)
    if st.session_state.session_id:
        st.markdown(f'''
        <div style="background: rgba(102, 126, 234, 0.1); padding: 0.8rem 1rem; border-radius: 10px; margin-bottom: 1rem; font-size: 0.9rem; color: #6c757d;">
            <span style="margin-right: 2rem;">🔗 Session: <code>{st.session_state.session_id[:8]}...</code></span>
            <span>💬 Messages: {len(st.session_state.messages)}</span>
        </div>
        ''', unsafe_allow_html=True)
    
    # Chat messages area
    if not st.session_state.messages:
        # Welcome screen
        st.markdown('''
        <div class="welcome-container">
            <div class="welcome-title pulse-animation">👋 Welcome!</div>
            <div class="welcome-subtitle">
                Start a conversation by asking questions about your uploaded documents
                    <div class="suggestions-box">
                <div class="suggestions-title">💡 Try asking:</div>
                <ul class="suggestions-list">
                    <li>"Summarize the main points of the document"</li>
                    <li>"What are the key findings mentioned?"</li>
                    <li>"Explain this concept in simple terms"</li>
                    <li>"What questions does this document answer?"</li>
                    <li>"Compare different sections of the document"</li>
                </ul>
            </div>
            </div>
            
            
        </div>
        ''', unsafe_allow_html=True)
    else:
        # Chat messages container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for i, message in enumerate(st.session_state.messages):
            timestamp = message.get("timestamp", datetime.now().strftime("%H:%M"))
            
            if message["role"] == "user":
                st.markdown(f'''
                <div class="user-message">
                    <div class="message-bubble user-bubble">
                        <div class="message-header">👤 You</div>
                        <div class="message-content">{message["content"]}</div>
                        <div class="message-time">{timestamp}</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                bubble_class = "error-bubble" if message.get("error") else "assistant-bubble"
                icon = "❌" if message.get("error") else "🎓"
                
                st.markdown(f'''
                <div class="assistant-message">
                    <div class="message-bubble {bubble_class}">
                        <div class="message-header">{icon} AskProfessor</div>
                        <div class="message-content">{message["content"]}</div>
                        <div class="message-time">{timestamp}</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Response details for the last successful message
        if (st.session_state.messages and 
            st.session_state.messages[-1]["role"] == "assistant" and 
            not st.session_state.messages[-1].get("error")):
            
            last_message = st.session_state.messages[-1]
            with st.expander("📊 Response Details", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("🤖 Model", last_message.get('model', 'Unknown'))
                
                with col2:
                    st.metric("🔗 Session", f"{last_message.get('session_id', 'Unknown')[:8]}...")
                
                with col3:
                    st.metric("⏱️ Time", last_message.get('timestamp', 'Unknown'))
    
    # Chat input
    if prompt := st.chat_input("💭 Ask me anything about your documents...", key="chat_input"):
        # Add user message
        timestamp = datetime.now().strftime("%H:%M:%S")
        user_message = {
            "role": "user", 
            "content": prompt,
            "timestamp": timestamp
        }
        st.session_state.messages.append(user_message)
        
        # Show loading state
        with st.spinner("🤔 AskProfessor is thinking..."):
            time.sleep(0.5)  # Small delay for better UX
            
            try:
                response = get_api_response(prompt, st.session_state.session_id, st.session_state.model)
                
                response_timestamp = datetime.now().strftime("%H:%M:%S")
                
                if response:
                    # Update session ID
                    st.session_state.session_id = response.get('session_id')
                    
                    # Add successful response
                    assistant_message = {
                        "role": "assistant", 
                        "content": response['answer'],
                        "timestamp": response_timestamp,
                        "model": response.get('model', 'unknown'),
                        "session_id": response.get('session_id', 'unknown')
                    }
                    st.session_state.messages.append(assistant_message)
                    st.success("✅ Response generated successfully!")
                    
                else:
                    # Add error message
                    error_message = {
                        "role": "assistant", 
                        "content": "Sorry, I encountered an error while processing your request. Please try again.",
                        "timestamp": response_timestamp,
                        "error": True
                    }
                    st.session_state.messages.append(error_message)
                    st.error("❌ Failed to get response from API. Please try again.")
                    
            except Exception as e:
                error_timestamp = datetime.now().strftime("%H:%M:%S")
                error_message = {
                    "role": "assistant", 
                    "content": f"An unexpected error occurred: {str(e)}",
                    "timestamp": error_timestamp,
                    "error": True
                }
                st.session_state.messages.append(error_message)
                st.error(f"❌ Unexpected error: {str(e)}")
        
        # Rerun to show new messages
        st.rerun()