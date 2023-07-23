import os
import dotenv

dotenv.load_dotenv()


class Settings:
    """
    Settings class to handle environment variables and application configurations.

    Attributes:
        port (int): The port number to run the application.
        host (str): The host address to bind the application.

    Usage:
        settings = Settings()
        port = settings.port
        host = settings.host
    """

    port: int = int(os.getenv("PORT"))
    host: str = os.getenv("HOST")


settings = Settings()
