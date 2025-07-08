# status_api.py

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from task_status_tracker import task_tracker

app = FastAPI(title="AI Legal Assistant Status API")

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AI Legal Assistant Status API"}

@app.get("/status")
async def get_status():
    """Get current task status"""
    return task_tracker.get_status_summary()

@app.get("/progress")
async def get_progress():
    """Get current progress percentage"""
    return {
        "progress": task_tracker.get_progress_percentage(),
        "status_text": task_tracker.get_status_text()
    }

@app.get("/tasks")
async def get_tasks():
    """Get all tasks with their current status"""
    summary = task_tracker.get_status_summary()
    return {"tasks": summary["tasks"]}

@app.post("/reset")
async def reset_status():
    """Reset all task statuses"""
    task_tracker.reset()
    return {"message": "Status reset successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)