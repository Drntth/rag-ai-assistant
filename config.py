import os

from dotenv import load_dotenv

load_dotenv()

DATA_DIR = "data"

INPUT_FILENAME = "1_SZMR EKKE- 20250101.docx"

API_KEY = os.getenv("API_KEY")

API_PROVIDER = "openai"
