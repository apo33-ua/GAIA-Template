"""
FastAPI main application entry point.
Expense Tracker - Personal Expense Management
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Expense Tracker API",
    description="Personal Expense Management API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5188", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "expense-tracker-backend"}

@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Expense Tracker API",
        "version": "1.0.0",
        "docs": "/docs"
    }
