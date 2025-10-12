from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.routes import api_router as api_

app = FastAPI(
    title = "cafeteria_api",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*",
)
app.include_router(api_, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "api running"}



