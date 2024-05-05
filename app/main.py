from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
from scraping.scraper import scrape_website
# from nlp.processor import extract_information, vectorize_text
from nlp.processor import ask_gpt_chat #ask_gpt3_5, generate_completion
import logging
import httpx
#from pinecone_config import index
import uuid

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: HttpUrl  # Validates and parses the URL

@app.post("/scrape/")
async def scrape_and_process(request: ScrapeRequest):
    url = str(request.url)  # Convert URL to string here
    logging.info(f"Received URL: {url}")

    try:
        # Scrape the website
        html_content = scrape_website(url)
        logging.info("Website content scraped successfully.")

        # Extract information
        extracted_info1 = ask_gpt_chat(html_content)
        logging.info("Information extracted successfully.")

        # Extract information
        # extracted_info = extract_information(html_content)
        # logging.info("Information extracted successfully.")
        #
        # # Vectorize text
        # vector = vectorize_text(html_content)
        # logging.info("Text vectorized successfully.")

        return {
            "vector": extracted_info1,
            # "vector": vector
        }
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=f"HTTP error occurred: {str(e)}")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.get("/")
async def root():
    return {"message": "Hello World!"}

