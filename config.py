import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_NAME = os.getenv("ADMIN_NAME")

    ADMIN_ROLE = os.getenv("ADMIN_ROLE")


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")