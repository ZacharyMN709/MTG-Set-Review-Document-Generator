from typing import Optional, Iterable
import os
from pathlib import Path
import tempfile
from io import BytesIO

from pptx import Presentation as NewPresentation
from pptx.util import Cm
from pptx.presentation import Presentation
from PIL.Image import Image
from PIL import Image

from core.scryfall import Scryfall
from core.caching import CardCache
from core.game_concepts.card import Card
from core.game_concepts.ordering import order


SLIDE_HEIGHT = 19.05
SLIDE_WIDTH = 25.40

SCRYFALL_DPI = 96
INCH_TO_CM = 2.54
MINIMUM_MARGIN = 2


def new_powerpoint_from_images(file_name: str, card_images: Iterable[Image]):
    presentation = NewPresentation()
    for image in card_images:
        add_centered_image_slide(presentation, image)
    presentation.save(file_name)


def add_centered_image_slide(presentation: Presentation, image: Image):
    image_width = (image.size[0] / SCRYFALL_DPI) * INCH_TO_CM
    image_height = (image.size[1] / SCRYFALL_DPI) * INCH_TO_CM
    width_ratio = image_width / (SLIDE_WIDTH - MINIMUM_MARGIN * 2)
    height_ratio = image_height / (SLIDE_HEIGHT - MINIMUM_MARGIN * 2)
    is_landscape = width_ratio >= height_ratio

    if is_landscape:
        new_image_width = image_width / width_ratio
        new_image_height = image_height / width_ratio
    else:
        new_image_width = image_width / height_ratio
        new_image_height = image_height / height_ratio

    x_position = (SLIDE_WIDTH - new_image_width) / 2
    y_position = (SLIDE_HEIGHT - new_image_height) / 2

    temporary_image_file = tempfile.NamedTemporaryFile(suffix=".png")
    image.save(temporary_image_file)

    blank_slide_layout = presentation.slide_layouts[6]
    slide = presentation.slides.add_slide(blank_slide_layout)
    slide.shapes.add_picture(
        temporary_image_file, Cm(x_position), Cm(y_position), width=Cm(new_image_width), height=Cm(new_image_height)
    )


class ImageProcessor:
    @classmethod
    def get_face_image(cls, url: str) -> Image.Image:
        image_data = Scryfall.request(url).content
        return Image.open(BytesIO(image_data))

    @classmethod
    def generate_slide_image(cls, card: Card) -> Image.Image:
        front_image = cls.get_face_image(card.front_image_url)
        if "Battle" in card.all_types or card.layout == "split":
            front_image = front_image.rotate(270, expand=True)

        if not card.back_image_url:
            return front_image

        back_image = cls.get_face_image(card.back_image_url)
        merge_image_size = (front_image.size[0] + back_image.size[0], max(front_image.size[1], back_image.size[1]))
        merged_image = Image.new("RGBA", merge_image_size, (255, 255, 255, 255))

        front_image_location = (0, (merged_image.size[1] - front_image.size[1]) // 2)
        back_image_location = (front_image.size[0], (merged_image.size[1] - back_image.size[1]) // 2)
        merged_image.paste(front_image, front_image_location)
        merged_image.paste(back_image, back_image_location)
        return merged_image

    @classmethod
    def image_generator(cls, cards: Iterable[Card]):
        for card in cards:
            yield cls.generate_slide_image(card)


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
        new_powerpoint_from_images(
            os.path.join(output_dir, day_one_file_name),
            ImageProcessor.image_generator(self.day_one_cards)
        )
        print(f"Created file '{day_one_file_name}'!")

        day_two_file_name = f"{self.expansion} - Rares and Mythics.pptx"
        new_powerpoint_from_images(
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

    new_powerpoint_from_images(
        os.path.join(output_dir, file_name),
        ImageProcessor.image_generator(cards)
    )
    print(f"Created file '{file_name}'!")


if __name__ == "__main__":
    debug()



