from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.endpoints import score
from .services.scoring_service import scoring_service

# Initialize the FastAPI app
app = FastAPI(
    title="AI Lead Scoring API",
    description="API for predicting lead intent using an ML model and a rule-based re-ranker.",
    version="1.0.0"
)

# --- Middleware ---
# Configure CORS (Cross-Origin Resource Sharing) to allow requests from your frontend
# IMPORTANT: For production, restrict the origins to your actual frontend domain.
origins = [
    "http://localhost",
    "http://localhost:5173", # Default for Vite dev server
    "http://127.0.0.1:5500", # Default for VS Code Live Server
    "https://687d3bc32ff23ff169565803--lead-generation-project.netlify.app", # Generated URL from Netlify
    # Add your deployed Netlify frontend URL here later
    # e.g., "https://your-app-name.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For simplicity, allow all. Restrict in production.
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# --- API Routers ---
# Include the scoring endpoint
app.include_router(score.router, prefix="/api/v1", tags=["Scoring"])

# --- Application Events ---
@app.on_event("startup")
def startup_event():
    """
    Actions to perform on application startup.
    This is a good place to load models, establish DB connections, etc.
    """
    print("Application startup: Loading ML model...")
    try:
        scoring_service.get_model()
    except Exception as e:
        print(f"FATAL: Could not load ML model on startup. Error: {e}")
        # In a real app, you might want to exit if the model can't be loaded.

@app.get("/", tags=["Root"])
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "Welcome to the AI Lead Scoring API!"}