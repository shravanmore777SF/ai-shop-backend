from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import products, recommendations
from app.database import engine
from app.models import models
import os
from app.api import products, recommendations, assistant
from fastapi.middleware.cors import CORSMiddleware

# Initialize database tables on application startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Smart Shop")

# Include API Routers
# Note: Ensure app/api/auth.py exists before including the auth router
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(recommendations.router, prefix="/api/recs", tags=["recommendations"])

# Configure Static Files for the Frontend
# This assumes your HTML/JS files are in a folder named 'static' inside 'backend'
base_dir = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(base_dir, "static")

if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index():
    """
    Serves the main frontend page.
    """
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Backend is live. Please ensure 'index.html' is in the static folder."}

app.include_router(products.router, prefix="/api/products")
app.include_router(assistant.router, prefix="/api/assistant")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows the frontend to talk to your backend
    allow_methods=["*"],
    allow_headers=["*"],
)