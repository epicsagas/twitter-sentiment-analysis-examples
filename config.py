import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DRIVER_DIR = os.getenv("DRIVER_DIR")
CKEY = os.getenv("CKEY")
CSECRET = os.getenv("CSECRET")
ATOKEN = os.getenv("ATOKEN")
ASECRET = os.getenv("ASECRET")