# app.py

import streamlit as st
import time
import threading
from dotenv import load_dotenv
from crew import legal_assistant_crew
from crew_with_status import create_crew_with_status
from task_status_tracker import task_tracker

load_dotenv()

st.set_page_config(page_title="🧠 AI Legal Assistant", layout="wide")

st.title("⚖️ Personal AI Legal Assistant")
st.markdown(
    "Enter a legal problem in plain English. This assistant will help you:\n"
    "- Understand the legal issue\n"
    "- Find applicable IPC sections\n"
    "- Retrieve matching precedent cases\n"
    "- Generate a formal legal document"
)

with st.form("legal_form"):
    user_input = st.text_area("📝 Describe your legal issue:", height=250)
    submitted = st.form_submit_button("🔍 Run Legal Assistant")

if submitted:
    if not user_input.strip():
        st.warning("Please enter a legal issue to analyze.")
    else:
        # Create crew with status tracking
        crew_with_status = create_crew_with_status(legal_assistant_crew)
        
        # Create placeholders for status updates
        status_container = st.container()
        progress_bar = st.progress(0)
        status_text = st.empty()
        task_status_container = st.empty()
        
        # Function to update status in Streamlit
        def update_streamlit_status():
            while True:
                summary = task_tracker.get_status_summary()
                progress = task_tracker.get_progress_percentage()
                status = task_tracker.get_status_text()
                
                # Update progress bar
                progress_bar.progress(progress / 100)
                
                # Update status text
                status_text.text(status)
                
                # Update individual task statuses
                with task_status_container.container():
                    for task in summary["tasks"]:
                        status_icon = {
                            "pending": "⏳",
                            "in_progress": "🔄",
                            "completed": "✅",
                            "failed": "❌"
                        }.get(task["status"], "❓")
                        st.text(f"{status_icon} {task['description']}")
                
                # Check if completed
                if progress >= 100 or "failed" in status:
                    break
                    
                time.sleep(0.5)
        
        # Start status updates in background
        status_thread = threading.Thread(target=update_streamlit_status)
        status_thread.daemon = True
        status_thread.start()
        
        # Execute the crew with status tracking
        try:
            result = crew_with_status.kickoff(inputs={"user_input": user_input})
            
            # Wait for status updates to complete
            time.sleep(1)
            
            st.success("✅ Legal Assistant completed the workflow!")
            
            # Display final result
            st.subheader("📄 Final Output")
            st.markdown(result if isinstance(result, str) else str(result))
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.error("Please check your API keys and try again.")

        # Optional: Expand sections if intermediate steps are structured (later enhancement)
