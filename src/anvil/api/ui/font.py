import os

from PIL import Image, ImageDraw, ImageFont

from anvil import ANVIL
from anvil.lib.config import CONFIG
from anvil.lib.lib import CopyFiles, FileExists


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
        font_size = round(character_size * 0.8)

        try:
            self.font = ImageFont.truetype(
                f"assets/textures/ui/{font_name}.ttf", font_size
            )
        except FileNotFoundError:
            self.font = ImageFont.truetype(
                f"assets/textures/ui/{font_name}.otf", font_size
            )
        except:
            self.font = ImageFont.truetype(f"{font_name}.ttf", font_size)

        self.character_size = character_size
        self._path = os.path.join(CONFIG.RP_PATH, "font")

    def generate_font(self):
        """Generates a default8 font image"""

        font_size = round(self.character_size * 0.8)
        image_size = self.character_size * 16

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

            x = offset[0] * self.character_size - bbox[0]
            y = offset[1] * self.character_size

            img_draw.text((x, y), i, fill=(255, 255, 255), font=font_target)

            offset[0] += 1
            if offset[0] >= 16:
                offset[0] = 0
                offset[1] += 1

            image.save(os.path.join("assets", "textures", "ui", "default8.png"))

        return self

    def generate_numbers_particle(self):
        """Generates a numbers particle from 0 to 999."""
        img_path = os.path.join("assets", "particles", "numbers.png")
        particle_path = os.path.join("assets", "particles", "numbers.particle.json")

        max_size = int(self.font.getlength("999"))
        image_size = (max_size * 10, self.character_size * 100)

        if not FileExists(img_path):
            image = Image.new("RGBA", image_size)
            offset = [0, 0]

            img_draw = ImageDraw.Draw(image)
            for i in range(0, 1000):
                bbox = self.font.getbbox(str(i))

                x = offset[0] * max_size
                y = offset[1] * self.character_size

                img_draw.text((x, y), str(i), fill=(255, 255, 255), font=self.font)

                offset[0] += 1
                if offset[0] >= 10:
                    offset[0] = 0
                    offset[1] += 1

                image.save(img_path)

        # if not FileExists(particle_path):
        #    File(
        #        "numbers.particle.json",
        #        {
        #            "format_version": "1.10.0",
        #            "particle_effect": {
        #                "description": {
        #                    "identifier": f"{CONFIG.NAMESPACE}:numbers",
        #                    "basic_render_parameters": {"material": "particles_alpha", "texture": "textures/particle/numbers"},
        #                },
        #                "components": {
        #                    "minecraft:emitter_local_space": {"position": True, "rotation": True, "velocity": True},
        #                    "minecraft:emitter_rate_steady": {"spawn_rate": 10, "max_particles": 1},
        #                    "minecraft:emitter_lifetime_looping": {"active_time": 1},
        #                    "minecraft:particle_lifetime_expression": {"max_lifetime": 0.75},
        #                    "minecraft:emitter_shape_point": {"offset": [0, 0, 0]},
        #                    "minecraft:particle_initial_speed": 0,
        #                    "minecraft:particle_motion_dynamic": {"linear_drag_coefficient": 1},
        #                    "minecraft:particle_appearance_billboard": {
        #                        "size": [0.18, 0.1],
        #                        "facing_camera_mode": "rotate_xyz",
        #                        "direction": {"mode": "custom", "custom_direction": [0, 0, -1]},
        #                        "uv": {
        #                            "texture_width": image_size[0],
        #                            "texture_height": image_size[1],
        #                            "uv": ["v.number_x_uv", "v.number_y_uv"],
        #                            "uv_size": [image_size[0] // 10, image_size[1] // 100],
        #                        },
        #                    },
        #                },
        #            },
        #        },
        #        os.path.join("assets", "particles"),
        #        "w",
        #    )

        return self

    def queue(self):
        """Queues the font to be exported."""
        ANVIL._queue(self)

    def _export(self):
        """Exports the font configuration."""
        for file in ["glyph_E1.png", "default8.png"]:
            if FileExists(os.path.join("assets", "textures", "ui", file)):
                CopyFiles(os.path.join("assets", "textures", "ui"), self._path, file)
