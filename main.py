from fastapi import FastAPI
from fastapi.responses import JSONResponse
from urllib.parse import unquote

app = FastAPI()

@app.get("/analyse")
async def analyse_listing(listing_url: str):
    decoded_url = unquote(listing_url)

    response = {
        "listing_url": decoded_url,
        "risk_score": 8,
        "risk_level": "High",
        "warnings": [
            "Image also appears in another listing in Morocco",
            "Suspicious wording: 'Urgent sale, contact via WhatsApp'",
            "Price unusually low compared to similar listings"
        ]
    }
    return JSONResponse(content=response)
