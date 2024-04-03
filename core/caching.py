from typing import Optional
from functools import cache

import logging

from core.scryfall import Scryfall


class CardCache:
    @classmethod
    def from_expansions(cls, expansions: list[str]):
        card_cache = cls()
        for expansion in expansions:
            card_cache.populate_cache_by_expansion(expansion)
        return card_cache

    @classmethod
    def from_queries(cls, queries: list[str]):
        card_cache = cls()
        for query in queries:
            card_cache.populate_cache_by_query(query)
        return card_cache

    @classmethod
    def from_config(cls):
        card_cache = cls()

        # TODO: Load these from a config file
        expansions = list()
        queries = list()

        for expansion in expansions:
            card_cache.populate_cache_by_expansion(expansion)

        for query in queries:
            card_cache.populate_cache_by_query(query)
        return card_cache

    def __init__(self):
        self._card_cache = dict()

    def _add_to_cache(self, card, overwrite: bool = False) -> bool:
        """
        Adds new card data to the cache, skipping existing records.
        Can be set to overwrite data with the `overwrite` flag.
        :param card: The card data to add to the cache.
        :param overwrite: Whether to overwrite existing data.
        :return: Whether the value was updated.
        """
        name = card['name']
        if name in self._card_cache and not overwrite:
            return False

        logging.debug(f"Adding '{name}' to `CARD_CACHE`")
        self._card_cache[name] = card

        if "card_faces" in card:
            short_name = card['card_faces'][0]['name']
            logging.debug(f"Adding '{short_name}' to `CARD_CACHE`")
            self._card_cache[short_name] = card
        return True

    def populate_cache_by_query(self, query) -> None:
        """
        Populates the card cache with results from searching scryfall using a query.
        :param query: The query to use, following Scryfall's search syntax.
        """
        query = query.replace(' ', '+').replace('=', '%3D').replace(':', '%3A')
        cards = Scryfall.scryfall_search(query)
        for _, card in cards:
            self._add_to_cache(card)

    def populate_cache_by_expansion(self, expansion) -> None:
        """
        Popluates the card cache with results for a specific set.
        :param expansion: The set to get cards from.
        """
        cards = Scryfall.scryfall_search(f"e%3A{expansion}")
        for _, card in cards:
            self._add_to_cache(card)

    @cache
    def get_card_data(self, card_name) -> Optional[dict]:
        """
        Gets data for a card, by name. Uses Scryfall's fuzzy match, if a card can't be found in the cache.
        :param card_name: The name of the card.
        :return: The card data, if found.
        """
        if card_name in self._card_cache:
            return self._card_cache[card_name]

        card = Scryfall.scryfall_card(f"named?fuzzy={card_name}")
        self._add_to_cache(card)
        return card

    def get_card_data_by_set(self, card_name, expansion, number) -> Optional[dict]:
        """
        Gets data for a card, using its name, set and collector number.
        This allows for specifying a printing of a card.
        :param card_name: The card name.
        :param expansion: The set the card comes from.
        :param number: The card's collector number in the set.
        :return: The card data, if found.
        """
        card = self._card_cache.get(card_name, None)
        if card and card['set'].lower() == expansion.lower():
            return card

        card = Scryfall.scryfall_card(f"{expansion.lower()}/{number}")
        self._add_to_cache(card)
        return card
