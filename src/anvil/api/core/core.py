import base64
import io
import math
import os
import traceback as tb
import zipfile
from typing import Literal, Optional

import click
from halo import Halo
from PIL import Image

from anvil.api.actors.materials import MaterialsObject
from anvil.api.core.sounds import BlocksJSONObject, MusicDefinition, SoundDefinition, SoundEvent
from anvil.api.core.textures import FlipBookTexturesObject, ItemTexturesObject, TerrainTexturesObject
from anvil.lib.blockbench import _Blockbench
from anvil.lib.config import CONFIG, ConfigPackageTarget, _AnvilConfig
from anvil.lib.format_versions import MANIFEST_VERSION, MODULE_MINECRAFT_SERVER, MODULE_MINECRAFT_SERVER_UI
from anvil.lib.lib import (
    CreateDirectory,
    File,
    FileExists,
    RemoveDirectory,
    process_subcommand,
    validate_namespace_project_name,
    zipit,
)
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject, JsonSchemes
from anvil.lib.translator import AnvilTranslator

from ...__version__ import __version__


def resize(
    image: Image.Image,
    name: str,
    output: str,
    size,
    quality=95,
    dpi=72,
    overlay: Image.Image = None,
):
    resized = image.resize(size)

    if overlay:
        overlay = overlay.resize(size)
        resized.paste(overlay, mask=overlay.split()[3])

    resized.convert("RGB").save(
        os.path.join(output, name),
        dpi=(dpi, dpi),
        quality=quality,
    )


def extract_world_pack(extract_world: str | None = None):
    if extract_world != None and type(extract_world) is str:
        RemoveDirectory(CONFIG._WORLD_PATH)
        with zipfile.ZipFile(os.path.join("world", f"{extract_world}.mcworld"), "r") as zip_ref:
            zip_ref.extractall(CONFIG._WORLD_PATH)


def manifests(extract_world: str | None = None):
    release_list = [int(i) for i in CONFIG._RELEASE.split(".")]
    if extract_world != None and type(extract_world) is str:
        File(
            "manifest.json",
            JsonSchemes.manifest_world(release_list),
            CONFIG._WORLD_PATH,
            "w",
        )
        File(
            "world_resource_packs.json",
            JsonSchemes.world_packs(release_list, CONFIG._RP_UUID),
            CONFIG._WORLD_PATH,
            "w",
        )
        File(
            "world_behavior_packs.json",
            JsonSchemes.world_packs(release_list, CONFIG._BP_UUID),
            CONFIG._WORLD_PATH,
            "w",
        )


def scriptapi():
    if any([CONFIG._SCRIPT_API, CONFIG._SCRIPT_UI]):
        if not FileExists("tsconfig.json"):
            File(
                "tsconfig.json",
                JsonSchemes.tsconfig(CONFIG.BP_PATH),
                "",
                "w",
                False,
            )
        if not FileExists("esbuild.js") and "esbuild" in CONFIG._SCRIPT_BUNDLE_SCRIPT:
            File(
                "esbuild.js",
                JsonSchemes.esbuild_config_js(CONFIG.BP_PATH, CONFIG._MINIFY),
                "",
                "w",
                False,
            )
        if not FileExists("package.json"):
            File(
                "package.json",
                JsonSchemes.package_json(
                    CONFIG.PROJECT_NAME,
                    CONFIG._RELEASE,
                    CONFIG.PROJECT_DESCRIPTION,
                    CONFIG.COMPANY,
                ),
                "",
                "w",
                True,
            )


def addon_object_exception(object: AddonObject, e: Exception):
    full_traceback = tb.format_exc()
    creation_info = f"<{object.__class__.__name__} created from:\n{''.join(getattr(object, "_created_from", None))}>"
    click.echo(click.style(f"\r{'='*60}", fg="red"), err=True)
    click.echo(click.style(f"\r\nCreation Context:", fg="cyan"), err=True)
    click.echo(click.style(f"\r{creation_info}", fg="white"), err=True)
    click.echo(click.style(f"\r\nFull Traceback:", fg="cyan"), err=True)
    click.echo(click.style(f"\r{full_traceback}", fg="white"), err=True)
    click.echo(click.style(f"\r{'='*60}", fg="red"), err=True)
    click.echo(
        click.style(
            f"\rERROR EXPORTING OBJECT: {getattr(object, '_name', 'Unknown')}",
            fg="red",
        ),
        err=True,
    )
    click.echo(click.style(f"\r{'='*60}", fg="red"), err=True)
    click.echo(
        click.style(
            f"\rObject Type: {object.__class__.__name__}",
            fg="yellow",
        ),
        err=True,
    )
    click.echo(
        click.style(
            f"\rObject Name: {getattr(object, '_name', 'Unknown')}",
            fg="yellow",
        ),
        err=True,
    )
    click.echo(click.style(f"\rObject Content: {object._content}", fg="yellow"), err=True)
    click.echo(click.style(f"\rError Message: {str(e)}", fg="red"), err=True)
    click.echo(click.style(f"\r{'='*60}", fg="red"), err=True)


@Halo(text="Processing Art", spinner="dots")
def process_art(
    config: _AnvilConfig,
    apply_overlay: bool = False,
    zip: bool = True,
):
    """Process marketing art for packaging."""
    pack_icon_size = (256, 256)
    store_screenshot_size = (800, 450)
    marketing_screenshot_size = (1920, 1080)

    source = os.path.join("marketing")
    output_store = os.path.join("output", "Store Art")
    output_marketing = os.path.join("output", "Marketing Art")

    if zip:
        CreateDirectory(output_store)
        CreateDirectory(output_marketing)

        if FileExists(os.path.join(source, "keyart.png")):
            original = Image.open(os.path.join(source, "keyart.png")).convert("RGB")
            overlay = None

            if apply_overlay:
                overlay = Image.open(os.path.join(source, "keyart_overlay.png"))

            if config._TARGET == ConfigPackageTarget.WORLD:
                resize(
                    original,
                    "world_icon.jpeg",
                    config._WORLD_PATH,
                    store_screenshot_size,
                    95,
                    72,
                    overlay,
                )
            resize(
                original,
                f"{config.PROJECT_NAME}_Thumbnail_0.jpg",
                output_store,
                store_screenshot_size,
                95,
                72,
                overlay,
            )
            resize(
                original,
                f"{config.PROJECT_NAME}_MarketingKeyArt.jpg",
                output_marketing,
                marketing_screenshot_size,
                100,
                300,
                overlay,
            )

        else:
            raise FileNotFoundError("keyart.png not found in marketing directory. Please ensure the file exists.")

        if FileExists(os.path.join(source, "panorama.png")):
            original = Image.open(os.path.join(source, "panorama.png"))
            scale_factor = 450 / original.size[1]
            if (round(original.size[0] * scale_factor)) > 4000:
                raise RuntimeError(
                    f"panorama.png width exceeds 4000 pixels when resized to 450 pixels in height. Please use a smaller image. The recommended original size for this image would be {math.floor(4000 / scale_factor)}x450 pixels."
                )

            resize(
                original,
                f"{config.PROJECT_NAME}_panorama_0.jpg",
                output_store,
                (round(original.size[0] * scale_factor), 450),
                95,
                72,
            )

        else:
            click.echo(
                click.style(
                    f"\r[INFO]: panorama.png does not exist. It is optional but might have been left out unintentionally.",
                    fg="yellow",
                )
            )

        for i in range(999):
            if not FileExists(os.path.join(source, f"{i}.png")):
                if i < 5:
                    raise FileNotFoundError(f"{i}.png not found in marketing directory. Please ensure the file exists.")
                break
            else:
                original = Image.open(os.path.join(source, f"{i}.png"))
                resize(
                    original,
                    f"{config.PROJECT_NAME}_screenshot_{i}.jpg",
                    output_store,
                    store_screenshot_size,
                    95,
                    72,
                )
                resize(
                    original,
                    f"{config.PROJECT_NAME}_MarketingScreenshot_{i}.jpg",
                    output_marketing,
                    marketing_screenshot_size,
                    100,
                    300,
                )

        if FileExists(os.path.join(source, "partner_art.png")):
            original = Image.open(os.path.join(source, "partner_art.png"))

            resize(
                original,
                f"{config.PROJECT_NAME}_PartnerArt.jpg",
                output_marketing,
                marketing_screenshot_size,
                100,
                300,
            )

        else:
            raise FileNotFoundError("partner_art.png not found in marketing directory. Please ensure the file exists.")

        if FileExists(os.path.join(source, "pack_icon.png")):
            original = Image.open(os.path.join(source, "pack_icon.png"))
            resize(
                original,
                f"{config.PROJECT_NAME}_packicon_0.jpg",
                output_store,
                pack_icon_size,
            )
        else:
            raise FileNotFoundError("pack_icon.png not found in marketing directory. Please ensure the file exists.")


@Halo(text="Generating technical notes", spinner="dots")
def generate_technical_notes_pdf(config: _AnvilConfig):
    """Generates a technical notes PDF that contains information about included entities, blocks, items, sounds and more."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    def add_table(section_name: str, data: dict[bool, set[str]]):
        title_style.spaceBefore = 0
        title_style.fontSize = 14
        title_style.textColor = colors.royalblue
        title = Paragraph(section_name, title_style)

        converted_data = []
        vanilla_true_rows = []

        for idx, (row, columns) in enumerate(data.items()):
            vals = []
            for col_name, col_values in columns.items():
                value_string = "<br/>".join(col_values)
                if col_name != "vanilla":
                    vals.append(Paragraph(value_string, styles["Normal"]))
                elif value_string == "True":
                    vanilla_true_rows.append(idx)
            converted_data.append([Paragraph(row, styles["Normal"]), *vals])

        table = Table(
            converted_data,
            hAlign="LEFT",
            colWidths=doc.width / len(converted_data[0]),
        )

        style_commands = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
        for row in vanilla_true_rows:
            style_commands.append(("BACKGROUND", (0, row), (-1, row), colors.lightgreen))
        table.setStyle(TableStyle(style_commands))

        return title, Spacer(1, 0.3 * cm), table, Spacer(1, 1 * cm)

    doc = SimpleDocTemplate(
        os.path.join("output", "technical_notes.pdf"),
        pagesize=A4,
        leftMargin=1 * cm,
        rightMargin=1 * cm,
        topMargin=1 * cm,
        bottomMargin=1 * cm,
        title=f"{config.DISPLAY_NAME} Technical Notes",
        author=config.COMPANY,
        subject=f"{config.DISPLAY_NAME} Technical Notes",
        creator=f"Anvil@stark_lg {__version__}",
    )
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    body_style = styles["BodyText"]
    bullet_style = styles["Bullet"]

    elements = [
        Paragraph(f"{config.DISPLAY_NAME}:", title_style),
        Paragraph(f"Developed by: {config.COMPANY}", body_style),
        Paragraph(
            f'Generated with <a href="https://github.com/StarkTMA/Anvil"><u><font color="blue">StarkTMA/Anvil {__version__}</font></u></a>',
            body_style,
        ),
        Spacer(1, 1 * cm),
        Paragraph("General information:", title_style),
        Paragraph(
            "The following technical notes have been entirely generated from source code using Anvil.",
            body_style,
        ),
        Paragraph(
            "Features overwriting vanilla defaults will be highlighted in green.",
            bullet_style,
            "*",
        ),
        Spacer(1, 1 * cm),
        *add_table("Entities:", config.Report.dict[ReportType.ENTITY]),
        *add_table("Attachables:", config.Report.dict[ReportType.ATTACHABLE]),
        *add_table("Items:", config.Report.dict[ReportType.ITEM]),
        *add_table("Blocks:", config.Report.dict[ReportType.BLOCK]),
        *add_table("Particles:", config.Report.dict[ReportType.PARTICLE]),
        *add_table("Sounds:", config.Report.dict[ReportType.SOUND]),
    ]

    doc.build(elements)


@Halo(text="Packaging ZIP", spinner="dots")
def package_zip_core(
    config: _AnvilConfig,
    apply_overlay: bool = False,
    generate_technical_notes: bool = False,
):
    """Core logic for packaging the project into a zip file for Marketplace."""
    process_art(config, apply_overlay)

    content_structure = {
        os.path.join("output", "Store Art"): os.path.join("Store Art"),
        os.path.join("output", "Marketing Art"): os.path.join("Marketing Art"),
    }

    if config._TARGET == ConfigPackageTarget.ADDON:
        content_structure.update(
            {
                config.RP_PATH: os.path.join(
                    "Content",
                    "resource_packs",
                    f"RP_{config._PASCAL_PROJECT_NAME}",
                ),
                config.BP_PATH: os.path.join(
                    "Content",
                    "behavior_packs",
                    f"BP_{config._PASCAL_PROJECT_NAME}",
                ),
            }
        )

    else:
        content_structure.update(
            {
                config.RP_PATH: os.path.join(
                    "Content",
                    "world_template",
                    "resource_packs",
                    f"RP_{config._PASCAL_PROJECT_NAME}",
                ),
                config.BP_PATH: os.path.join(
                    "Content",
                    "world_template",
                    "behavior_packs",
                    f"BP_{config._PASCAL_PROJECT_NAME}",
                ),
                os.path.join(config._WORLD_PATH, "texts"): os.path.join("Content", "world_template", "texts"),
                os.path.join(config._WORLD_PATH, "level.dat"): os.path.join("Content", "world_template"),
                os.path.join(config._WORLD_PATH, "levelname.txt"): os.path.join("Content", "world_template"),
                os.path.join(config._WORLD_PATH, "manifest.json"): os.path.join("Content", "world_template"),
                os.path.join(config._WORLD_PATH, "world_icon.jpeg"): os.path.join("Content", "world_template"),
                os.path.join(config._WORLD_PATH, "world_behavior_packs.json"): os.path.join(
                    "Content", "world_template"
                ),
                os.path.join(config._WORLD_PATH, "world_resource_packs.json"): os.path.join(
                    "Content", "world_template"
                ),
            }
        )
        if not config._RANDOM_SEED:
            content_structure.update(
                {
                    os.path.join(config._WORLD_PATH, "db"): os.path.join("Content", "world_template", "db"),
                }
            )

    zipit(
        os.path.join("output", f"{config.PROJECT_NAME}.zip"),
        content_structure,
    )

    RemoveDirectory(os.path.join("output", "Store Art"))
    RemoveDirectory(os.path.join("output", "Marketing Art"))

    if generate_technical_notes:
        generate_technical_notes_pdf(config)


@Halo(text="Packaging mcaddon", spinner="dots")
def mcaddon_core(config):
    """Core logic for packaging the project into a .mcaddon file."""
    process_art(config, False, False)

    content_structure = {
        config.RP_PATH: f"RP_{config.PROJECT_NAME}",
        config.BP_PATH: f"BP_{config.PROJECT_NAME}",
    }

    zipit(
        os.path.join("output", f"{config.PROJECT_NAME}.mcaddon"),
        content_structure,
    )


@Halo(text="Packaging mcworld", spinner="dots")
def mcworld_core(config: _AnvilConfig):
    """Core logic for packaging the project into a .mcworld file."""
    process_art(config, False, False)

    content_structure = {
        config.RP_PATH: os.path.join("resource_packs", f"RP_{config.PROJECT_NAME}"),
        config.BP_PATH: os.path.join("behavior_packs", f"BP_{config.PROJECT_NAME}"),
        os.path.join(config._WORLD_PATH, "texts"): "texts",
        os.path.join(config._WORLD_PATH, "level.dat"): "",
        os.path.join(config._WORLD_PATH, "levelname.txt"): "",
        os.path.join(config._WORLD_PATH, "manifest.json"): "",
        os.path.join(config._WORLD_PATH, "world_icon.jpeg"): "",
        os.path.join(config._WORLD_PATH, "world_behavior_packs.json"): "",
        os.path.join(config._WORLD_PATH, "world_resource_packs.json"): "",
    }

    zipit(
        os.path.join("output", f"{config.PROJECT_NAME}.mcworld"),
        content_structure,
    )


@Halo(text="Compiling", spinner="dots")
def compile_objects(anvil: "_Anvil", extract_world: str = None):
    extract_world_pack(extract_world)
    manifests(extract_world)
    scriptapi()

    ItemTexturesObject().queue()
    TerrainTexturesObject().queue()
    FlipBookTexturesObject().queue()
    SoundDefinition().queue()
    SoundEvent().queue()
    MusicDefinition().queue()
    BlocksJSONObject().queue()
    MaterialsObject().queue()
    _Blockbench._export()
    anvil._queue(AnvilTranslator())
    ManifestBP().queue()
    ManifestRP().queue()

    from anvil.api.blocks.blocks import _PermutationComponents

    if _PermutationComponents._count > 10000:
        if CONFIG._TARGET == ConfigPackageTarget.ADDON:
            raise RuntimeError(
                f"\rTotal Block permutations exceeded 10000 ({_PermutationComponents._count}). Addons must not exceed this limit."
            )
        else:
            click.echo(
                click.style(
                    f"\r[INFO]: Total Block permutations exceeded 10000 ({_PermutationComponents._count}). This may cause issues when submitting to the Marketplace.",
                    fg="yellow",
                )
            )

    for object in anvil._objects_list:
        try:
            object._export()
        except Exception as e:
            addon_object_exception(object, e)

    if CONFIG._TARGET == ConfigPackageTarget.ADDON:
        if len(CONFIG._RP_UUID) > 1:
            raise RuntimeError(
                "Multiple resource pack UUIDs found. Please ensure only one UUID is set for the resource pack."
            )
        if len(CONFIG._BP_UUID) > 1:
            raise RuntimeError(
                "Multiple behavior pack UUIDs found. Please ensure only one UUID is set for the behavior pack."
            )

    if CONFIG._SCRIPT_API:
        process_subcommand(
            CONFIG._SCRIPT_BUNDLE_SCRIPT + f' --outdir="{os.path.join(CONFIG.BP_PATH, "scripts")}"',
            "Building scripts error",
        )

    source = os.path.join("marketing")
    pack_icon_size = (256, 256)

    if FileExists(os.path.join(source, "pack_icon.png")):
        original = Image.open(os.path.join(source, "pack_icon.png"))
        resize(original, "pack_icon.png", CONFIG.BP_PATH, pack_icon_size)
        resize(original, "pack_icon.png", CONFIG.RP_PATH, pack_icon_size)

    else:
        click.echo(
            click.style(
                f"\r[INFO]: pack_icon.png not found in marketing directory. Using placeholder pack icon.",
                fg="yellow",
            )
        )
        placeholder_base64 = "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"
        placeholder_bytes = base64.b64decode(placeholder_base64)
        placeholder_image = Image.open(io.BytesIO(placeholder_bytes))

        resize(placeholder_image, "pack_icon.png", CONFIG.BP_PATH, pack_icon_size)
        resize(placeholder_image, "pack_icon.png", CONFIG.RP_PATH, pack_icon_size)

    anvil._compiled = True


@Halo(text="Translating", spinner="dots")
def translate(languages: Optional[list[str]] = None) -> None:
    """Translates the project."""
    AnvilTranslator().auto_translate_all(languages)


class ManifestRP(AddonObject):
    _instance = None
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH)
    _setting_ids: set[str] = set()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ManifestRP, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initializes a ManifestRP instance."""
        if not hasattr(self, "_initialized"):
            super().__init__("manifest")
            self.content(JsonSchemes.manifest_rp(version=CONFIG._RELEASE))
            self._initialized = True

    @property
    def settings(self) -> "_ManifestSettings":
        """Returns a Manifest Settings object to add settings to the manifest."""
        return _ManifestSettings(self)

    def queue(self):
        if CONFIG._PBR:
            self._content.update({"capabilities": ["pbr"]})

        if CONFIG._TARGET == "addon":
            self._content["header"]["pack_scope"] = "world"
            self._content["metadata"]["product_type"] = "addon"

        return super().queue()


class ManifestBP(AddonObject):
    _instance = None
    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH)
    _setting_ids: set[str] = set()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ManifestBP, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initializes a ManifestBP instance."""
        if not hasattr(self, "_initialized"):
            super().__init__("manifest")
            self.content(JsonSchemes.manifest_bp(version=CONFIG._RELEASE))
            self._initialized = True

    @property
    def settings(self) -> "_ManifestSettings":
        """Returns a Manifest Settings object to add settings to the manifest."""
        if not CONFIG._PREVIEW:
            raise RuntimeError("Behaviour Pack Settings are currently only supported in current preview builds.")
        return _ManifestSettings(self)

    def queue(self):
        if CONFIG._SCRIPT_API:
            self._content["modules"].append(
                {
                    "uuid": CONFIG._SCRIPT_MODULE_UUID,
                    "version": CONFIG._RELEASE,
                    "type": "script",
                    "language": "javascript",
                    "entry": "scripts/main.js",
                }
            )
            self._content["dependencies"].append(
                {
                    "module_name": "@minecraft/server",
                    "version": MODULE_MINECRAFT_SERVER,
                }
            )
            if CONFIG._SCRIPT_UI:
                self._content["dependencies"].append(
                    {
                        "module_name": "@minecraft/server-ui",
                        "version": MODULE_MINECRAFT_SERVER_UI,
                    }
                )

        if CONFIG._TARGET == "addon":
            self._content["header"]["pack_scope"] = "world"
            self._content["metadata"]["product_type"] = "addon"

        return super().queue()


class _ManifestSettings:
    def __init__(self, manifest: ManifestRP | ManifestBP):
        if MANIFEST_VERSION < 3:
            raise RuntimeError("Settings labels are only supported in manifest version 3 and above.")
        self.manifest = manifest

        # Initialize settings in _content if not present
        if "settings" not in self.manifest._content:
            self.manifest._content["settings"] = []

    def label(self, label: str):
        self.manifest._content["settings"].append({"type": "label", "text": label})
        return self

    def toggle(self, id: str, text: str, default: bool = True):
        if id in self.manifest._setting_ids:
            raise ValueError(f"Setting ID '{id}' is already used.")

        self.manifest._setting_ids.add(id)
        self.manifest._content["settings"].append(
            {
                "type": "toggle",
                "name": f"{CONFIG.NAMESPACE}:{id}",
                "text": text,
                "default": default,
            }
        )
        return self

    def slider(self, id: str, text: str, min: int, max: int, step: int, default: int):
        if min >= max:
            raise ValueError(f"Min value '{min}' must be less than max '{max}'.")

        if step <= 0:
            raise ValueError(f"Step value '{step}' must be greater than 0.")

        if not (min <= default <= max):
            raise ValueError(f"Default value '{default}' must be between min '{min}' and max '{max}'.")

        if id in self.manifest._setting_ids:
            raise ValueError(f"Setting ID '{id}' is already used.")

        self.manifest._setting_ids.add(id)
        self.manifest._content["settings"].append(
            {
                "type": "slider",
                "name": f"{CONFIG.NAMESPACE}:{id}",
                "text": text,
                "min": min,
                "max": max,
                "step": step,
                "default": default,
            }
        )
        return self

    def dropdown(self, id: str, text: str, options: list[dict[str, str]], default: str):
        if not isinstance(options, list) or len(options) == 0:
            raise ValueError("Options must be a non-empty list of dictionaries.")

        if default not in [key for option in options for key in option.keys()]:
            raise ValueError(f"Default value '{default}' is not in the options list.")

        if id in self.manifest._setting_ids:
            raise ValueError(f"Setting ID '{id}' is already used.")

        self.manifest._setting_ids.add(id)
        self.manifest._content["settings"].append(
            {
                "type": "dropdown",
                "name": f"{CONFIG.NAMESPACE}:{id}",
                "text": text,
                "options": [{"name": k, "text": v} for option in options for k, v in option.items()],
                "default": default,
            }
        )
        return self


class _Anvil:
    """A class representing an Anvil instance."""

    _instance = None
    _objects_list: list[AddonObject] = []

    def _queue(self, object: AddonObject):
        """Queues an object to be compiled."""
        self._objects_list.append(object)

    def __init__(self):
        """Initializes an Anvil instance.

        Parameters:
            config (_Config): The config of the Anvil instance.
        """
        if _Anvil._instance is None:
            _Anvil._instance = self
        else:
            raise Exception("Anvil instance already exists.")

        self._compiled = False
        self.config = CONFIG
        validate_namespace_project_name(CONFIG.NAMESPACE, CONFIG.PROJECT_NAME)

    def translate(self, languages: Optional[list[str]] = None) -> None:
        """Translates the project."""
        translate(languages)

    def compile(self, extract_world: str = None) -> None:
        """Compiles the project."""
        compile_objects(self, extract_world)

    def package_zip(
        self,
        apply_overlay: bool = False,
        generate_technical_notes: bool = False,
    ) -> None:
        """Packages the project into a zip file for Marketplace.

        Parameters:
            apply_overlay (bool, optional): Whether to apply the overlay to the marketing art. Defaults to False.
            generate_technical_notes (bool, optional): Whether to generate technical notes PDF. Defaults to False.
        """
        if not self._compiled:
            raise RuntimeError("Project must be compiled before packaging.")

        package_zip_core(self.config, apply_overlay, generate_technical_notes)

    def mcaddon(self):
        """Packages the project into a .mcaddon file."""
        if not self._compiled:
            raise RuntimeError("Project must be compiled before packaging.")

        mcaddon_core(self.config)

    def mcworld(self):
        """Packages the project into a .mcworld file."""
        if not self._compiled:
            raise RuntimeError("Project must be compiled before packaging.")

        mcworld_core(self.config)


ANVIL = _Anvil()
