from pydantic import BaseModel, HttpUrl


class GutenbergModel(BaseModel):
    """
    Model for representing Gutenberg data.

    Attributes:
        URL (HttpUrl): The URL of the Gutenberg text.
        author (str | None): The author of the text (optional).
        title (str | None): The title of the text (optional).
    """

    URL: HttpUrl
    author: str | None
    title: str | None
