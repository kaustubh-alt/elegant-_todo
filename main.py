from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TaskCreate(BaseModel):
    title: str

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

# In-memory storage
tasks: List[Task] = []
task_id_counter = 1

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Retrieve all tasks"""
    return tasks

@app.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate):
    """Create a new task"""
    global task_id_counter
    new_task = Task(id=task_id_counter, title=task.title, completed=False)
    tasks.append(new_task)
    task_id_counter += 1
    return new_task

@app.put("/tasks/{task_id}/toggle", response_model=Task)
async def toggle_task(task_id: int):
    """Toggle task completion status"""
    for task in tasks:
        if task.id == task_id:
            task.completed = not task.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a task by ID"""
    global tasks
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
