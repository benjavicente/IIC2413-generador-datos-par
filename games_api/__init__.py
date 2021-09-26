from dotenv import load_dotenv

from .authentication import load_access_token
from .client import Client

load_dotenv()
load_access_token()
