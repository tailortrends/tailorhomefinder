from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from .api import properties

load_dotenv()

app = FastAPI(title="Tailor Home Finder API", version="1.0.0")

CORS_ORIGINS = eval(os.getenv("CORS_ORIGINS", '["http://localhost:5173"]'))
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(properties.router)

@app.get("/")
async def root():
    return {"message": "Tailor Home Finder API", "version": "1.0.0", "docs": "/docs"}
