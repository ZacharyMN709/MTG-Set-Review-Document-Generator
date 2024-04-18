from typing import Optional
import logging
import requests
from time import sleep
from io import BytesIO

from PIL import Image

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
    front_image_url: str
    back_image_url: Optional[str]

    def __init__(self, json: dict):
        self._json = json
        self._populate_card_face_data()
        self._populate_collector_data()
        self._populate_cost_data()
        self._populate_types()
        self._populate_image_data()

    # region Initialization
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

    def _populate_card_face_data(self):
        if 'card_faces' in self._json:
            self._front_face = self._json['card_faces'][0]
            self._back_face = self._json['card_faces'][1]
        else:
            self._front_face = self._json
            self._back_face = None

        self.layout = self._parse_from_json('layout')

        # NOTE: Some custom handling has to be done to identify aftermath card frames.
        if self.layout == 'split':
            keywords = self._parse_from_json('keywords')
            if 'Aftermath' in keywords:
                self.layout = 'aftermath'

    def _populate_collector_data(self):
        self.scryfall_id = self._json['id']
        self.expansion = self._json['set'].upper()
        self.number = self._parse_from_json('collector_number')
        self.rarity = self._parse_from_json('rarity')
        self.full_name = self._parse_from_json('name')
        if self.layout in {'split'}:
            self.name = self.full_name
        else:
            self.name = self._front_face.get('name', self.full_name)

    def _populate_cost_data(self):
        self.mana_cost = self._parse_from_json('mana_cost', '')
        self.cmc = self._parse_from_json('cmc', 0)
        self.colors = parse_color_list(self._parse_from_json('colors', ''))
        self.color_identity = parse_color_list(self._parse_from_json('color_identity', ''))
        self.casting_identity = get_color_identity(self.mana_cost)

    def _populate_types(self):
        self.type_line = self._parse_from_json('type_line', '')
        self.all_types = set(self.type_line.split(' ')) - {'—', '//'}
        self.supertypes = self.all_types & SUPERTYPES
        self.types = self.all_types & TYPES
        self.subtypes = self.all_types & SUBTYPES

    def _populate_image_data(self):
        if self.layout in {'adventure', 'split', 'aftermath', 'flip'}:
            self.front_image_url = self._get_image_url(self._json)
            self.back_image_url = None
        else:
            self.front_image_url = self._get_image_url(self._front_face)
            self.back_image_url = self._get_image_url(self._back_face)
    # endregion Initialization

    @property
    def card_url(self) -> str:
        """Shortened link to the Scryfall page for the card"""
        return f"https://scryfall.com/card/{self.expansion.lower()}/{self.number}"

    @classmethod
    def _get_face_image(cls, url: str) -> Optional[Image.Image]:
        if url:
            sleep(0.1)  # Scryfall requests this, so I try to be a good netizen.
            image_data = requests.get(url).content
            return Image.open(BytesIO(image_data))
        else:
            return None

    @property
    def front_image(self) -> Image.Image:
        image = self._get_face_image(self.front_image_url)
        if "Battle" in self.all_types or self.layout == "split":
            image = image.rotate(270, expand=True)
        return image

    @property
    def back_image(self) -> Optional[Image.Image]:
        return self._get_face_image(self.back_image_url)

    @property
    def full_card_image(self) -> Image.Image:
        if not self.back_image:
            return self.front_image

        merge_image_size = (
            self.front_image.size[0] + self.back_image.size[0],
            max(self.front_image.size[1], self.back_image.size[1])
        )
        merged_image = Image.new("RGBA", merge_image_size, (255, 255, 255, 255))

        front_image_location = (0, (merged_image.size[1] - self.front_image.size[1]) // 2)
        back_image_location = (self.front_image.size[0], (merged_image.size[1] - self.back_image.size[1]) // 2)
        merged_image.paste(self.front_image, front_image_location)
        merged_image.paste(self.back_image, back_image_location)
        return merged_image

    def __str__(self):
        return self.full_name

    def __repr__(self):
        return f"{self.full_name:35} - {self.mana_cost:25} ({self.expansion}:{self.number:3} {self.rarity})"


if __name__ == "__main__":
    from core.data.caching import CardCache

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
        card = card_cache.get_card_data(card_name)
        print_card(card)
        return card


    make_card("Crime")
