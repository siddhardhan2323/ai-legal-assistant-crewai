# crew_with_status.py

import time
from typing import Dict, Any
from task_status_tracker import task_tracker


class CrewWithStatus:
    """Wrapper around legal_assistant_crew that tracks task status"""
    
    def __init__(self, crew):
        self.crew = crew
        self.task_mapping = {
            0: "case_intake",
            1: "ipc_section", 
            2: "legal_precedent",
            3: "legal_drafter"
        }
    
    def kickoff(self, inputs: Dict[str, Any]) -> Any:
        """Execute the crew with status tracking"""
        task_tracker.reset()
        
        try:
            # Start the workflow
            print("🚀 Starting AI Legal Assistant workflow...")
            
            # Since we can't hook into CrewAI's internal execution,
            # we'll simulate the task progression with the actual crew execution
            result = self._execute_with_status_tracking(inputs)
            
            return result
            
        except Exception as e:
            # Mark current task as failed if there's an error
            if task_tracker.current_task:
                task_tracker.fail_task(task_tracker.current_task, str(e))
            print(f"❌ Error in workflow: {e}")
            raise
    
    def _execute_with_status_tracking(self, inputs: Dict[str, Any]) -> Any:
        """Execute the crew while tracking status"""
        # Since we can't directly hook into CrewAI's task execution,
        # we'll track the tasks manually by simulating their progression
        
        # This is a simplified approach - in a real implementation,
        # you'd want to hook into CrewAI's execution callbacks
        
        tasks = ["case_intake", "ipc_section", "legal_precedent", "legal_drafter"]
        
        # Start first task
        task_tracker.start_task(tasks[0])
        
        # For demonstration, we'll update status in a separate thread
        # In a real implementation, this would be integrated with CrewAI's callbacks
        import threading
        
        def update_status():
            """Update task status as they would progress"""
            time.sleep(1)  # Simulate case intake time
            task_tracker.complete_task("case_intake")
            
            task_tracker.start_task("ipc_section")
            time.sleep(1)  # Simulate IPC section search time
            task_tracker.complete_task("ipc_section")
            
            task_tracker.start_task("legal_precedent")
            time.sleep(1)  # Simulate legal precedent search time
            task_tracker.complete_task("legal_precedent")
            
            task_tracker.start_task("legal_drafter")
            # The legal drafter task will be completed after crew execution
        
        # Start status updates in background
        status_thread = threading.Thread(target=update_status)
        status_thread.daemon = True
        status_thread.start()
        
        # Execute the actual crew
        result = self.crew.kickoff(inputs=inputs)
        
        # Complete the final task
        task_tracker.complete_task("legal_drafter")
        
        return result


def create_crew_with_status(crew):
    """Create a crew wrapper with status tracking"""
    return CrewWithStatus(crew)