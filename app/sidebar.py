import streamlit as st
from api_utils import upload_document, list_documents, delete_document

def display_sidebar():
    # st.markdown("""
    # <div style="padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    #             border-radius: 15px; margin-bottom: 1.5rem; text-align: center;">
    #     <h2 style="color: white; margin: 0; font-size: 1.5rem;">⚙️ Control Panel</h2>
    # </div>
    # """, unsafe_allow_html=True)
    
    # Model Selection with enhanced styling

    # Quick action buttons
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
    


    st.markdown("### 🤖 Select AI Model")
    model_options = ["gpt-4o", "gpt-4o-mini", "gemini"]
    
    # Create a nice looking model selector
    selected_model = st.selectbox(
        "Choose your AI model:",
        options=model_options,
        key="model",
        help="Select the AI model that will answer your questions"
    )
    
    # Display model info
    model_info = {
        "gpt-4o": "🚀 Most advanced OpenAI model",
        "gpt-4o-mini": "⚡ Fast and efficient OpenAI model", 
        "gemini": "✨ Google's powerful Gemini model"
    }
    
    st.info(f"{model_info.get(selected_model, 'AI Model')}")
    
    st.markdown("---")
    
    # Upload Document Section
    st.markdown("### 📁 Upload Documents")
    
    # File upload with enhanced styling
    uploaded_file = st.file_uploader(
        "📄 Choose a file",
        type=["pdf", "docx", "html"],
        help="Upload PDF, DOCX, or HTML files to enhance the AI's knowledge base"
    )
    
    if uploaded_file is not None:
        # Display file info
        file_details = {
            "📄 Filename": uploaded_file.name,
            "📊 File size": f"{uploaded_file.size / 1024:.1f} KB",
            "🔖 File type": uploaded_file.type
        }
        
        st.markdown("**File Details:**")
        for key, value in file_details.items():
            st.text(f"{key}: {value}")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("📤 Upload", type="primary", use_container_width=True):
                with st.spinner("🔄 Uploading and processing..."):
                    upload_response = upload_document(uploaded_file)
                    if upload_response:
                        st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
                        st.balloons()  # Fun animation
                        st.session_state.documents = list_documents()
        
        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.rerun()
    
    st.markdown("---")
    
    # Document Management Section
    st.markdown("### 📚 Document Library")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Refresh List", use_container_width=True):
            with st.spinner("🔄 Refreshing..."):
                st.session_state.documents = list_documents()
    
    # Initialize document list if not present
    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()
    
    documents = st.session_state.documents
    
    if documents:
        st.markdown(f"**📈 Total Documents: {len(documents)}**")
        
        st.markdown(
            "<div style='max-height: 300px; overflow-y: auto;'>",
            unsafe_allow_html=True,
        )
        # Display documents in a nice format
        for i, doc in enumerate(documents):
            with st.expander(f"📄 {doc['filename']}", expanded=False):
                st.markdown(f"""
                **📋 Details:**
                - **ID:** `{doc['id']}`
                - **📅 Uploaded:** {doc['upload_timestamp']}
                - **📄 Name:** {doc['filename']}
                """)
                
                # Delete button for each document
                if st.button(f"🗑️ Delete", key=f"delete_{doc['id']}", type="secondary"):
                    with st.spinner("🗑️ Deleting..."):
                        delete_response = delete_document(doc['id'])
                        if delete_response:
                            st.success(f"✅ Document deleted successfully!")
                            st.session_state.documents = list_documents()
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to delete document.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Bulk delete option
        with col2:
            if st.button("🗑️ Clear All", use_container_width=True, type="secondary"):
                if st.checkbox("⚠️ I understand this will delete ALL documents"):
                    for doc in documents:
                        delete_document(doc['id'])
                    st.session_state.documents = list_documents()
                    st.success("🧹 All documents cleared!")
                    st.rerun()
    
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: rgba(255,193,7,0.1); 
                    border-radius: 10px; border: 2px dashed #ffc107;">
            <h4 style="color: #856404;">📭 No Documents Found</h4>
            <p style="color: #856404; margin: 0;">Upload your first document to get started!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tips section
    # st.markdown("---")
    # st.markdown("### 💡 Tips")
    
    # tips = [
    #     "📄 Upload PDF files for best text extraction",
    #     "🔍 Ask specific questions for better results", 
    #     "📚 Upload multiple documents for comprehensive answers",
    #     "🎯 Use keywords related to your uploaded content"
    # ]
    
    # for tip in tips:
    #     st.markdown(f"• {tip}")
    
    # Quick stats
    # if documents:
    #     st.markdown("---")
    #     st.markdown("### 📊 Quick Stats")
        
    #     # Calculate some basic stats
    #     total_docs = len(documents)
        
    #     st.metric("📄 Documents", total_docs)
        
    #     if total_docs > 0:
    #         # Show most recent upload
    #         latest_doc = max(documents, key=lambda x: x['upload_timestamp'])
    #         st.metric("🕒 Latest Upload", latest_doc['filename'][:20] + "..." if len(latest_doc['filename']) > 20 else latest_doc['filename'])