import os
import zipfile
from typing import Optional

import click
from halo import Halo
from PIL import Image

from anvil.api.actors.materials import MaterialsObject
from anvil.api.core.sounds import (
    BlocksJSONObject,
    MusicDefinition,
    SoundDefinition,
    SoundEvent,
)
from anvil.api.core.textures import (
    FlipBookTexturesObject,
    ItemTexturesObject,
    TerrainTexturesObject,
)
from anvil.lib.blockbench import _Blockbench
from anvil.lib.config import CONFIG, ConfigPackageTarget
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


def extract_world_pack(extract_world: str | None = None):
    if extract_world != None and type(extract_world) is str:
        RemoveDirectory(CONFIG._WORLD_PATH)
        with zipfile.ZipFile(
            os.path.join("world", f"{extract_world}.mcworld"), "r"
        ) as zip_ref:
            zip_ref.extractall(CONFIG._WORLD_PATH)


def manifests(extract_world: str | None = None):
    release_list = [int(i) for i in CONFIG._RELEASE.split(".")]
    if extract_world != None and type(extract_world) is str:
        File(
            "manifest.json",
            JsonSchemes.manifest_world(version=release_list),
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
    File(
        "manifest.json",
        JsonSchemes.manifest_rp(version=CONFIG._RELEASE),
        CONFIG.RP_PATH,
        "w",
    )
    File(
        "manifest.json",
        JsonSchemes.manifest_bp(version=CONFIG._RELEASE),
        CONFIG.BP_PATH,
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


class _AnvilSkinPack(AddonObject):
    _extension = ".json"
    _path = os.path.join("assets", "skins")

    def __init__(self, config) -> None:
        """Initializes a SkinPack instance."""
        super().__init__("skins")
        self._languages = []
        self._skins = []
        self.content(JsonSchemes.skin_pack(CONFIG.PROJECT_NAME))

    def add_skin(
        self,
        filename: str,
        display_name: str,
        is_slim: bool = False,
        free: bool = False,
    ):
        """Adds a skin to the SkinPack.

        Parameters:
            filename (str): The filename of the skin.
            display_name (str): The display name of the skin.
            is_slim (bool, optional): Whether the skin is slim. Defaults to False.
            free (bool, optional): Whether the skin is free. Defaults to False.
        """
        if not FileExists(os.path.join(self._path, f"{filename}.png")):
            raise FileNotFoundError(
                f"{filename}.png not found in {self._path}. Please ensure the file exists."
            )
        self._skins.append(JsonSchemes.skin_json(filename, is_slim, free))
        self._languages[f"skin.{CONFIG.PROJECT_NAME}.{filename}"] = display_name

    def _export(self):
        """Exports the SkinPack to the file system."""
        self._content["skins"] = self._skins
        l = JsonSchemes.skin_pack_name_lang(
            CONFIG.PROJECT_NAME, CONFIG.PROJECT_NAME + " Skin Pack"
        )
        l.extend([f"{k}={v}" for k, v in self._languages.items()])

        File("languages.json", JsonSchemes.languages(), self._path, "w")
        File(
            "manifest.json",
            JsonSchemes.manifest_skins(CONFIG._RELEASE),
            self._path,
            "w",
        )
        File("en_US.lang", "\n".join(l), os.path.join(self._path, "texts"), "w")

        super()._export()


class _Anvil:
    """A class representing an Anvil instance."""

    _instance = None
    _objects_list: list[AddonObject] = []

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
        validate_namespace_project_name(CONFIG.NAMESPACE, CONFIG.PROJECT_NAME)

    @property
    def config(self):
        return CONFIG

    @Halo(text="Translating", spinner="dots")
    def translate(self, languages: Optional[list[str]] = None) -> None:
        """Translates the project."""
        AnvilTranslator().auto_translate_all(languages)

    @Halo(text="Compiling", spinner="dots")
    def compile(self, extract_world: str = None) -> None:
        """Compiles the project."""
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
        self._queue(AnvilTranslator())

        _Blockbench._export()

        for object in self._objects_list:
            try:
                object._export()
            except Exception as e:
                import traceback as tb

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
                click.echo(
                    click.style(f"\rError Message: {str(e)}", fg="red"), err=True
                )
                click.echo(click.style(f"\r{'='*60}", fg="red"), err=True)

        from anvil.api.blocks.blocks import _PermutationComponents

        if _PermutationComponents._count > 10000:
            if self.config._TARGET == ConfigPackageTarget.ADDON:
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

        if self.config._TARGET == ConfigPackageTarget.ADDON:
            if len(self.config._RP_UUID) > 1:
                raise RuntimeError(
                    "Multiple resource pack UUIDs found. Please ensure only one UUID is set for the resource pack."
                )
            if len(self.config._BP_UUID) > 1:
                raise RuntimeError(
                    "Multiple behavior pack UUIDs found. Please ensure only one UUID is set for the behavior pack."
                )

        if self.config._SCRIPT_API:
            process_subcommand(
                self.config._SCRIPT_BUNDLE_SCRIPT, "Building scripts error"
            )

        self._compiled = True

    @Halo(text="Packaging ZIP", spinner="dots")
    def package_zip(
        self,
        apply_overlay: bool = False,
    ) -> None:
        """Packages the project into a zip file for Marketplace.

        Parameters:
            apply_overlay (bool, optional): Whether to apply the overlay to the marketing art. Defaults to False.
        """
        if not self._compiled:
            raise RuntimeError("Project must be compiled before packaging.")

        self._process_art(apply_overlay)

        content_structure = {
            os.path.join("output", "Store Art"): os.path.join("Store Art"),
            os.path.join("output", "Marketing Art"): os.path.join("Marketing Art"),
        }

        if self.config._TARGET == ConfigPackageTarget.ADDON:
            content_structure.update(
                {
                    self.config.RP_PATH: os.path.join(
                        "Content",
                        "resource_packs",
                        f"RP_{self.config._PASCAL_PROJECT_NAME}",
                    ),
                    self.config.BP_PATH: os.path.join(
                        "Content",
                        "behavior_packs",
                        f"BP_{self.config._PASCAL_PROJECT_NAME}",
                    ),
                }
            )

        else:
            content_structure.update(
                {
                    self.config.RP_PATH: os.path.join(
                        "Content",
                        "world_template",
                        "resource_packs",
                        f"RP_{self.config._PASCAL_PROJECT_NAME}",
                    ),
                    self.config.BP_PATH: os.path.join(
                        "Content",
                        "world_template",
                        "behavior_packs",
                        f"BP_{self.config._PASCAL_PROJECT_NAME}",
                    ),
                    os.path.join(self.config._WORLD_PATH, "texts"): os.path.join(
                        "Content", "world_template", "texts"
                    ),
                    os.path.join(self.config._WORLD_PATH, "level.dat"): os.path.join(
                        "Content", "world_template"
                    ),
                    os.path.join(
                        self.config._WORLD_PATH, "levelname.txt"
                    ): os.path.join("Content", "world_template"),
                    os.path.join(
                        self.config._WORLD_PATH, "manifest.json"
                    ): os.path.join("Content", "world_template"),
                    os.path.join(
                        self.config._WORLD_PATH, "world_icon.jpeg"
                    ): os.path.join("Content", "world_template"),
                    os.path.join(
                        self.config._WORLD_PATH, "world_behavior_packs.json"
                    ): os.path.join("Content", "world_template"),
                    os.path.join(
                        self.config._WORLD_PATH, "world_resource_packs.json"
                    ): os.path.join("Content", "world_template"),
                }
            )
            if not self.config._RANDOM_SEED:
                content_structure.update(
                    {
                        os.path.join(self.config._WORLD_PATH, "db"): os.path.join(
                            "Content", "world_template", "db"
                        ),
                    }
                )

        zipit(
            os.path.join("output", f"{self.config.PROJECT_NAME}.zip"),
            content_structure,
        )

        RemoveDirectory(os.path.join("output", "Store Art"))
        RemoveDirectory(os.path.join("output", "Marketing Art"))

    @Halo(text="Packaging mcaddon", spinner="dots")
    def mcaddon(self):
        """Packages the project into a .mcaddon file."""
        if not self._compiled:
            raise RuntimeError("Project must be compiled before packaging.")

        self._process_art(False, False)

        content_structure = {
            self.config.RP_PATH: f"RP_{self.config.PROJECT_NAME}",
            self.config.BP_PATH: f"BP_{self.config.PROJECT_NAME}",
        }

        zipit(
            os.path.join("output", f"{self.config.PROJECT_NAME}.mcaddon"),
            content_structure,
        )

    @Halo(text="Packaging mcworld", spinner="dots")
    def mcworld(self):
        """Packages the project into a .mcworld file."""
        if not self._compiled:
            raise RuntimeError("Project must be compiled before packaging.")

        self._process_art(False, False)

        content_structure = {
            self.config.RP_PATH: os.path.join(
                "resource_packs", f"RP_{self.config.PROJECT_NAME}"
            ),
            self.config.BP_PATH: os.path.join(
                "behavior_packs", f"BP_{self.config.PROJECT_NAME}"
            ),
            os.path.join(self.config._WORLD_PATH, "texts"): "texts",
            os.path.join(self.config._WORLD_PATH, "level.dat"): "",
            os.path.join(self.config._WORLD_PATH, "levelname.txt"): "",
            os.path.join(self.config._WORLD_PATH, "manifest.json"): "",
            os.path.join(self.config._WORLD_PATH, "world_icon.jpeg"): "",
            os.path.join(self.config._WORLD_PATH, "world_behavior_packs.json"): "",
            os.path.join(self.config._WORLD_PATH, "world_resource_packs.json"): "",
        }

        zipit(
            os.path.join("output", f"{self.config.PROJECT_NAME}.mcworld"),
            content_structure,
        )

    @Halo(text="Generating technical notes", spinner="dots")
    def generate_technical_notes(self):
        """Generates a technical notes PDF that contains information about included entities, blocks, items, sounds and more."""
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )

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
                style_commands.append(
                    ("BACKGROUND", (0, row), (-1, row), colors.lightgreen)
                )
            table.setStyle(TableStyle(style_commands))

            return title, Spacer(1, 0.3 * cm), table, Spacer(1, 1 * cm)

        doc = SimpleDocTemplate(
            os.path.join("output", "technical_notes.pdf"),
            pagesize=A4,
            leftMargin=1 * cm,
            rightMargin=1 * cm,
            topMargin=1 * cm,
            bottomMargin=1 * cm,
            title=f"{self.config.DISPLAY_NAME} Technical Notes",
            author=self.config.COMPANY,
            subject=f"{self.config.DISPLAY_NAME} Technical Notes",
            creator=f"Anvil@stark_lg {__version__}",
        )
        styles = getSampleStyleSheet()
        title_style = styles["Heading1"]
        body_style = styles["BodyText"]
        bullet_style = styles["Bullet"]

        elements = [
            Paragraph(f"{self.config.DISPLAY_NAME}:", title_style),
            Paragraph(f"Developed by: {self.config.COMPANY}", body_style),
            Paragraph(f"Generated with StarkTMA/Anvil {__version__}", body_style),
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
            *add_table("Entities:", self.config.Report.dict[ReportType.ENTITY]),
            *add_table("Attachables:", self.config.Report.dict[ReportType.ATTACHABLE]),
            *add_table("Items:", self.config.Report.dict[ReportType.ITEM]),
            *add_table("Blocks:", self.config.Report.dict[ReportType.BLOCK]),
            *add_table("Particles:", self.config.Report.dict[ReportType.PARTICLE]),
            *add_table("Sounds:", self.config.Report.dict[ReportType.SOUND]),
        ]

        doc.build(elements)

    def _queue(self, object: AddonObject):
        """Queues an object to be compiled."""
        self._objects_list.append(object)

    @Halo(text="Processing Art", spinner="dots")
    def _process_art(self, apply_overlay: bool = False, zip: bool = True):
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

        pack_icon_size = (256, 256)
        store_screenshot_size = (800, 450)
        marketing_screenshot_size = (1920, 1080)

        source = os.path.join("marketing")
        output_store = os.path.join("output", "Store Art")
        output_marketing = os.path.join("output", "Marketing Art")

        if FileExists(os.path.join(source, "pack_icon.png")):
            original = Image.open(os.path.join(source, "pack_icon.png"))
            resize(original, "pack_icon.png", self.config.BP_PATH, pack_icon_size)
            resize(original, "pack_icon.png", self.config.RP_PATH, pack_icon_size)

        else:
            raise FileNotFoundError(
                "pack_icon.png not found in marketing directory. Please ensure the file exists."
            )

        if zip:
            CreateDirectory(output_store)
            CreateDirectory(output_marketing)

            if FileExists(os.path.join(source, "keyart.png")):
                original = Image.open(os.path.join(source, "keyart.png")).convert("RGB")
                overlay = None

                if apply_overlay:
                    overlay = Image.open(os.path.join(source, "keyart_overlay.png"))

                resize(
                    original,
                    "world_icon.jpeg",
                    self.config._WORLD_PATH,
                    store_screenshot_size,
                    95,
                    72,
                    overlay,
                )
                resize(
                    original,
                    f"{self.config.PROJECT_NAME}_Thumbnail_0.jpg",
                    output_store,
                    store_screenshot_size,
                    95,
                    72,
                    overlay,
                )
                resize(
                    original,
                    f"{self.config.PROJECT_NAME}_MarketingKeyArt.jpg",
                    output_marketing,
                    marketing_screenshot_size,
                    100,
                    300,
                    overlay,
                )

            else:
                raise FileNotFoundError(
                    "keyart.png not found in marketing directory. Please ensure the file exists."
                )

            if FileExists(os.path.join(source, "panorama.png")):
                original = Image.open(os.path.join(source, "panorama.png"))
                scale_factor = 450 / original.size[1]

                resize(
                    original,
                    f"{self.config.PROJECT_NAME}_panorama_0.jpg",
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
                        raise FileNotFoundError(
                            f"{i}.png not found in marketing directory. Please ensure the file exists."
                        )
                    break
                else:
                    original = Image.open(os.path.join(source, f"{i}.png"))
                    resize(
                        original,
                        f"{self.config.PROJECT_NAME}_screenshot_{i}.jpg",
                        output_store,
                        store_screenshot_size,
                        95,
                        72,
                    )
                    resize(
                        original,
                        f"{self.config.PROJECT_NAME}_MarketingScreenshot_{i}.jpg",
                        output_marketing,
                        marketing_screenshot_size,
                        100,
                        300,
                    )

            if FileExists(os.path.join(source, "partner_art.png")):
                original = Image.open(os.path.join(source, "partner_art.png"))

                resize(
                    original,
                    f"{self.config.PROJECT_NAME}_PartnerArt.jpg",
                    output_marketing,
                    marketing_screenshot_size,
                    100,
                    300,
                )

            else:
                raise FileNotFoundError(
                    "partner_art.png not found in marketing directory. Please ensure the file exists."
                )

            if FileExists(os.path.join(source, "pack_icon.png")):
                original = Image.open(os.path.join(source, "pack_icon.png"))
                resize(
                    original,
                    f"{self.config.PROJECT_NAME}_packicon_0.jpg",
                    output_store,
                    pack_icon_size,
                )
            else:
                raise FileNotFoundError(
                    "pack_icon.png not found in marketing directory. Please ensure the file exists."
                )


ANVIL = _Anvil()
