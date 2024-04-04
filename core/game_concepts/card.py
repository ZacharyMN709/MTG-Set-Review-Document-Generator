from typing import Optional
import logging

from core.game_concepts.card_types import SUPERTYPES, TYPES, SUBTYPES
from core.game_concepts.colors import parse_color_list, get_color_identity


class Card:
    scryfall_id: str
    expansion: str
    number: int
    rarity: str
    full_name: str
    name: str
    mana_cost: str
    cmc: int
    colors: str
    color_identity: str
    casting_identity: str
    type_line: str
    all_types: set[str]
    supertypes: set[str]
    types: set[str]
    subtypes: set[str]
    front_image: str
    back_image: Optional[str]

    @classmethod
    def _get_image_url(cls, face: Optional[dict]) -> Optional[str]:
        """
        Get the highest resolution image available from a card face
        :param face: The card or card face data.
        :return: A url to the image.
        """
        if face is None:
            return None

        uris = ['large', 'border_crop', 'normal', 'small', 'art_crop']
        for uri in uris:
            if uri in face["image_uris"]:
                return face["image_uris"][uri]

    def __init__(self, json: dict):
        self._json = json
        if 'card_faces' in self._json:
            self._front_face = self._json['card_faces'][0]
            self._back_face = self._json['card_faces'][1]
        else:
            self._front_face = self._json
            self._back_face = None

        self.scryfall_id = json['id']
        self.expansion = json['set'].upper()
        self.number = self._parse_from_json('collector_number')
        self.rarity = self._parse_from_json('rarity')
        self.full_name = self._parse_from_json('name')
        self.name = self._front_face.get('name', self.full_name)

        self.mana_cost = self._parse_from_json('mana_cost', '')
        self.cmc = self._parse_from_json('cmc', 0)
        self.colors = parse_color_list(self._parse_from_json('colors', ''))
        self.color_identity = parse_color_list(self._parse_from_json('color_identity', ''))
        self.casting_identity = get_color_identity(self.mana_cost)

        self.type_line = self._parse_from_json('type_line', '')
        self.all_types = set(self.type_line.split(' ')) - {'—', '//'}
        self.supertypes = self.all_types & SUPERTYPES
        self.types = self.all_types & TYPES
        self.subtypes = self.all_types & SUBTYPES

        self.front_image_url = self._get_image_url(self._front_face)
        self.back_image_url = self._get_image_url(self._back_face)

    @property
    def card_url(self) -> str:
        """Shortened link to the Scryfall page for the card"""
        return f"https://scryfall.com/card/{self.expansion.lower()}/{self.number}"

    def _parse_from_json(self, key, default=None):
        # Attempt to get the value from general card information.
        val = self._json.get(key)
        if val is not None:
            return val

        # Attempt to get the value from the front face.
        faces = self._json.get('card_faces')
        if faces:
            val = faces[0].get(key)
            if val is not None:
                return val

        # Fall-back to the default, logging unexpected absences.
        #  Because of how mana cost and colour are stored, they are likely to be empty,
        #  so we skip logging when they're missing, to avoid cluttering up the log.
        if key not in ['mana_cost', 'colors']:  # pragma: nocover
            logging.debug(f"'{key}' is empty for card '{self.name}'")
        return default


if __name__ == "__main__":
    from core.caching import CardCache

    card_cache = CardCache()

    def print_card(card):
        print()
        print(f"NAME: {card.name}")
        print(f"FULL NAME: {card.full_name}")
        print(f"MANA_COST: {card.mana_cost}")
        print(f"SET: {card.expansion}")
        print(f"CMC: {card.cmc}")
        print(f"COLORS: {card.colors}")
        print(f"COLOR_IDENTITY: {card.color_identity}")
        print(f"SUPERTYPES: {card.supertypes}")
        print(f"TYPES: {card.types}")
        print(f"SUBTYPES: {card.subtypes}")
        print(f"FRONT IMAGE: {card.front_image_url}")
        print(f"BACK IMAGE: {card.back_image_url}")


    def make_card(card_name):
        card_data = card_cache.get_card_data(card_name)
        card = Card(card_data)
        print_card(card)
        return card


    make_card("Joyful Stormsculptor")
    make_card("Captive Weird")
    make_card("Invasion of Kaladesh")

    pass