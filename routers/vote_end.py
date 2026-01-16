from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .websocket import websockets
from ..utils.logger import logger
from .websocket import websockets, isConnected


router = APIRouter(
    prefix="/ve",
    tags=["vote_end"],
    responses={404: {"message":"This request was invalid"}},
)

class VoteEnd(BaseModel):
    next_map: str

@router.post("/", status_code=201)
async def vote_end(vote_end: VoteEnd, status_code=201):
    json=vote_end.model_dump()
    for clientws in websockets:
        if clientws == "tf2":
            continue    
        json["event_type"] = "vote_end"
        try:
            await websockets[clientws]["ws"].send_json(json)
        except RuntimeError:
            logger.info(f"Envio pro cliente websocket {clientws} falhou, tornando a conexão como desconectada...")
            websockets[clientws]["connected"] = False
    
    recipients=isConnected(websockets)
    if "tf2" in recipients:
        recipients.remove("tf2")
    return {
            "vote_end": vote_end.model_dump(),
            "recipients": recipients          
            }