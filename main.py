from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.orm import Session
import uvicorn
import json
from urllib.parse import urlparse, parse_qs

from database import get_db
from models import Task, StudyBlock
from google_classroom import (
    get_google_credentials,
    get_classroom_service,
    get_courses,
    get_course_work,
    format_assignment
)
from google_calendar import (
    get_google_credentials,
    get_calendar_service,
    get_events,
    format_event
)

app = FastAPI(title="SmartStudents API")

# Configure CORS - Allow requests from any origin during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data for testing
mock_tasks = [
    {
        "id": 1,
        "title": "Math Assignment",
        "description": "Complete chapters 1-3",
        "due_date": datetime.now().isoformat(),
        "priority": "high",
        "status": "pending"
    },
    {
        "id": 2,
        "title": "Read Chapter 3",
        "description": "Biology textbook",
        "due_date": datetime.now().isoformat(),
        "priority": "medium",
        "status": "pending"
    }
]

mock_study_blocks = [
    {
        "id": 1,
        "task_id": 1,
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now().replace(hour=datetime.now().hour + 2)).isoformat(),
        "productivity_score": 8,
        "notes": "Focused study session"
    },
    {
        "id": 2,
        "task_id": 2,
        "start_time": (datetime.now().replace(hour=datetime.now().hour + 3)).isoformat(),
        "end_time": (datetime.now().replace(hour=datetime.now().hour + 4)).isoformat(),
        "productivity_score": 7,
        "notes": "Review session"
    }
]

@app.get("/")
async def root():
    return {"message": "Welcome to SmartStudents API"}

@app.get("/tasks", response_model=List[dict])
async def get_tasks(
    date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    if date:
        # Filter tasks by date (mock implementation)
        return [task for task in mock_tasks if datetime.fromisoformat(task["due_date"]).date() == date]
    return mock_tasks

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = next((task for task in mock_tasks if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/study-blocks", response_model=List[dict])
async def get_study_blocks(
    date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    if date:
        # Filter study blocks by date (mock implementation)
        return [
            block for block in mock_study_blocks
            if datetime.fromisoformat(block["start_time"]).date() == date
        ]
    return mock_study_blocks

@app.get("/study-blocks/{block_id}")
async def get_study_block(block_id: int):
    block = next((block for block in mock_study_blocks if block["id"] == block_id), None)
    if block is None:
        raise HTTPException(status_code=404, detail="Study block not found")
    return block

# Google Classroom Integration
@app.get("/auth/google")
async def google_auth():
    try:
        creds, auth_url = get_google_credentials()
        if auth_url:
            return {"url": auth_url}
        return {"message": "Already authenticated"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Authentication failed: {str(e)}"}
        )

@app.get("/auth/google/callback")
async def google_auth_callback(request: Request):
    try:
        # Parse the authorization code from the callback URL
        parsed_url = urlparse(str(request.url))
        query_params = parse_qs(parsed_url.query)
        code = query_params.get('code', [None])[0]
        
        if not code:
            return JSONResponse(
                status_code=400,
                content={"error": "Authorization code not found"}
            )
        
        # Exchange the authorization code for credentials
        flow = Flow.from_client_secrets_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri='http://localhost:8080/auth/google/callback'
        )
        flow.fetch_token(code=code)
        creds = flow.credentials
        
        # Save the credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        
        return RedirectResponse(url="http://localhost:3000/calendar")
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Authentication failed: {str(e)}"}
        )

@app.get("/google-classroom/assignments")
async def get_google_classroom_assignments():
    creds, auth_url = get_google_credentials()
    if auth_url:
        raise HTTPException(status_code=401, detail="Not authenticated with Google")
    
    service = get_classroom_service(creds)
    courses = get_courses(service)
    
    assignments = []
    for course in courses:
        course_work = get_course_work(course['id'], service)
        for work in course_work:
            assignment = format_assignment(work, course['name'])
            assignments.append(assignment)
    
    return assignments

# Google Calendar Integration
@app.get("/google-calendar/events")
async def get_google_calendar_events():
    try:
        creds, auth_url = get_google_credentials()
        if auth_url:
            return JSONResponse(
                status_code=401,
                content={"error": "Not authenticated with Google"}
            )
        
        service = get_calendar_service(creds)
        events = get_events(service)
        
        formatted_events = [format_event(event) for event in events]
        return formatted_events
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to fetch events: {str(e)}"}
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    print("Starting server on http://localhost:8080")
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True) 