import importlib
import logging
import os

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI


class BasicSetup:
    def __init__(self):
        self.env = None
        self.api = None
        self.client = None
        self.logger = None
        self.formatter = None
        self.handler = None

    def setapi(self):
        self.env = load_dotenv(find_dotenv())
        self.api = os.environ["api_key"]

    def setclient(self):
        self.client = OpenAI(api_key=self.api, base_url="https://api.deepseek.com")

    def setlogger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.handler = logging.StreamHandler()
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def setup(self):
        self.setapi
        self.setclient
        self.setlogger
        return result


def libcheck(lib: str):
    try:
        importlib.import_module(lib)
    except ImportError:
        print(f"Библиотека '{lib}' не установлена.")
    else:
        print(f"Библиотека '{lib}' установлена.")

libcheck('spacy')