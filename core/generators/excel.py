from typing import Optional, Any

import os
from pathlib import Path
import pandas as pd

from core.caching import CardCache
from core.game_concepts.card import Card
from core.game_concepts.ordering import order


class ExcelGenerator:
    expansion: str
    bonus_sheet: Optional[str]
    card_cache: CardCache
    day_one_cards: list[Card]
    day_two_cards: list[Card]

    def __init__(self, expansion: str, bonus_sheet: Optional[str], card_cache: CardCache, reviewers: list[str]):
        self.expansion = expansion
        self.bonus_sheet = bonus_sheet
        self.card_cache = card_cache
        self.reviewers = reviewers
        # TODO: See if this can be moved into the cache object.
        self.day_one_cards, self.day_two_cards = order(self.card_cache, self.expansion, self.bonus_sheet)

    def gen_dict_from_card(self, card: Card) -> dict[str, Any]:
        sanitized_name = card.name.replace('"', '')
        mapping_dict = {
            "Card Name": f'=HYPERLINK("{card.card_url}", "{sanitized_name}")',
            "Expansion": card.expansion
        }
        mapping_dict |= {reviewer: "" for reviewer in self.reviewers}
        mapping_dict |= {
            "Color": card.casting_identity,
            "Cost": card.mana_cost,
            "Rarity": card.rarity,
            "Type": card.type_line
        }
        return mapping_dict

    def generate_spreadsheet(self, output_dir: str):
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        path.joinpath()

        file_name = f"{self.expansion} - Grades.xlsx"
        records = [self.gen_dict_from_card(card) for card in self.day_one_cards + self.day_two_cards]
        frame = pd.DataFrame.from_records(records)
        frame.to_excel(os.path.join(output_dir, file_name))
        print(f"Created file '{file_name}'!")

    # TODO: See if this can be moved into the cache object.
    @property
    def sorted_card_list(self) -> list[Card]:
        return self.day_one_cards + self.day_two_cards


def main(
        expansion: str,
        bonus_sheet: Optional[str],
        reviewers: list[str],
        *queries: str,
        print_card_list: bool = False
) -> ExcelGenerator:
    cache = CardCache.from_queries(*queries)
    generator = ExcelGenerator(expansion, bonus_sheet, cache, reviewers)

    if print_card_list:
        print("Cards: ")
        for card in generator.sorted_card_list:
            print(repr(card))
        print(" - - - - - - - - - - \n")

    generator.generate_spreadsheet(os.path.join('../../Generated Documents', expansion.upper()))
    return generator


if __name__ == "__main__":
    MAIN_EXPANSION = 'OTJ'
    BONUS_SHEET = 'OTP'
    REVIEWERS = ['Alex', 'Marc']
    QUERIES = [
        'set:otj unique:cards',
        'set:otp unique:cards',
        'set:big unique:cards',
        '(set:spg and date=otj) unique:cards'
    ]

    main(MAIN_EXPANSION, BONUS_SHEET, REVIEWERS, *QUERIES, print_card_list=True)

