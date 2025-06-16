from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.get("/analyse")
async def analyse_listing(listing_url: str = Query(...)):
    decoded_url = unquote(listing_url)

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(decoded_url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")

        title = soup.find("h1")
        title_text = title.get_text(strip=True) if title else ""

        description = soup.find("p")
        description_text = description.get_text(strip=True) if description else ""

        combined_text = f"Title: {title_text}\nDescription: {description_text}"

        prompt = f"""You are a fraud detection assistant. Analyse the following online classified ad and determine if it shows signs of being a scam. Be direct. Highlight any red flags in the language or structure.

{combined_text}

Reply with a risk level (Low, Medium, High) and explain why.
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert fraud detector for online listings."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        gpt_reply = response.choices[0].message.content

        return JSONResponse(content={
            "listing_url": decoded_url,
            "ai_analysis": gpt_reply
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e), "listing_url": decoded_url})
