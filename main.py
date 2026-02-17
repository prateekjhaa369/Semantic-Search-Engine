from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware # <--- 1. Add this import
from scripts.search import FinancialSearchEngine
import uvicorn
import os

app = FastAPI(title="Mini-Google Financial Search")

# 2. Add the CORS Middleware "Permission Slip"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins (fine for local dev)
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

try:
    engine = FinancialSearchEngine()
except Exception as e:
    print(f"❌ Error loading search engine: {e}")
    engine = None

@app.get("/")
def serve_index():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "API is online, but index.html was not found."}

@app.get("/search")
def search_news(q: str, limit: int = 5):
    if not engine:
        raise HTTPException(status_code=500, detail="Search engine not initialized.")
    results = engine.search(q, top_k=limit)
    return {"query": q, "results": results}

if __name__ == "__main__":
    import os
    # Render provides a PORT environment variable. If it's not there, use 8000.
    port = int(os.environ.get("PORT", 8000))
    # Use 0.0.0.0 so it's accessible externally
    uvicorn.run(app, host="0.0.0.0", port=port)