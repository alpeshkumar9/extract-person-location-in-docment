import logging
import requests
import validators
from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse
from typing import Any
import uvicorn
from bs4 import BeautifulSoup

from model.gutenberg import GutenbergModel
from ner import NER
from settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
ner = NER()


def fetch_text(url) -> str:
    """
    Fetches text content from the provided URL using HTTP GET request.

    Parameters:
        url (str): The URL from which to fetch the text.

    Returns:
        str: The text content retrieved from the URL.

    Raises:
        HTTPException: If the URL is invalid or the request fails.
    """

    if not validators.url(url):
        logger.error(f"Invalid URL: {url}")
        raise HTTPException(status_code=400, detail="Invalid URL provided.")

    logging.info(f"Fetching text from URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        logger.info(f"Text extracted!")
        return text
    else:
        logger.error(f"Failed to fetch text from URL: {url}")
        raise HTTPException(
            status_code=404, detail="Failed to fetch text from URL.")


@app.post("/analyse")
def analyse_text(data: GutenbergModel) -> Any:
    """
    Analyzes the text content from a given URL and performs Named Entity Recognition (NER) to identify person names
    and associated places.

    Parameters:
        data (GutenbergModel): The data containing the URL, author, and title.

    Returns:
        Any: A list
    """

    results = []
    try:
        text = fetch_text(data.URL)
        person_names, person_places = ner.process_text(text)

        # Sort the names by their counts in descending order
        sorted_person_names = sorted(
            person_names.items(), key=lambda x: x[1], reverse=True
        )

        # Get the dynamic metakeys
        metakeys = data.dict().keys()

        # Prepare the output in the desired format
        output = {
            **{metakey: data.dict()[metakey] for metakey in metakeys},
            "people": [
                {
                    "name": name,
                    "count": count,
                    "associated_places": [
                        {"name": place, "count": count}
                        for place, count in sorted(
                            places.items(), key=lambda x: x[1], reverse=True
                        )
                    ],
                }
                for name, count in sorted_person_names
                for places in [person_places[name]]
            ],
        }

        results.append(output)

    except HTTPException as e:
        logger.error(f"Error: {e.status_code} - {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    return results


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
