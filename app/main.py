from fastapi import FastAPI
from app.api.v1.api import api_router

app = FastAPI(
    title="FastAPI Studies",
    description="FastAPI Studies",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def read_root():
    """
    Endpoint raiz para verificar se a API está online.
    """
    return {"message": "API Online"}