import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException

def scrape_website(url):
    try:
        response = httpx.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return str(soup)  # Ensure the output is always a string
    except httpx.HTTPStatusError as e:
        # Convert this to an HTTPException that FastAPI can handle properly
        raise HTTPException(status_code=400, detail=f"HTTP error occurred: {e}")
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
