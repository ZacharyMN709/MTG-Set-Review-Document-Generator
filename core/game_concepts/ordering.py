from typing import TypeVar, Optional, Iterable

from itertools import chain
from functools import cmp_to_key

from core.data.caching import CardCache
from core.game_concepts.colors import GROUP_COLOR_COMBINATIONS, SET_REVIEW_COLOR_ORDER
from core.game_concepts.card import Card

T = TypeVar('T')

RARITIES = ['common', 'uncommon', 'rare', 'mythic']


def flatten_lists(lists: Iterable[list[T]]) -> list[T]:
    return [item for sublist in lists for item in sublist]


def weave_lists(l1: list[T], l2: list[T]) -> list[T]:
    if len(l1) != len(l2):
        raise ValueError("List length must be equal!")
    return list(chain.from_iterable(zip(l1, l2)))


def set_review_color_sort(card_1: Card, card_2: Card):
    return SET_REVIEW_COLOR_ORDER[card_1.color_identity] - SET_REVIEW_COLOR_ORDER[card_2.color_identity]


def split_by_rarities(card_list: list[Card]):
    commons, uncommons, rares, mythics = [[card for card in card_list if card.rarity == rarity] for rarity in RARITIES]
    return commons, uncommons, rares, mythics


def split_by_color(card_list: list[Card]) -> list[list[Card]]:
    def get_by_color(color: str) -> list[Card]:
        return sorted([card for card in card_list if card.casting_identity == color], key=lambda x: x.cmc)
    temp = [get_by_color(color) for color in GROUP_COLOR_COMBINATIONS]
    colorless_temp = temp[0]
    colorless = [x for x in colorless_temp if 'Land' not in x.types]
    land = [x for x in colorless_temp if 'Land' in x.types]
    return [land, colorless] + temp[1:]


def sort_for_day_one(cards: list[Card]) -> list[Card]:
    commons, uncommons, _, _ = split_by_rarities(cards)
    commons_by_color = split_by_color(commons)
    uncommons_by_color = split_by_color(uncommons)

    key = cmp_to_key(set_review_color_sort)
    common_lands = sorted(commons_by_color[0], key=key)
    uncommon_lands = sorted(uncommons_by_color[0], key=key)
    lands = flatten_lists([common_lands, uncommon_lands])

    colorless = flatten_lists([commons_by_color[1], uncommons_by_color[1]])
    single_colored = flatten_lists(weave_lists(commons_by_color[2:7], uncommons_by_color[2:7]))
    signposts = flatten_lists(weave_lists(commons_by_color[7:], uncommons_by_color[7:]))

    return signposts + colorless + lands + single_colored


def sort_for_day_two(cards: list[Card]) -> list[Card]:
    _, _, rares, mythics = split_by_rarities(cards)
    by_color = split_by_color(rares + mythics)
    return flatten_lists(by_color[7:] + by_color[2:7] + by_color[0:2])


def sort_for_bonus_sheet(cards: list[Card]):
    return sort_for_day_one(cards) + sort_for_day_two(cards)


def order(cache: CardCache, expansion: str, bonus_sheet: Optional[str]) -> tuple[list[Card], list[Card]]:
    main_set_cards = cache.card_list(expansion)

    if bonus_sheet:
        bonus_sheet_cards = cache.card_list(bonus_sheet)
        bonus_sheet_cards = sort_for_bonus_sheet(bonus_sheet_cards)
    else:
        bonus_sheet_cards = list()

    the_list_cards = [card for card in cache.card_list() if card.expansion not in {expansion, bonus_sheet, 'SPG'}]
    the_list_cards = sort_for_bonus_sheet(the_list_cards)

    special_quests = cache.card_list('SPG')
    special_quests = sort_for_bonus_sheet(special_quests)

    day_one_cards = sort_for_day_one(main_set_cards)
    day_two_cards = sort_for_day_two(main_set_cards) + bonus_sheet_cards + the_list_cards + special_quests
    return day_one_cards, day_two_cards
