import uvicorn
import os
import sys

# Ensure backend folder is in python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Starting AI Facial Beauty Analyzer on http://{host}:{port}")
    uvicorn.run("backend.main:app", host=host, port=port, reload=False)
