import dotenv
import os


class Settings():
    dotenv.load_dotenv()

    app_port = os.getenv("PORT")
    app_host = os.getenv("HOST")
    db_name = os.getenv("SQLITE_DB")
    DATABASE_URI = f"sqlite+aiosqlite:///{db_name}"

settings = Settings()

