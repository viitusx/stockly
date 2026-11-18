from dotenv import load_dotenv

load_dotenv()
import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-temporaria-desenvolvimento")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///stockflow.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False