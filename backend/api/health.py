from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to the Paper Checker API. Go to /docs for Swagger documentation."}

@router.get("/health")
def read_health():
    return {"status": "healthy"}
