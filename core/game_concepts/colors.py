from typing import Optional

import logging
import re

_mana_symbol_scrub = re.compile('[0-9{}XC]')


def get_color_string(text: Optional[str]) -> str:
    """
    Takes in a string, and attempts to convert it to a color string, with some amount
    of forgiveness for misspelling and casing. If the string is invalid, returns ''.
    Egs. '{2}{G}{G}' -> 'GG', '{2}{G{G}' -> 'GG', 'A' -> ''
    :param text: The string to convert.
    :return: A color string, which contains only characters found in 'WUBRG'.
    """

    # If the string is None, log a warning.
    if text is None:
        logging.warning(f"Invalid color string provided: `None`. Converting to ''.")
        return ''

    # Replace '{', '}', 'X', 'C' and any numerics.
    s = text.strip().upper()
    ret = _mana_symbol_scrub.sub('', s)

    # TODO: Check if this is redundant.
    # If the incoming string was a colorless mana-cost, it will be empty.
    if ret == '':
        return ''

    # Get all the characters that are in WUBRG
    ret = ''.join(c for c in ret if c in 'WUBRG')

    # If the return string is empty, log a warning message.
    if not ret:
        logging.warning(f"Invalid color string provided: {text}. No color values could be found in string.")

    return ret


def get_color_identity(text: str) -> str:
    """
    Takes in a color string, and attempts to convert it to a
    color identity string.
    :param text: The color string to convert.
    :return: A color identity string, a subset of 'WUBRG', in 'WUBRG' order.
    """

    # Get the colour string, and put it into a set to remove duplicate characters.
    color_string = get_color_string(text)
    char_set = set(color_string)

    # Removes any non-COLOR symbols from the set, converting it to a COLOR_IDENTITY
    color_identity = ''.join(c for c in 'WUBRG' if c in char_set)
    return color_identity


def parse_color_list(color_list: list[str]) -> str:
    """
    Takes a lists of colours and combines it into a COLOR_STRING.
    """
    color_str = ''.join(color_list)
    return get_color_identity(color_str)
