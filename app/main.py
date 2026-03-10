from fastapi import FastAPI
from .routers import log, users


app = FastAPI()

app.include_router(users.router, prefix="/user")
app.include_router(log.router, prefix="/log")
