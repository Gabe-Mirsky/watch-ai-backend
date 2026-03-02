from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

API_KEY = "AIzaSyBRJ_Yyx8kPJoJl5ExfzWhH3Jr8tec24Fw"

class Prompt(BaseModel):
    prompt: str


@app.post("/ask")
def ask(p: Prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json={
            "contents": [
                {
                    "parts": [
                        {"text": p.prompt}
                    ]
                }
            ]
        }
    )

    data = response.json()

    if response.status_code != 200:
        return {"error": data}

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"text": text}
    except Exception:
        return {"error": data}