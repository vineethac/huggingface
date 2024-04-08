"""
FastAPI that interacts with LLM and returns response.
"""

import logging
import coloredlogs
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from model import model_pipeline


coloredlogs.install()

# Setting log level
logging.basicConfig(level="INFO")

app = FastAPI()


class Item(BaseModel):
    """
    Class for input text string.
    """
    text: str


@app.get("/")
def read_root():
    """
    Welcome API.
    """
    return "Welcome to FastAPI for your local LLM!"


@app.get("/healthz")
def health():
    """
    Health API.
    """
    return {"Status": "OK"}


@app.post("/ask")
def ask(data: Item):
    """
    API to query the LLM.
    """
    logging.info(f"User prompt: {data.text}")
    result = model_pipeline(data.text)
    logging.info(f"FastAPI response: {result}")
    return {"response": result}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True,
                host="0.0.0.0",
                port=5000,
                log_level="info",
                timeout_keep_alive=30)
