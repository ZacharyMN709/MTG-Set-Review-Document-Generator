from typing import Optional
from functools import cache

import logging
import requests
from time import sleep

from core.game_concepts.card import Card


class Scryfall:
    @classmethod
    @cache
    def request(cls, url: str) -> requests.Response:
        """
        Request data from a url, with an automatic delay that Scryfall requests.
        :param url: The url to request data from.
        :return: The response from the request.
        """
        response = requests.get(url)
        sleep(0.1)  # Scryfall requests this, so I try to be a good netizen.
        return response

    @classmethod
    def scryfall_search(cls, query: str) -> dict[str, Card]:
        """
        Search scryfall for multiple cards, populating the card cache with the results.
        :param query: The query to use, formatted for url.
        :return: A list of names added to the cache.
        """
        cards = dict()
        url = f"https://api.scryfall.com/cards/search?format=json&order=set&q={query}"
        while url:
            all_data = cls.request(url).json()
            url = all_data.get('next_page', None)
            cards |= {card_data['name']: Card(card_data) for card_data in all_data['data']}

        return cards

    @classmethod
    def scryfall_card(cls, query: str) -> Optional[Card]:
        """
        Search scryfall for a specific card, populating the card cache with the results.
        :param query: The url parameter/path for the card.
        :return: The card data, if found.
        """
        url = f"https://api.scryfall.com/cards/{query}"
        data = cls.request(url).json()

        if data["object"] == 'card':
            return Card(data)
        else:
            logging.warning(f"Could not find card for '{url}'")
            return None
