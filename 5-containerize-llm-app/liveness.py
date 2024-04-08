"""
This scipt will be used for liveness probe checks.
"""

import sys
from ast import literal_eval
import logging
import coloredlogs
import requests


coloredlogs.install()

# Setting log level
logging.basicConfig(level="INFO")

URL = "http://localhost:5000/ask"
headers = {"Content-Type": "application/json"}
data = {"text": "select head or tail randomly. strictly respond only in one word. \
        no explanations needed."
    }

try:
    response = requests.post(URL, json=data, headers=headers, timeout=300)
except requests.exceptions.ReadTimeout:
    logging.error("ReadTimeout error: LLM did not respond within the specified timeout!")
    # exit unsuccessfully
    sys.exit(1)

response_dict = literal_eval(response.content.decode('utf-8'))

logging.info("Liveness full response: %s", response_dict)
logging.info("Liveness response: %s", response_dict["response"])

if "Head" in response_dict["response"] or "Tail" in response_dict["response"]:
    logging.info("LLM is responding to the prompt.")
else:
    logging.error("LLM is not responding to the prompt!")
    # exit unsuccessfully
    sys.exit(1)
