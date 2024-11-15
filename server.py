import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()
keystrokes: List[dict] = []


class Keystroke(BaseModel):
    key: str

@app.post("/log_key")
async def log_key(keystroke: Keystroke):
    keystrokes.append({keystroke.key})
    return {keystroke.key}


@app.get("/view_log")
async def view_log():
    return {"keystrokes": keystrokes}