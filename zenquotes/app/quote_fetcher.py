import requests
import logging
from urllib.parse import urljoin

base_url = "https://zenquotes.io/api/"

endpoint = "today"

default_quote = {
    "quote": "Keep pushing forward, even when it gets tough.",
    "author": "The MindFuel Team"
}

def fetch_quote():
    """Fetches a quote from ZenQuotes API and returns a dict {quote, author}"""
    try:
        #response = requests.get(base_url + endpoint, timeout=5)
        response = requests.get(urljoin(base_url, endpoint), timeout=5)


        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and 'q' in data[0] and 'a' in data[0]:
                return{
                    "quote": data[0]["q"],
                    "author": data[0]["a"]
                }
        logging.warning("Invalid response from ZenQuotes API.")
        # return default_quote as fallback should in ZenQuotes is down
        return default_quote
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching quote: {e}")
        logging.warning("Falling back to default quote due to API error.")
        return default_quote