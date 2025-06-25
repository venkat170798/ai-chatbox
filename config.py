import os
from dotenv import load_dotenv
load_dotenv()

MODE = os.getenv("MODE", "local").lower()