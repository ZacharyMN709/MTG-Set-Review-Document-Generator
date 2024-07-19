from typing import Optional, Any

import os
from pathlib import Path
import pandas as pd

from core.data.set_context import SetContext
from core.game_concepts.card import Card


class ExcelGenerator:
    set_context: SetContext

    def __init__(self, set_context: SetContext, reviewers: list[str]):
        self.set_context = set_context
        self.reviewers = reviewers

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

        file_name = f"{self.set_context.set_code} - Grades.xlsx"
        records = [self.gen_dict_from_card(card) for card in self.set_context.sorted_card_list]
        frame = pd.DataFrame.from_records(records)
        frame.to_excel(os.path.join(output_dir, file_name))
        print(f"Created file '{file_name}'!")

    @property
    def sorted_card_list(self) -> list[Card]:
        return self.set_context.sorted_card_list


def main(
        expansion: str,
        bonus_sheet: Optional[str],
        reviewers: list[str],
        *queries: str,
        print_card_list: bool = False
) -> ExcelGenerator:
    context = SetContext.from_queries(expansion, bonus_sheet, *queries, print_card_list=print_card_list)
    generator = ExcelGenerator(context, reviewers)
    generator.generate_spreadsheet(os.path.join('../../Generated Documents', expansion.upper()))
    return generator


if __name__ == "__main__":
    REVIEWERS = ['Alex', 'Marc']

    set_code = 'BLB'
    bonus_set_code = None
    scryfall_queries = [
        "set:blb unique:cards and cn<=261",
        "(set:spg and date=blb) unique:cards",
    ]

    main(set_code, bonus_set_code, REVIEWERS, *scryfall_queries, print_card_list=True)

