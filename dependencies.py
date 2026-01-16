from typing import Annotated
from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()
    
async def get_query_token(token: str):
    if token != str(os.getenv("API_TOKEN")):
        raise HTTPException(status_code=401, detail="Token invalid")
