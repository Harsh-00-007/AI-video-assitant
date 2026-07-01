import streamlit as st
from dotenv import load_dotenv
import time

# Import your existing pipeline functions
from main import run_pipeline
from core.rag_engine import ask_question

# Load environment variables
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🤖",
    layout="wide"
)

# --- Initialize Session State ---
# We use session state to remember data between button clicks and chat messages
if "processed_data" not in st.session_state:
    st.session_state.processed_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Sidebar: Inputs & Controls ---
with st.sidebar:
    st.header("⚙️ Configuration")
    source_input = st.text_input("YouTube URL or Local File Path:", placeholder="https://youtu.be/...")
    language_input = st.selectbox("Language:", ["english", "hinglish"])
    
    process_button = st.button("🚀 Process Video", use_container_width=True)
    
    if process_button and source_input:
        with st.spinner("Processing video... This may take a few minutes depending on length."):
            try:
                # Run your backend pipeline
                result = run_pipeline(source_input, language_input)
                
                # Store the result in session state so it survives script reruns
                st.session_state.processed_data = result
                
                # Reset chat history for a new video
                st.session_state.chat_history = [
                    {"role": "assistant", "content": f"Hello! I have analyzed '{result['title']}'. What would you like to know?"}
                ]
                st.success("Processing Complete!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- Main Area: Dashboard & Chat ---
st.title("🤖 AI Video & Meeting Assistant")

# Only show the dashboard if we have processed data
if st.session_state.processed_data:
    data = st.session_state.processed_data
    
    st.subheader(f"📌 {data['title']}")
    
    # Phase 1: Structured Data (Using Tabs for a clean UI)
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Summary", "✅ Action Items", "🔑 Key Decisions", "❓ Open Questions"])
    
    with tab1:
        st.write(data['summary'])
    with tab2:
        st.write(data['action_items'])
    with tab3:
        st.write(data['key_decisions'])
    with tab4:
        st.write(data['open_questions'])
        
    st.divider()
    
    # Phase 2: RAG Chat Interface
    st.subheader("💬 Chat with your meeting")
    
    # Display existing chat messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Chat Input Box
    if user_question := st.chat_input("Ask a question about the video..."):
        # 1. Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_question)
            
        # 2. Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        
        # 3. Get AI response using the cached RAG chain
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                rag_chain = data["rag_chain"]
                answer = ask_question(rag_chain, user_question)
                st.markdown(answer)
                
        # 4. Add AI response to history
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

else:
    # Default landing screen
    st.info("👈 Please enter a video URL in the sidebar and click 'Process Video' to begin.")