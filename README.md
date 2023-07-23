# FastAPI Text Analyser: Extract Person & Location from document

A FastAPI-based web application that fetches text from a given URL and performs **Named Entity Recognition (NER)** to identify people's names and associated places within the text. The application uses the **spaCy** library for NER.

## Tech Stack

- **FastAPI:** FastAPI is a modern, fast, web framework for building APIs with Python.
- **spaCy:** spaCy is a powerful and efficient natural language processing library.
- **BeautifulSoup:** BeautifulSoup is used for web scraping and parsing HTML content.
- **requests:** requests is used to make HTTP requests to fetch the text from a given URL.
- **uvicorn:** uvicorn is a fast ASGI server used to run the FastAPI application.

## Installation

You can use Docker Compose to run the application inside a Docker container. Follow these steps:

1. Clone this repository to your local machine.
2. Make sure you have Docker and Docker Compose installed on your system.
3. Open a terminal or command prompt in the project's root directory.
4. Run the following command to build the Docker image:
   <pre>docker-compose up -d --build</pre>
5. The application will now be accessible at http://localhost:8080.

**NOTE:** en_core_web_lg is large file so it may take a while to download

## Endpoints

**Analyze Text**
**Endpoint:** /analyze

**Method:** POST

**Request Payload:** JSON data with the following format:

<pre>{
  "URL": "https://www.example.com/sample-text",
  "author": "John Doe",
  "title": "Sample Title"
}</pre>

Happy analysing! 📚✨
