import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_TELEGRAM = os.getenv('TOKEN_TELEGRAM')
TOKEN_OPENAI = os.getenv('TOKEN_OPENAI')
ADMIN_ID = os.getenv('ADMIN_ID')