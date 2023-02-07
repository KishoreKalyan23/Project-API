
from .user_recommendation import user_base, convertion

from fastapi import FastAPI

app = FastAPI()



app.include_router(user_base.router)

app.include_router(convertion.router)