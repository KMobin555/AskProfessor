import streamlit as st
from api_utils import get_api_response
import time
from datetime import datetime

def display_chat_interface():
    # Chat header with gradient background
    st.markdown("""
    <div style="padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; margin-bottom: 1.5rem; text-align: center;">
        <h2 style="color: white; margin: 0; font-size: 1.5rem;">💬 Chat with AskProfessor</h2>
        <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            Ask questions about your uploaded documents
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display session info
    if st.session_state.session_id:
        st.markdown(f"""
        <div style="background: rgba(102, 126, 234, 0.1); padding: 0.5rem 1rem; 
                    border-radius: 10px; margin-bottom: 1rem; font-size: 0.85rem;">
            🔗 <strong>Session ID:</strong> <code>{st.session_state.session_id[:8]}...</code>
            📊 <strong>Messages:</strong> {len(st.session_state.messages)}
        </div>
        """, unsafe_allow_html=True)
    
    # Chat container with custom styling
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages with enhanced styling
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
                    <div style="background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); 
                                color: white; padding: 1rem; border-radius: 20px 20px 5px 20px; 
                                max-width: 80%; box-shadow: 0 4px 15px rgba(0,123,255,0.3);
                                animation: slideInRight 0.3s ease-out;">
                        <div style="font-weight: 500; margin-bottom: 0.5rem;">👤 You</div>
                        <div>{message["content"]}</div>
                        <div style="font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem;">
                            {datetime.now().strftime("%H:%M")}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
                    <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                                color: white; padding: 1rem; border-radius: 20px 20px 20px 5px; 
                                max-width: 80%; box-shadow: 0 4px 15px rgba(40,167,69,0.3);
                                animation: slideInLeft 0.3s ease-out;">
                        <div style="font-weight: 500; margin-bottom: 0.5rem;">🎓 AskProfessor</div>
                        <div>{message["content"]}</div>
                        <div style="font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem;">
                            {datetime.now().strftime("%H:%M")}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Enhanced input area
    st.markdown("""
    <style>
    .chat-input {
        position: sticky;
        bottom: 0;
        background: white;
        padding: 1rem 0;
        border-top: 1px solid #e9ecef;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .stChatInput > div {
        border-radius: 25px !important;
        border: 2px solid #e9ecef !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInput > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Chat input with placeholder
    if prompt := st.chat_input("💭 Ask me anything about your documents..."):
        # Add user message with timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Display user message immediately
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
            <div style="background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); 
                        color: white; padding: 1rem; border-radius: 20px 20px 5px 20px; 
                        max-width: 80%; box-shadow: 0 4px 15px rgba(0,123,255,0.3);">
                <div style="font-weight: 500; margin-bottom: 0.5rem;">👤 You</div>
                <div>{prompt}</div>
                <div style="font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem;">
                    {timestamp}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show typing indicator
        with st.spinner("🤔 AskProfessor is thinking..."):
            # Add a small delay for better UX
            time.sleep(0.5)
            
            response = get_api_response(prompt, st.session_state.session_id, st.session_state.model)
            
            if response:
                # Update session ID
                st.session_state.session_id = response.get('session_id')
                
                # Add assistant response with timestamp
                response_timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response['answer'],
                    "timestamp": response_timestamp,
                    "model": response.get('model', 'unknown'),
                    "session_id": response.get('session_id', 'unknown')
                })
                
                # Display assistant response
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
                    <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                                color: white; padding: 1rem; border-radius: 20px 20px 20px 5px; 
                                max-width: 80%; box-shadow: 0 4px 15px rgba(40,167,69,0.3);">
                        <div style="font-weight: 500; margin-bottom: 0.5rem;">🎓 AskProfessor</div>
                        <div>{response['answer']}</div>
                        <div style="font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem;">
                            {response_timestamp}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced details section
                with st.expander("📊 Response Details", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**🤖 Model Used**")
                        st.code(response.get('model', 'Unknown'))
                    
                    with col2:
                        st.markdown("**🔗 Session ID**")
                        st.code(response.get('session_id', 'Unknown'))
                    
                    with col3:
                        st.markdown("**⏱️ Response Time**")
                        st.code(response_timestamp)
                    
                    st.markdown("**📝 Full Response**")
                    st.text_area("", value=response['answer'], height=100, disabled=True)
                    
                    # Add copy button functionality (note: this requires JavaScript)
                    st.markdown("""
                    <button onclick="navigator.clipboard.writeText(arguments[0])" 
                            style="background: #667eea; color: white; border: none; 
                                   padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;">
                        📋 Copy Response
                    </button>
                    """, unsafe_allow_html=True)
                
                # Success message
                st.success("✅ Response generated successfully!")
                
            else:
                st.error("❌ Failed to get a response from the API. Please try again.")
                
                # Add error message to chat
                error_timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "Sorry, I encountered an error while processing your request. Please try again.",
                    "timestamp": error_timestamp,
                    "error": True
                })
    
    # Quick action buttons
    if st.session_state.messages:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🧹 Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.session_id = None
                st.success("Chat cleared!")
                st.rerun()
        
        with col2:
            if st.button("💾 Export Chat", use_container_width=True):
                chat_export = ""
                for msg in st.session_state.messages:
                    role = "You" if msg["role"] == "user" else "AskProfessor"
                    timestamp = msg.get("timestamp", "Unknown")
                    chat_export += f"[{timestamp}] {role}: {msg['content']}\n\n"
                
                st.download_button(
                    label="📥 Download Chat History",
                    data=chat_export,
                    file_name=f"askprofessor_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col3:
            if st.button("🔄 New Session", use_container_width=True):
                st.session_state.session_id = None
                st.info("New session started!")
    
    # Empty state message
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: rgba(102, 126, 234, 0.05); 
                    border-radius: 15px; border: 2px dashed #667eea;">
            <h3 style="color: #667eea; margin-bottom: 1rem;">👋 Welcome to AskProfessor!</h3>
            <p style="color: #6c757d; font-size: 1.1rem; margin-bottom: 1.5rem;">
                Start by asking a question about your uploaded documents.
            </p>
            <div style="background: white; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                <h4 style="color: #495057; margin-bottom: 0.5rem;">💡 Try asking:</h4>
                <ul style="text-align: left; color: #6c757d; max-width: 400px; margin: 0 auto;">
                    <li>"Summarize the main points of the document"</li>
                    <li>"What are the key findings mentioned?"</li>
                    <li>"Explain this concept in simple terms"</li>
                    <li>"What questions does this document answer?"</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)