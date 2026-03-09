from fastapi import FastAPI
from .routers import users, log_analysis


app = FastAPI()

app.include_router(users.router, prefix="/user")
app.include_router(log_analysis.router, prefix="/log-analysis")
