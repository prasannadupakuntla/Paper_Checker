import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from backend.api.health import router as health_router
from backend.api.upload import router as upload_router
from backend.api.evaluate import router as evaluate_router

app = FastAPI(
    title="Paper Checker API",
    description="API for evaluating handwritten student answer sheets using OCR and AI.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory to serve static files
UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(health_router, tags=["Health"])
app.include_router(upload_router, tags=["Upload"])
app.include_router(evaluate_router, tags=["Evaluation"])

# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": f"An unexpected error occurred: {str(exc)}"}
    )
