from fastapi import FastAPI
from .routers import users
from .crud.database import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (optional)


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)


@app.get("/")
def hello():
    return {"message": "Flight Booking Api"}
