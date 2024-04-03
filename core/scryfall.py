from typing import Optional
from functools import cache

import logging
import requests
from time import sleep


class Scryfall:
    @classmethod
    @cache
    def _request(cls, url: str) -> requests.Response:
        """
        Request data from a url, with an automatic delay that Scryfall requests.
        :param url: The url to request data from.
        :return: The response from the request.
        """
        response = requests.get(url)
        sleep(0.1)  # Scryfall requests this, so I try to be a good netizen.
        return response

    @classmethod
    def scryfall_search(cls, query: str) -> dict[str, dict]:
        """
        Search scryfall for multiple cards, populating the card cache with the results.
        :param query: The query to use, formatted for url.
        :return: A list of names added to the cache.
        """
        cards = dict()
        url = f"https://api.scryfall.com/cards/search?format=json&order=set&q={query}"
        while url:
            data = cls._request(url).json()
            url = data.get('next_page', None)
            cards |= {card['name']: card for card in data['data']}

        return cards

    @classmethod
    def scryfall_card(cls, query: str) -> Optional[dict]:
        """
        Search scryfall for a specific card, populating the card cache with the results.
        :param query: The url parameter/path for the card.
        :return: The card data, if found.
        """
        url = f"https://api.scryfall.com/cards/{query}"
        data = cls._request(url).json()

        if data["object"] == 'card':
            return data["object"]
        else:
            logging.warning(f"Could not find card for '{url}'")
            return None

