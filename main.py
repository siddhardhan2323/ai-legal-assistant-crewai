# main.py

import time
import threading
from dotenv import load_dotenv
from crew import legal_assistant_crew
from crew_with_status import create_crew_with_status
from task_status_tracker import task_tracker

load_dotenv()

def print_status_updates():
    """Print status updates in real-time"""
    previous_status = ""
    while True:
        current_status = task_tracker.get_status_text()
        progress = task_tracker.get_progress_percentage()
        
        if current_status != previous_status:
            print(f"\n📊 Status: {current_status}")
            print(f"📈 Progress: {progress:.1f}%")
            
            # Show individual task statuses
            summary = task_tracker.get_status_summary()
            for task in summary["tasks"]:
                status_icon = {
                    "pending": "⏳",
                    "in_progress": "🔄",
                    "completed": "✅",
                    "failed": "❌"
                }.get(task["status"], "❓")
                print(f"   {status_icon} {task['description']}")
            
            previous_status = current_status
        
        # Check if all tasks are completed or failed
        if progress >= 100 or "failed" in current_status:
            break
            
        time.sleep(0.5)

def run(user_input: str):
    # Create crew with status tracking
    crew_with_status = create_crew_with_status(legal_assistant_crew)
    
    # Start status monitoring in background
    status_thread = threading.Thread(target=print_status_updates)
    status_thread.daemon = True
    status_thread.start()
    
    print("🚀 Starting AI Legal Assistant...")
    print("=" * 60)
    
    # Execute the crew with status tracking
    result = crew_with_status.kickoff(inputs={"user_input": user_input})
    
    # Wait for status thread to complete
    time.sleep(1)
    
    print("\n" + "=" * 60)
    print("📄 FINAL RESULT:")
    print("-" * 50)
    print(result)
    print("-" * 50)

if __name__ == "__main__":
    user_input = (
        "A man broke into my house at night while my family was sleeping. "
        "He stole jewelry and cash from our bedroom. When I confronted him, "
        "he threatened me with a knife and ran away. We reported it to the police, "
        "but I'm not sure which legal charges should be filed under IPC."
    )

    run(user_input)
