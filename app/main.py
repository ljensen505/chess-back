from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from __version__ import __version__
from app.models.routes import AvailableRoutes
from app.routers.games import router as games_router
from app.routers.users import router as users_router

load_dotenv(override=True)

app = FastAPI()
app.include_router(games_router)
app.include_router(users_router)

origins = [
    "http://localhost:3000",
    "http://localhost:",
    "https://api.chess.v2.lucasjensen.me/",
    "https://chess.lucasjensen.me/",
    "https://chess.lucasjensen.me",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=status.HTTP_200_OK)
async def read_root() -> AvailableRoutes:
    return AvailableRoutes(
        available_routes=[
            "/",
            "/games",
            "/games/{game_id}",
            "/users",
            "/users/{user_id}",
        ],
        version=__version__,
    )
