from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .websocket import websockets
from ..utils.logger import logger
from .websocket import websockets, isConnected


router = APIRouter(
    prefix="/mc",
    tags=["map_change"],
    responses={404: {"message":"This request was invalid"}},
)

class MapChange(BaseModel):
    did_map_end: bool
    map_name: str

@router.post("/", status_code=201)
async def map_change(map_change: MapChange, status_code=201):
    json=map_change.model_dump()
    for clientws in websockets:
        if clientws == "tf2":
            continue    
        json["event_type"] = "mapchange"
        try:
            await websockets[clientws]["ws"].send_json(json)
        except RuntimeError:
            logger.info(f"Envio pro cliente websocket {clientws} falhou, tornando a conexão como desconectada...")
            websockets[clientws]["connected"] = False
    
    recipients=isConnected(websockets)
    if "tf2" in recipients:
        recipients.remove("tf2")
    return {
            "map_change": map_change.model_dump(),
            "recipients": recipients          
            }