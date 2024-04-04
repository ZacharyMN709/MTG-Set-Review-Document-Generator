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

    def __init__(self, expansion: str, bonus_sheet: Optional[str], card_cache: CardCache):
        self.expansion = expansion
        self.bonus_sheet = bonus_sheet
        self.card_cache = card_cache
        self.day_one_cards, self.day_two_cards = order(self.card_cache, self.expansion, self.bonus_sheet)

    def generate_powerpoint(self, output_dir: str = '.'):
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        path.joinpath()

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

    def sorted_card_list(self) -> list[Card]:
        return self.day_two_cards + self.day_two_cards


def main(
        expansion: str,
        bonus_sheet: Optional[str],
        *queries: str,
        print_card_list: bool = False
) -> PowerPointGenerator:
    cache = CardCache.from_queries(*queries)
    generator = PowerPointGenerator(expansion, bonus_sheet, cache)

    if print_card_list:
        print("Cards: ")
        for card in generator.sorted_card_list():
            print(repr(card))
        print(" - - - - - - - - - - \n")

    generator.generate_powerpoint(os.path.join('Generated Documents', expansion.upper()))
    return generator


if __name__ == "__main__":
    MAIN_EXPANSION = 'OTJ'
    BONUS_SHEET = 'OTP'
    QUERIES = [
        'set:otj unique:cards',
        'set:otp unique:cards',
        'set:big unique:cards',
        '(set:spg and date=otj) unique:cards'
    ]

    main(MAIN_EXPANSION, BONUS_SHEET, *QUERIES, print_card_list=True)



