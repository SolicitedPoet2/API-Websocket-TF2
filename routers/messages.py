from fastapi import APIRouter
from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional
from pydantic import BaseModel
from .websocket import websockets, isConnected
from ..utils.logger import logger
from ..utils.database import SessionDep, insert_into_database

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: str = Field(index=True)
    content: str = Field(index=True)
    steamid: Optional[str] = Field(default=None, index=True)
    team: Optional[str] = Field(default=None, index=True)
    created: Optional[datetime] = Field(index=True)

router = APIRouter(
    prefix="/cm",
    tags=["message"],
    responses={404: {"message":"This request was invalid"}},
)           

@router.post("/{client}", status_code=201)
async def create_message(client: str, message: Message, session: SessionDep):
    json=message.model_dump()
    message.created = datetime.now()
    insert_into_database(session, message)
    del json["id"]
    json["event_type"] = "message"
    
    for clientws in websockets:
        if clientws == client:
            continue
        
        try:
            await websockets[clientws]["ws"].send_json(json)
        except RuntimeError:
            logger.info(f"Envio pro cliente websocket {clientws} falhou, tornando a conexão como desconectada...")
            websockets[clientws]["connected"] = False
    
    del json["event_type"]
    
    recipients=isConnected(websockets)
    return {
            "message": json,
            "recipients": recipients          
            }
        
        
