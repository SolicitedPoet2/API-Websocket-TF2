from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from .dependencies import get_query_token
from .routers import messages
from .routers import map_change
from .routers import player_connected
from .routers import player_disconnected
from .routers import vote_end
from .routers import websocket
from .utils import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_db_and_tables()
    yield
     
app = FastAPI(dependencies=[Depends(get_query_token)], lifespan=lifespan)
app.include_router(messages.router)
app.include_router(map_change.router)
app.include_router(player_connected.router)
app.include_router(player_disconnected.router)
app.include_router(vote_end.router)
app.include_router(websocket.router)

@app.get("/")
async def root():
    return {"message": "Ayo!"}