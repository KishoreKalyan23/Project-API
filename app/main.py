# adding cors headers
from fastapi.middleware.cors import CORSMiddleware

from .user_recommendation import user_base, convertion

from fastapi import FastAPI

app = FastAPI()

# bypass the cors error while execution
origins = [
    'http://localhost:8000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



app.include_router(user_base.router)

app.include_router(convertion.router)