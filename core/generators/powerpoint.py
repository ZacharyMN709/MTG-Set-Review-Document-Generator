from typing import Optional
import os
from pathlib import Path

from core.caching import CardCache
from core.images import ImageProcessor
from core.documents import pptx
from core.game_concepts.card import Card
from core.game_concepts.ordering import order


class PowerPointGenerator:
    expansion: str
    bonus_sheet: Optional[str]
    card_cache: CardCache
    day_one_cards: list[Card]
    day_two_cards: list[Card]

    @classmethod
    def create_set_review(
            cls,
            expansion: str,
            bonus_sheet: Optional[str],
            card_cache: CardCache,
            print_card_list: bool = False
    ):
        generator = PowerPointGenerator(expansion, bonus_sheet, card_cache)

        if print_card_list:
            print("Cards: ")
            for card in generator.sorted_card_list:
                print(repr(card))
            print(" - - - - - - - - - - \n")

        # TODO: Better handle output path logic.
        generator.generate_powerpoints(os.path.join(f'../../Generated Documents', expansion.upper()))
        return generator

    def __init__(self, expansion: str, bonus_sheet: Optional[str], card_cache: CardCache):
        self.expansion = expansion
        self.bonus_sheet = bonus_sheet
        self.card_cache = card_cache
        # TODO: See if this can be moved into the cache object.
        self.day_one_cards, self.day_two_cards = order(self.card_cache, self.expansion, self.bonus_sheet)

    def generate_powerpoints(self, output_dir: str = '.'):
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)

        day_one_file_name = f"{self.expansion} - Commons and Uncommons.pptx"
        pptx.gen_powerpoint(
            os.path.join(output_dir, day_one_file_name),
            ImageProcessor.image_generator(self.day_one_cards)
        )
        print(f"Created file '{day_one_file_name}'!")

        day_two_file_name = f"{self.expansion} - Rares and Mythics.pptx"
        pptx.gen_powerpoint(
            os.path.join(output_dir, day_two_file_name),
            ImageProcessor.image_generator(self.day_two_cards)
        )
        print(f"Created file '{day_two_file_name}'!")

    # TODO: See if this can be moved into the cache object.
    @property
    def sorted_card_list(self) -> list[Card]:
        return self.day_one_cards + self.day_two_cards


def main(
        expansion: str,
        bonus_sheet: Optional[str],
        *queries: str,
        print_card_list: bool = False
) -> PowerPointGenerator:
    cache = CardCache.from_queries(*queries)
    return PowerPointGenerator.create_set_review(expansion, bonus_sheet, cache, print_card_list)


def otj():
    set_code = 'OTJ'
    bonus_set_code = 'OTP'
    scryfall_queries = [
        'set:otj unique:cards',
        'set:otp unique:cards',
        'set:big unique:cards',
        '(set:spg and date=otj) unique:cards'
    ]

    main(set_code, bonus_set_code, *scryfall_queries, print_card_list=True)


def debug():
    file_name = "Test.pptx"
    cache = CardCache.from_card_keys(
        # TODO: Come up with more comprehensive test suite of cards.
        ("MOM", "Captive Weird"),
        ("MOM", "Invasion of Kaladesh"),
        ("MOM", "Joyful Stormsculptor"),
        ("HOU", "Refuse // Cooperate"),
        ("GRN", "Expansion // Explosion"),
        ("ELD", "Bonecrusher Giant"),
        ("NEO", "Fable of the Mirror Breaker"),
        ("ZNR", "Shatterskull Smashing"),
        ("CHK", "Akki Lavarunner"),
        ("BRO", "Skitterbeam Battalion"),
        ("EMN", "Hanweir Garrison"), # TODO: Handle meld back faces
    )
    cards = cache.card_list()

    for card in cards:
        print(f"{card}: {card.layout}")

    output_dir = f'../../Generated Documents/Debug'
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)

    pptx.gen_powerpoint(
        os.path.join(output_dir, file_name),
        ImageProcessor.image_generator(cards)
    )
    print(f"Created file '{file_name}'!")


if __name__ == "__main__":
    debug()



