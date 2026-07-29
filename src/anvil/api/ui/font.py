import os

from anvil.api.core.core import ANVIL
from anvil.lib.config import CONFIG
from anvil.lib.lib import Directory
from PIL import Image, ImageDraw, ImageFont


class Fonts:
    """A class representing a Fonts."""

    def __init__(self, font_name: str, character_size: int = 32) -> None:
        """Initializes a Fonts instance.

        Parameters:
            font_name (str): The name of the font.
            character_size (int, optional): The size of the character. Defaults to 32.
        """
        if character_size % 16 != 0:
            raise ValueError(
                f"Character size must be a multiple of 16. Font [{font_name}]"
            )
        self._character_size = character_size
        self._font_size = round(character_size * 0.8)
        self._path = os.path.join(CONFIG.RP_PATH, "font")

        extensions = ["ttf", "otf"]
        self._font_image = None
        self._particles_image = None
        for ext in extensions:
            path = os.path.join("assets", "textures", "ui", f"{font_name}.{ext}")
            if os.path.exists(path):
                self.font = ImageFont.truetype(path, self._font_size)
                return

        raise FileNotFoundError(
            f"Font file {font_name} could not be found in assets/textures/ui. Please make sure a .ttf or .otf file exists."
        )

    def generate_font(self):
        """Generates a default8 font image"""
        font_size = round(self._character_size * 0.8)
        image_size = self._character_size * 16

        image = Image.new("RGBA", (image_size, image_size))
        backup_font = ImageFont.truetype("arial.ttf", font_size)

        ascii = "ÀÁÂÈÉÊÍÓÔÕÚßãõǧÎ¹ŒœŞşŴŵŽê§©      !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~⌂"
        extended_ascii = "ÇüéâäàåçêëèïîìÄÅÉ§ÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴├├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■	"
        default8 = ascii + extended_ascii

        offset = [0, 0]

        img_draw = ImageDraw.Draw(image)
        for i in default8:
            font_target = self.font if i in ascii else backup_font

            bbox = font_target.getbbox(i)

            char_height = bbox[3] - bbox[1]

            x = offset[0] * self._character_size - bbox[0]
            y = offset[1] * self._character_size

            img_draw.text((x, y), i, fill=(255, 255, 255), font=font_target)

            offset[0] += 1
            if offset[0] >= 16:
                offset[0] = 0
                offset[1] += 1

        self._font_image = image

        return self

    def generate_numbers_particle(self):
        """Generates a numbers particle from 0 to 999."""
        max_size = int(self.font.getlength("999"))
        image_size = (max_size * 10, self._character_size * 100)

        image = Image.new("RGBA", image_size)
        offset = [0, 0]

        img_draw = ImageDraw.Draw(image)
        for i in range(0, 1000):
            bbox = self.font.getbbox(str(i))

            x = offset[0] * max_size
            y = offset[1] * self._character_size

            img_draw.text((x, y), str(i), fill=(255, 255, 255), font=self.font)

            offset[0] += 1
            if offset[0] >= 10:
                offset[0] = 0
                offset[1] += 1

        self._particles_image = image
        return self

    def queue(self):
        """Queues the font to be exported."""
        ANVIL.__queue__(self)

    def __export__(self):
        """Exports the font configuration."""
        Directory.create(self._path)
        if self._font_image:
            self._font_image.save(os.path.join(self._path, "default8.png"))

        if self._particles_image:
            self._particles_image.save(
                os.path.join("assets", "particles", "numbers.png")
            )

        for file in ["glyph_E1.png"]:
            if os.path.exists(os.path.join("assets", "textures", "ui", file)):
                Directory.copy_files(
                    os.path.join("assets", "textures", "ui"), self._path, file
                )
