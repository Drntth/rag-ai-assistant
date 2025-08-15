import os

from dotenv import load_dotenv

load_dotenv()

DATA_DIR = "data"

INPUT_FILENAME = "input.docx"

API_KEY = os.getenv("API_KEY")

API_PROVIDER = "openai"
