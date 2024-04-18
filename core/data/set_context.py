
from core.data.caching import CardCache, CardKey
from core.game_concepts.card import Card
from core.game_concepts.ordering import order


class SetContext:
    set_code: str
    bonus_set_code: str
    card_cache: CardCache
    _day_one_cards: list[Card]
    _day_two_cards: list[Card]

    @classmethod
    def from_expansions(cls, set_code: str, bonus_set_code: str, *expansions: str):
        card_cache = CardCache.from_expansions(*expansions)
        return cls(set_code, bonus_set_code, card_cache)

    @classmethod
    def from_queries(cls, set_code: str, bonus_set_code: str, *queries: str):
        card_cache = CardCache.from_queries(*queries)
        return cls(set_code, bonus_set_code, card_cache)

    @classmethod
    def from_card_keys(cls, set_code: str, bonus_set_code: str, *keys: CardKey):
        card_cache = CardCache.from_card_keys(*keys)
        return cls(set_code, bonus_set_code, card_cache)

    @classmethod
    def from_config(cls):
        # TODO: Load these from a config file
        set_code = None
        bonus_set_code = None
        queries = list()
        return cls.from_queries(set_code, bonus_set_code, *queries)

    def __init__(self, set_code: str, bonus_set_code: str, card_cache: CardCache):
        self.set_code = set_code
        self.bonus_set_code = bonus_set_code
        self.card_cache = card_cache
        self._day_one_cards, self._day_two_cards = list(), list()

        self.card_cache.on_edit = self.on_cache_update

    def get_card_orders(self):
        self._day_one_cards, self._day_two_cards = order(self.card_cache, self.set_code, self.bonus_set_code)

    def on_cache_update(self):
        self._day_one_cards, self._day_two_cards = list(), list()

    @property
    def day_one_cards(self) -> list[Card]:
        if not self._day_one_cards:
            self.get_card_orders()
        return self._day_one_cards

    @property
    def day_two_cards(self) -> list[Card]:
        if not self._day_two_cards:
            self.get_card_orders()
        return self._day_two_cards

    @property
    def sorted_card_list(self) -> list[Card]:
        return self.day_one_cards + self.day_two_cards

