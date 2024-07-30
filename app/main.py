from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import List

# Initialize FastAPI application
app = FastAPI()

# Define a Pydantic model to structure the consent information
class ConsentInfo(BaseModel):
    purpose: str
    data_collected: List[str]
    data_retention: str
    data_sharing: str
    user_rights: List[str]

# Create an API key header for security
api_key_header = APIKeyHeader(name="X-API-Key")

# Environment variable for the API key
import os
API_KEY = os.getenv("API_KEY", "defaultapikey")

# Function to get the API key and validate it
def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key_header

# Endpoint to serve the consent information, secured by API key
@app.get("/consent", response_model=ConsentInfo)
async def get_consent(api_key: str = Depends(get_api_key)):
    # Sample consent data
    consent_data = {
        "purpose": "To provide personalized exercise recommendations",
        "data_collected": ["heart rate", "exercise duration", "exercise type"],
        "data_retention": "Data will be retained for one year from the date of collection.",
        "data_sharing": "Data will not be shared with third parties.",
        "user_rights": ["Access", "Correction", "Deletion", "Portability"]
    }
    return consent_data

# A simple root endpoint to verify the API is running
@app.get("/")
async def root():
    return {"message": "Hello, World!"}
