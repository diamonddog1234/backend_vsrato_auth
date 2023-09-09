from typing import Union

from fastapi import FastAPI
from routes.auth_route import auth_router

app = FastAPI()
app.include_router(auth_router)