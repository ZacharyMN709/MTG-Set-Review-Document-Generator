from typing import Iterable

from io import BytesIO
from PIL import Image

from core.scryfall import Scryfall
from core.game_concepts.card import Card


class ImageProcessor:
    @classmethod
    def get_face_image(cls, url: str) -> Image.Image:
        image_data = Scryfall.request(url).content
        return Image.open(BytesIO(image_data))

    @classmethod
    def generate_slide_image(cls, card: Card) -> Image.Image:
        front_image = cls.get_face_image(card.front_image_url)
        back_image = cls.get_face_image(card.back_image_url)

        if "Battle" in card.all_types:
            front_image = front_image.rotate(270, expand=True)  # Rotate image by -90 degrees

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
