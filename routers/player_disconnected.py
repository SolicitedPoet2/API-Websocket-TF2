from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .websocket import websockets
from ..utils.logger import logger
from .websocket import websockets, isConnected


router = APIRouter(
    prefix="/pd",
    tags=["player_disconnected"],
    responses={404: {"message":"This request was invalid"}},
)

class PlayerDisconnected(BaseModel):
    name: str
    steamid: str
    reason: str
    
@router.post("/", status_code=201)
async def player_disconnected(player_disconnected: PlayerDisconnected, status_code=201):
    json=player_disconnected.model_dump()
    for clientws in websockets:
        if clientws == "tf2":
            continue   
        json["event_type"] = "player_disconnected" 
        try:
            await websockets[clientws]["ws"].send_json(json)
        except RuntimeError:
            logger.info(f"Envio pro cliente websocket {clientws} falhou, tornando a conexão como desconectada...")
            websockets[clientws]["connected"] = False
    
    recipients=isConnected(websockets)
    if "tf2" in recipients:
        recipients.remove("tf2")
    return {
            "player_disconnected": player_disconnected.model_dump(),
            "recipients": recipients          
            }