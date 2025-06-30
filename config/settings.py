from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

settings = Settings()
