from typing import Iterable

from io import BytesIO
from PIL import Image

from core.scryfall import Scryfall
from core.caching import CardCache


class ImageProcessor:
    def __init__(self, card_cache: CardCache):
        self.card_cache = card_cache

    @classmethod
    def _get_image_url(cls, face) -> str:
        """
        Get the highest resolution image available from a card face
        :param face: The card or card face data.
        :return: A url to the image.
        """
        uris = ['large', 'border_crop', 'normal', 'small', 'art_crop']
        for uri in uris:
            if uri in face["image_uris"]:
                return face["image_uris"][uri]

    def get_face_image(self, card_face: dict) -> Image.Image:
        url = self._get_image_url(card_face)
        image_data = Scryfall.request(url).content
        return Image.open(BytesIO(image_data))

    def generate_slide_image(self, card_name: str) -> Image.Image:
        print(card_name)
        card_data = self.card_cache.get_card_data(card_name)

        if "layout" in card_data and card_data["layout"] != "transform":
            return self.get_face_image(card_data)

        front_image = self.get_face_image(card_data["card_faces"][0])
        back_image = self.get_face_image(card_data["card_faces"][1])

        if "Battle" in card_data["card_faces"][0]["type_line"]:
            front_image = front_image.rotate(270, expand=True)  # Rotate image by -90 degrees

        merge_image_size = (front_image.size[0] + back_image.size[0], max(front_image.size[1], back_image.size[1]))
        merged_image = Image.new("RGBA", merge_image_size, (255, 255, 255, 255))

        front_image_location = (0, (merged_image.size[1] - front_image.size[1]) // 2)
        back_image_location = (front_image.size[0], (merged_image.size[1] - back_image.size[1]) // 2)
        merged_image.paste(front_image, front_image_location)
        merged_image.paste(back_image, back_image_location)
        return merged_image

    def image_generator(self, card_names: Iterable[str]):
        for card_name in card_names:
            yield self.generate_slide_image(card_name)
