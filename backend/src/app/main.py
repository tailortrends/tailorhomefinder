from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from dotenv import load_dotenv
from .api import properties
from .api import inquiries

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

load_dotenv()

app = FastAPI(
    title="Tailor Home Finder API",
    version="1.0.0",
    description="API for TailorHomeFinder luxury real estate platform"
)

CORS_ORIGINS = eval(os.getenv("CORS_ORIGINS", '["http://localhost:5173", "http://localhost:5174"]'))
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(properties.router)
app.include_router(inquiries.router)


@app.get("/")
async def root():
    return {
        "message": "Tailor Home Finder API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "properties": "/api/properties",
            "inquiries": "/api/inquiries"
        }
    }
