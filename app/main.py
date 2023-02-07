
from .user_recommendation import user_base

from fastapi import FastAPI

app = FastAPI()



app.include_router(user_base.router)

