#!/usr/bin/env python
"""Simple script to start the backend server"""
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Detection Engineering Dashboard Backend")
    print("=" * 60)
    print("Backend will be available at: http://localhost:8000")
    print("API docs will be at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
