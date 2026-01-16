from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .websocket import websockets
from ..utils.logger import logger
from .websocket import websockets, isConnected


router = APIRouter(
    prefix="/pc",
    tags=["player_connected"],
    responses={404: {"message":"This request was invalid"}},
)

class PlayerConnected(BaseModel):
    name: str
    steamid: str
    country: str
    
@router.post("/", status_code=201)
async def player_connected(player_connected: PlayerConnected, status_code=201):
    json=player_connected.model_dump()
    for clientws in websockets:
        if clientws == "tf2":
            continue   
        json["event_type"] = "player_connected" 
        try:
            await websockets[clientws]["ws"].send_json(json)
        except RuntimeError:
            logger.info(f"Envio pro cliente websocket {clientws} falhou, tornando a conexão como desconectada...")
            websockets[clientws]["connected"] = False
    
    recipients=isConnected(websockets)
    if "tf2" in recipients:
        recipients.remove("tf2")
    return {
            "player_connected": player_connected.model_dump(),
            "recipients": recipients          
            }