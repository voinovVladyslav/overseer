from fastapi import FastAPI

from overseer.config import base as config


app = FastAPI()


@app.get("/")
def home():
    return {
        "Hello": "World",
        "SECRET_KEY": config.SECRET_KEY,
    }
