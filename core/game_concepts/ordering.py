from typing import TypeVar, Iterable

from itertools import chain

from core.game_concepts.colors import GROUP_COLOR_COMBINATIONS
from core.game_concepts.card import Card

T = TypeVar('T')

RARITIES = ['common', 'uncommon', 'rare', 'mythic']


def flatten_lists(lists: Iterable[list[T]]) -> list[T]:
    return [item for sublist in lists for item in sublist]


def weave_lists(l1: list[T], l2: list[T]) -> list[T]:
    if len(l1) != len(l2):
        raise ValueError("List length must be equal!")
    return list(chain.from_iterable(zip(l1, l2)))


def split_by_color(card_list: list[Card]) -> list[list[Card]]:
    def get_by_color(color: str) -> list[Card]:
        return sorted([card for card in card_list if card.casting_identity == color], key=lambda x: x.cmc)
    temp = [get_by_color(color) for color in GROUP_COLOR_COMBINATIONS]
    colorless_temp = temp[0]
    colorless = [x for x in colorless_temp if 'Land' not in x.types]
    land = [x for x in colorless_temp if 'Land' in x.types]
    return [land, colorless] + temp[1:]


def gen_set_review_chunks(card_list: list[Card]) -> tuple[list[Card], list[Card], list[Card], list[Card], list[Card]]:
    commons, uncommons, rares, mythics = [[card for card in card_list if card.rarity == rarity] for rarity in RARITIES]
    common_sublists = split_by_color(commons)
    uncommon_sublists = split_by_color(uncommons)
    rare_sublists = split_by_color(rares + mythics)

    lands = flatten_lists([common_sublists[0], uncommon_sublists[0]])
    colorless = flatten_lists([common_sublists[1], uncommon_sublists[1]])
    single_colored = flatten_lists(weave_lists(common_sublists[2:7], uncommon_sublists[2:7]))
    signposts = flatten_lists(weave_lists(common_sublists[7:], uncommon_sublists[7:]))
    rares_and_mythics = flatten_lists(rare_sublists[2:7] + rare_sublists[0:2] + rare_sublists[7:])

    return signposts, colorless, lands, single_colored, rares_and_mythics


def order_for_set_review(card_list: list[Card]) -> list[Card]:
    return flatten_lists(gen_set_review_chunks(card_list))

