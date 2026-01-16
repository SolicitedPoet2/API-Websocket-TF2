from fastapi import APIRouter, Depends, HTTPException, WebSocket
from pydantic import BaseModel
from ..utils.logger import logger
import starlette.websockets

router = APIRouter(
    prefix="/ws",
    tags=["websocket"],
    responses={404: {"message":"This request was invalid"}},
)

websockets={}

@router.websocket("/{client}")
async def websocket_endpoint(client: str, websocket: WebSocket):
    await websocket.accept()
    websockets[client]={"ws": websocket, "connected": True}
    while True:
        try:
            data=await websocket.receive_json()
        except starlette.websockets.WebSocketDisconnect:
            logger.info(f"Cliente {client} desconectou.")
            break
            
def isConnected(websockets):
    connected=[]
    for i in websockets:
        if websockets[i]["connected"]:
            connected.append(i)
            
    return connected