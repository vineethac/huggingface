from model import model_pipeline
from fastapi import FastAPI, Request
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/ask")
def ask(data: Item):
    print(data.text)
    result = model_pipeline(data.text)
    print(result)
    return {"answer": result}
    # return {"message": f"You wrote: '{data.text}'"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=5000, log_level="info", timeout_keep_alive=30)