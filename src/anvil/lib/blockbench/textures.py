import base64
import os

from anvil.lib.config import CONFIG


class _TexturesManager:
    def __init__(self, filename: str, source: str, bbmodel: dict) -> None:
        config = CONFIG
        self._name = filename
        self._bbmodel = bbmodel

        self._path = os.path.join(
            config.RP_PATH,
            "textures",
            config.NAMESPACE,
            config.PROJECT_NAME,
            source,
            self._name,
        )
        self._textures = {
            texture.get("name").split(".")[0]: texture
            for texture in self._bbmodel["textures"]
        }
        self._queued_textures: dict[str, str | None] = {}

    def queue_texture(self, texture: str, dest_dir: str | None = None) -> None:
        if texture in self._textures:
            self._queued_textures[texture] = dest_dir
        else:
            raise ValueError(
                f"Texture '{texture}' not found in blockbench model '{self._bbmodel['model_identifier']}'."
            )

    def _blend_layers(self, texture_data: dict):
        import colorsys
        import io

        from PIL import Image, ImageChops

        width = texture_data.get("width", 16)
        height = texture_data.get("height", 16)
        base_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        blend_ops = {
            "multiply": ImageChops.multiply,
            "screen": ImageChops.screen,
            "overlay": ImageChops.overlay,
            "hard_light": ImageChops.hard_light,
            "add": ImageChops.add,
            "subtract": lambda l, b: ImageChops.subtract(b, l),
            "difference": lambda l, b: ImageChops.difference(b, l),
            "darken": ImageChops.darker,
            "lighten": ImageChops.lighter,
        }

        for layer in texture_data.get("layers", []):
            if not layer.get("visible", True):
                continue

            data_url = layer.get("data_url", "")
            if not data_url:
                continue

            base64_data = data_url.split("base64,")[-1]
            layer_bytes = base64.b64decode(base64_data)
            layer_img = Image.open(io.BytesIO(layer_bytes)).convert("RGBA")

            # Apply scale if not [1, 1]
            scale = layer.get("scale", [1, 1])
            if scale != [1, 1]:
                new_width = int(round(layer_img.width * scale[0]))
                new_height = int(round(layer_img.height * scale[1]))
                if new_width != layer_img.width or new_height != layer_img.height:
                    layer_img = layer_img.resize(
                        (new_width, new_height), Image.Resampling.NEAREST
                    )

            # Apply opacity directly to the alpha channel
            opacity = layer.get("opacity", 100) / 100.0
            if opacity < 1.0:
                layer_img.putalpha(
                    layer_img.getchannel("A").point(lambda p: int(p * opacity))
                )

            ox, oy = map(int, layer.get("offset", [0, 0]))
            blend_mode = layer.get("blend_mode", "default")

            # Crop overlapping region to perform fast, native Pillow blending
            start_x, end_x = max(0, ox), min(width, ox + layer_img.width)
            start_y, end_y = max(0, oy), min(height, oy + layer_img.height)

            if start_x >= end_x or start_y >= end_y:
                continue

            crop_base = base_img.crop((start_x, start_y, end_x, end_y))
            crop_layer = layer_img.crop(
                (start_x - ox, start_y - oy, end_x - ox, end_y - oy)
            )

            if blend_mode == "default":
                blended_region = Image.alpha_composite(crop_base, crop_layer)
            elif blend_mode == "behind":
                blended_region = Image.alpha_composite(crop_layer, crop_base)
            elif blend_mode == "alpha_mask":
                mask = ImageChops.multiply(
                    crop_layer.convert("L"), crop_layer.getchannel("A")
                )
                r, g, b, a = crop_base.split()
                blended_region = Image.merge(
                    "RGBA", (r, g, b, ImageChops.multiply(a, mask))
                )
            elif blend_mode == "set_opacity":
                r, g, b, a = crop_base.split()
                blended_region = Image.merge(
                    "RGBA", (r, g, b, crop_layer.getchannel("A"))
                )
            elif blend_mode in blend_ops:
                rgb_base = crop_base.convert("RGB")
                rgb_layer = crop_layer.convert("RGB")
                rgb_m = blend_ops[blend_mode](rgb_layer, rgb_base)
                blended_layer = Image.merge(
                    "RGBA", (*rgb_m.split(), crop_layer.getchannel("A"))
                )
                blended_region = Image.alpha_composite(crop_base, blended_layer)
            else:
                # Custom HSL color and divide modes fallback
                px_b = crop_base.load()
                px_l = crop_layer.load()
                blended_region = crop_base.copy()
                px_out = blended_region.load()

                for y_idx in range(crop_base.height):
                    for x_idx in range(crop_base.width):
                        r_b, g_b, b_b, a_b = px_b[x_idx, y_idx]
                        r_t, g_t, b_t, a_t = px_l[x_idx, y_idx]

                        cb = [c / 255.0 for c in (r_b, g_b, b_b)]
                        ct = [c / 255.0 for c in (r_t, g_t, b_t)]
                        ab, at = a_b / 255.0, a_t / 255.0

                        if blend_mode == "divide":
                            cm = [
                                min(b / t, 1.0) if t > 0.0 else 1.0
                                for b, t in zip(cb, ct)
                            ]
                        elif blend_mode == "color":
                            h_b, l_b, s_b = colorsys.rgb_to_hls(*cb)
                            h_t, l_t, s_t = colorsys.rgb_to_hls(*ct)
                            cm = list(colorsys.hls_to_rgb(h_t, l_b, s_t))
                        else:
                            cm = ct

                        a_out = at + ab * (1.0 - at)
                        c_out = [
                            (
                                (m * at + b * ab * (1.0 - at)) / a_out
                                if a_out > 0.0
                                else 0.0
                            )
                            for m, b in zip(cm, cb)
                        ]

                        px_out[x_idx, y_idx] = tuple(
                            max(0, min(255, int(round(c * 255.0)))) for c in c_out
                        ) + (
                            max(0, min(255, int(round(a_out * 255.0)))),
                        )

            base_img.paste(blended_region, (start_x, start_y))

        return base_img

    def __export__(self) -> None:
        import io

        from PIL import Image

        for texture, dest_dir in self._queued_textures.items():
            path = dest_dir if dest_dir is not None else self._path
            os.makedirs(path, exist_ok=True)

            tex_data = self._textures[texture]
            if tex_data.get("layers_enabled", False) and tex_data.get("layers"):
                img = self._blend_layers(tex_data)
                is_blended = True
            else:
                source_str = tex_data.get("source", "")
                base64_data = source_str.split("base64,")[-1]
                image_data = base64.b64decode(base64_data)
                is_blended = False

            file_format = tex_data.get("file_format", "png").lower()
            if file_format in ("tga", "jpeg", "jpg", "webp") or is_blended:
                if not is_blended:
                    img = Image.open(io.BytesIO(image_data))
                out_bytes = io.BytesIO()

                pil_format = {
                    "tga": "TGA",
                    "jpeg": "JPEG",
                    "jpg": "JPEG",
                    "webp": "WEBP",
                    "png": "PNG",
                }.get(file_format, "PNG")

                ext = {
                    "tga": "tga",
                    "jpeg": "jpeg",
                    "jpg": "jpg",
                    "webp": "webp",
                    "png": "png",
                }.get(file_format, "png")

                if pil_format == "JPEG" and img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")

                img.save(out_bytes, format=pil_format)
                with open(os.path.join(path, f"{texture}.{ext}"), "wb") as file:
                    file.write(out_bytes.getvalue())
            else:
                with open(os.path.join(path, f"{texture}.png"), "wb") as file:
                    file.write(image_data)
