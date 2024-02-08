"""Provides the core functionality of the Anvil library."""
import os
from atexit import register
from datetime import datetime

import commentjson
from bs4 import Stylesheet
from halo import Halo
from PIL import Image

from anvil.api.types import Identifier
from anvil.lib.config import _AnvilConfig
from anvil.lib.lib import (CopyFiles, CreateDirectory, File, FileExists,
                           RemoveDirectory, RemoveFile, process_subcommand,
                           validate_namespace_project_name, zipit)
from anvil.lib.materials import MaterialsObject
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject, JsonSchemes
from anvil.lib.sounds import (EntitySoundEvent, MusicCategory, MusicDefinition,
                              SoundCategory, SoundDefinition, SoundEvent)
from anvil.lib.textures import (BlocksJSONObject, ItemTexturesObject,
                                TerrainTexturesObject)

from ..__version__ import __version__


class _AnvilDefinitions:
    _materials_object: MaterialsObject = None
    _sound_definition_object: SoundDefinition = None
    _music_definition_object: MusicDefinition = None
    _sound_event_object: SoundEvent = None
    _item_textures_object: ItemTexturesObject = None
    _terrain_texture_object: TerrainTexturesObject = None

    _scores: dict[str, int] = {}
    _language: dict[str, str] = {}
    _tags: set[str] = ()
    _raw_text: int = 0

    _blocks_object: BlocksJSONObject = None

    def __init__(self, config: _AnvilConfig):
        self.config = config

    def add_material(self, material_name: str, base_material: str = None):
        """Adds a material to the materials.json file.

        Args:
            material_name (str): The name of the material.
            base_material (str, optional): The name of the base material. Defaults to None.

        """
        if self._materials_object is None:
            self._materials_object = MaterialsObject()

        return self._materials_object.add_material(material_name, base_material)

    def register_sound_definition(
        self,
        sound_reference: str,
        category: SoundCategory,
        use_legacy_max_distance: bool = False,
        max_distance: int = 0,
        min_distance: int = 9999,
    ):
        """Adds a sound to the sound definition.

        Args:
            sound_reference (str): The name of the sound definition.
            category (SoundCategory): The category of the sound.
            use_legacy_max_distance (bool, optional): Whether to use legacy max distance. Defaults to False.
            max_distance (int, optional): The max distance of the sound. Defaults to 0.
            min_distance (int, optional): The min distance of the sound. Defaults to 9999.
        """
        if self._sound_definition_object is None:
            self._sound_definition_object = SoundDefinition()
        return self._sound_definition_object.sound_reference(
            sound_reference,
            category,
            use_legacy_max_distance,
            max_distance,
            min_distance,
        )

    def register_sound_event(
        self,
        entity_identifier: Identifier,
        sound_identifier,
        sound_event: EntitySoundEvent,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
    ):
        if self._sound_event_object is None:
            self._sound_event_object = SoundEvent()
        return self._sound_event_object.add_entity_event(entity_identifier, sound_identifier, sound_event, volume, pitch)

    def register_item_textures(self, item_name: str, directory: str, *item_sprites: str):
        if self._item_textures_object is None:
            self._item_textures_object = ItemTexturesObject()
        return self._item_textures_object.add_item(item_name, directory, *item_sprites)

    def register_music(self, music_category: MusicCategory, min_delay: int = 60, max_delay: int = 180):
        """Adds a music to the music definition.

        Args:
            music_category (MusicCategory): The category of the music.
            min_delay (int, optional): The min delay of the music. Defaults to 60.
            max_delay (int, optional): The max delay of the music. Defaults to 180.

        """
        if self._music_definition_object is None:
            self._music_definition_object = MusicDefinition()
        if self._sound_definition_object is None:
            self._sound_definition_object = SoundDefinition()
        self._music_definition_object.music_definition(music_category, min_delay, max_delay)
        return self._sound_definition_object.sound_reference(f"music.{music_category}", SoundCategory.Music)

    def register_scores(self, **score_id_value: dict[str, int]):
        """
        Adds the provided scores to the setup functions as well as setting the global score values.
        Score objective must be 16 characters or less.

        Parameters:
        ---------
        `score_id_value` : `kwargs`
            The score and it's initial value.

        Examples:
        ---------
        >>> ANVIL.score(player_id=0,test=4)
        >>> ANVIL.score(**{'level':5,'type':1})
        """
        for score_id, score_value in score_id_value.items():
            if len(score_id) > 16:
                self.config.Logger.score_error(score_id)

            start = f"{self.config.NAMESPACE}."
            if not score_id.startswith(start) and self.config._TARGET == "addon":
                self.config.Logger.invalid_score_format(start, score_id)

            if not score_id in self._scores.keys():
                self._scores[score_id] = score_value

    def register_lang(self, key: str, value: str):
        """Adds a localized string to en_US. Translatable."""
        if key not in self._language:
            self._language.update({key: value})

    def register_tag(self, *tags: str):
        """Registers tags.

        Args:
            tags (str): The tags to register.
        """
        for tag in tags:

            start = f"{self.config.NAMESPACE}."
            if not tag.startswith(start) and self.config._TARGET == "addon":
                self.config.Logger.invalid_tag_format(start, tag)

            if not tag in self._tags:
                self._tags.add(tags)

    def register_block(self, block_identifier: Identifier, block_data: dict):
        """Registers blocks.

        Args:
            blocks (dict): The blocks to register.
        """
        if self._blocks_object is None:
            self._blocks_object = BlocksJSONObject()

        self._blocks_object.add_block(block_identifier, block_data)

    def register_terrain_texture(self, texture_name: str, texture_path: str, *block_textures):
        """Registers a terrain texture.

        Args:
            texture_name (str): The name of the texture.
            texture_path (str): The path to the texture.
        """
        if self._terrain_texture_object is None:
            self._terrain_texture_object = TerrainTexturesObject()
        self._terrain_texture_object.add_block(texture_name, texture_path, *block_textures)

    @property
    def get_new_score(self):
        id = f"{self.config.NAMESPACE}.{len(self._scores)}"
        self.register_scores(**{id: 0})
        return id

    @property
    def get_new_lang(self):
        id = f"raw_text_{self._raw_text}"
        self._raw_text += 1
        return id

    def _export_manifest(self):
        release_list = [int(i) for i in self.config._RELEASE.split(".")]
        manifest_rp = JsonSchemes.manifest_rp(release_list, self.config._RP_UUID[0], self.config._BP_UUID[0], self.config.COMPANY, self.config._PBR, self.config._TARGET == "addon")
        manifest_bp = JsonSchemes.manifest_bp(release_list, self.config._BP_UUID[0], self.config._RP_UUID[0], self.config.COMPANY, self.config._SCRIPT_API, self.config._SCRIPT_UI)
        manifest_world = JsonSchemes.manifest_world(release_list, self.config._PACK_UUID, self.config.COMPANY, self.config._RANDOM_SEED)
        world_rp_pack = JsonSchemes.world_packs(self.config._RP_UUID, release_list)
        world_bp_pack = JsonSchemes.world_packs(self.config._BP_UUID, release_list)

        File("manifest.json", manifest_rp, self.config.RP_PATH, "w")
        File("manifest.json", manifest_bp, self.config.BP_PATH, "w")
        File("manifest.json", manifest_world, "", "w")

        File("world_resource_packs.json", world_rp_pack, "", "w")
        File("world_behavior_packs.json", world_bp_pack, "", "w")

    def _export_language(self):
        default_langs = JsonSchemes.pack_name_lang(self.config.DISPLAY_NAME, self.config.PROJECT_DESCRIPTION)
        langs = default_langs.copy()
        langs.extend([f"{k}={v}" for k, v in self._language.items()])
        langs.sort(reverse=True)

        File("languages.json", JsonSchemes.languages(), os.path.join(self.config.BP_PATH, "texts"), "w")
        File("languages.json", JsonSchemes.languages(), os.path.join(self.config.RP_PATH, "texts"), "w")
        File("languages.json", JsonSchemes.languages(), "texts", "w")

        File("en_US.lang", "\n".join(langs), os.path.join(self.config.RP_PATH, "texts"), "w")
        File("en_US.lang", "\n".join(default_langs), os.path.join(self.config.BP_PATH, "texts"), "w")
        File("en_US.lang", "\n".join(default_langs), "texts", "w")

    def _export_scripts(self):
        File(
            "package.json",
            JsonSchemes.packagejson(
                self.config.PROJECT_NAME, self.config._RELEASE, self.config.PROJECT_DESCRIPTION, self.config.COMPANY
            ),
            "",
            "w",
            True,
        )

    def _export_helper_functions(self):
        from anvil.api.commands import (Scoreboard, ScriptEvent, Tag, Target,
                                        Tellraw)
        from anvil.api.features import Function, _Tick

        self._setup_function = Function("setup")
        for f in Function._setup:
            self._setup_function.add(f.execute)
        self._setup_function.queue()

        _Tick().add_function(*Function._ticking).queue

        self._setup_scores = Function("setup_scores")
        self._remove_scores = Function("remove_scores")
        self._remove_tags = Function("remove_tags")

        Function("version").add(
            Tellraw(Target.A).text.text("[Anvil Debug Message]"),
            Tellraw(Target.A).text.text("This message contains information about the creating of this pack."),
            Tellraw(Target.A).text.text(f"Last compiled on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"),
            Tellraw(Target.A).text.text(f"Minecraft Version: {self.config._VANILLA_VERSION}"),
            Tellraw(Target.A).text.text(f"Pack Version: {self.config._RELEASE}"),
        ).queue()

        for score, value in self._scores.items():
            self._setup_scores.add(
                Scoreboard().objective.add(score, score.title()),
                Scoreboard().players.set(self.config.PROJECT_NAME, score, value),
            )
            self._remove_scores.add(Scoreboard().objective.remove(score))

        for tag in self._tags:
            self._remove_tags.add(Tag(Target.E).remove(tag))

        self._setup_scores.queue()
        self._remove_scores.queue()
        self._remove_tags.queue()

        self._setup_function.add(
            self._remove_tags.execute,
            self._remove_scores.execute,
            self._setup_scores.execute,
            ScriptEvent(f"{self.config.NAMESPACE}:setup"),
        )
        self._setup_function.queue()

    @property
    def queue(self):
        if not self._materials_object == None:
            self._materials_object.queue
        if not self._sound_definition_object == None:
            self._sound_definition_object.queue
        if not self._music_definition_object == None:
            self._music_definition_object.queue
        if not self._sound_event_object == None:
            self._sound_event_object.queue
        if not self._item_textures_object == None:
            self._item_textures_object.queue
        if not self._terrain_texture_object == None:
            self._terrain_texture_object.queue
        if not self._blocks_object == None:
            self._blocks_object.queue

        self._export_manifest()
        self._export_language()
        self._export_helper_functions()
        
        if any([self.config._SCRIPT_API, self.config._SCRIPT_UI]):
            self._export_scripts()


class _AnvilCore:
    """A class representing an Anvil instance."""

    _instance = None
    _objects_list: list[AddonObject] = []
    _definitions: _AnvilDefinitions
    _config: _AnvilConfig

    def __init__(self, config: _AnvilConfig):
        """Initializes an Anvil instance.

        Args:
            config (_Config): The config of the Anvil instance.
            logger (Logger): The logger of the Anvil instance.
        """
        if _Anvil._instance is None:
            _Anvil._instance = self
        else:
            raise Exception("Anvil instance already exists.")

        super().__init__()
        self._compiled = False
        self._config = config
        validate_namespace_project_name(config.NAMESPACE, config.PROJECT_NAME)
        self._definitions = _AnvilDefinitions(config)

    @property
    def definitions(self):
        return self._definitions

    @property
    def config(self):
        return self._config

    def require_config(self, *options):
        """Checks if the config has the required options.

        Args:
            options (str): The options to check.
        """
        if not self.config.Config.has_section(self.config.PROJECT_NAME):
            self.config.Logger.project_missing_config()
            self.config.Logger.config_option_changeable(*options)
            self.config.Config.add_section(self.config.PROJECT_NAME)

        for option in options:
            if not self.config.Config.has_option(self.config.PROJECT_NAME, option):
                self.config.Config.add_option(self.config.PROJECT_NAME, str(option), input(f"Enter {option}: "))
                self.config.Logger.config_added_option(self.config.PROJECT_NAME, option)

    @Halo(text="Translating", spinner="dots")
    def translate(self) -> None:
        """
        Translates en_US to all supported Minecraft languages.
        This is a time consuming function, it will be executed with anvil.package(), so it's better to avoid it unless you really want to use it.


        Usage:
        ---------
        >>> ANVIL.translate
        """
        from deep_translator import GoogleTranslator

        def _to_lang(translator: GoogleTranslator, langs: dict):
            lang = JsonSchemes.pack_name_lang(self.config.PROJECT_NAME, self.config.PROJECT_NAME)
            translated = translator.translate_batch(langs.values())
            for k, v in zip(langs.keys(), translated):
                lang.append(f"{k}={v}")
            return lang

        for language in JsonSchemes.languages():
            destination_language = (
                language.replace("zh_CN", "zh-CN").replace("zh_TW", "zh-TW").replace("nb_NO", "no").split("_")[0]
            )
            if not FileExists(
                os.path.join(
                    self.config.RP_PATH,
                    "texts",
                    f"{language}.lang",
                )
            ):
                self._langs = dict(sorted(self.definitions._language.items()))
                Translator = GoogleTranslator(target=destination_language)
                File(
                    f"{language}.lang",
                    "\n".join(_to_lang(Translator, self._langs)),
                    os.path.join(self.config.RP_PATH, "texts"),
                    "w",
                )
                File(
                    f"{language}.lang",
                    "\n".join(JsonSchemes.pack_name_lang(self.config.DISPLAY_NAME, self.config.PROJECT_DESCRIPTION)),
                    os.path.join(self.config.BP_PATH, "texts"),
                    "w",
                )
                File(
                    f"{language}.lang",
                    "\n".join(JsonSchemes.pack_name_lang(self.config.DISPLAY_NAME, self.config.PROJECT_DESCRIPTION)),
                    os.path.join("texts"),
                    "w",
                )

    @Halo(text="Compiling", spinner="dots")
    def compile(self) -> None:
        """Compiles the project."""

        self._definitions.queue

        for object in self._objects_list:
            object._export()
            
        from anvil.api.actors import _ActorClientDescription
        _ActorClientDescription._export()

        from anvil.api.blocks import _PermutationComponents
        if _PermutationComponents._count > 10000:
            if self.config._TARGET == "addon":
                self.config.Logger.too_many_permutations(_PermutationComponents._count)
            else:
                self.config.Logger.too_many_permutations_warn(_PermutationComponents._count)

        if self.config._SCRIPT_API:
            source = os.path.join("assets", "javascript")
            target = os.path.join(self.config.BP_PATH, "scripts")

            do_ts = False
            for subdir, dirname, files in os.walk(source):
                for file in files:
                    input_file_path = os.path.join(subdir, file)
                    relative_subdir = os.path.relpath(subdir, source)
                    new_output_dir = os.path.join(target, relative_subdir)
                    if file.endswith(".js"):
                        CopyFiles(subdir, new_output_dir, file)
                    elif file.endswith(".ts"):
                        do_ts = True

            if do_ts:
                tsconfig = {}
                if FileExists("tsconfig.json"):
                    with open("tsconfig.json", "r") as file:
                        tsconfig = commentjson.load(file)
                        tsconfig["compilerOptions"]["outDir"] = target
                        tsconfig["include"] = ["assets/javascript/**/*"]
                else:
                    tsconfig = JsonSchemes.tsconfig(self.config._PASCAL_PROJECT_NAME)

                File("tsconfig.json", tsconfig, "", "w", False)
                process_subcommand("tsc", "Typescript compilation error")

        self._compiled = True

    def _queue(self, object: AddonObject):
        """Queues an object to be compiled."""
        self._objects_list.append(object)


class _Anvil(_AnvilCore):
    def __init__(self, config: _AnvilConfig):
        super().__init__(config)

    def _process_art(self, apply_overlay: bool = False):
        pack_icon_size = (256, 256)
        store_screenshot_size = (800, 450)
        marketing_screenshot_size = (1920, 1080)

        source = os.path.join("assets", "marketing")
        output_store = os.path.join("assets", "output", "Store Art")
        output_marketing = os.path.join("assets", "output", "Marketing Art")

        CreateDirectory(output_store)
        CreateDirectory(output_marketing)

        def resize(image: Image.Image, name: str, output: str, size, quality=95, dpi=72, overlay: Image.Image = None):
            resized = image.resize(size)

            if overlay:
                overlay = overlay.resize(size)
                resized.paste(overlay, mask=overlay.split()[3])

            resized.convert("RGB").save(
                os.path.join(output, name),
                dpi=(dpi, dpi),
                quality=quality,
            )

        if FileExists(os.path.join(source, "pack_icon.png")):
            original = Image.open(os.path.join(source, "pack_icon.png"))
            resize(original, "pack_icon.png", self.config.BP_PATH, pack_icon_size)
            resize(original, "pack_icon.png", self.config.RP_PATH, pack_icon_size)
            resize(original, f"{self.config.PROJECT_NAME}_packicon_0.jpg", output_store, pack_icon_size)
        else:
            self.config.Logger.file_exist_warning("pack_icon.png")

        if FileExists(os.path.join(source, "keyart.png")):
            original = Image.open(os.path.join(source, "keyart.png")).convert("RGB")
            overlay = None

            if apply_overlay:
                overlay = Image.open(os.path.join(source, "keyart_overlay.png"))

            resize(original, "world_icon.jpeg", "", store_screenshot_size, 95, 72, overlay)
            resize(original, f"{self.config.PROJECT_NAME}_Thumbnail_0.jpg", output_store, store_screenshot_size, 95, 72, overlay)
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
            self.config.Logger.file_exist_warning("keyart.png")

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
            self.config.Logger.file_exist_warning("panorama.png")

        for i in range(5):
            if not FileExists(os.path.join(source, f"{i}.png")):
                if i < 5:
                    self.config.Logger.file_exist_warning(f"{i}.png")
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
                    overlay,
                )
                resize(
                    original,
                    f"{self.config.PROJECT_NAME}_MarketingScreenshot_{i}.jpg",
                    output_marketing,
                    marketing_screenshot_size,
                    100,
                    300,
                    overlay,
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
                overlay,
            )

        else:
            self.config.Logger.file_exist_warning("partner_art.png")

    def package_zip(
        self,
        skip_translation: bool = False,
        apply_overlay: bool = False,
    ) -> None:
        if not self._compiled:
            self.config.Logger.not_compiled()
        self.config.Logger.packaging_zip()

        content_structure = {}

        if not skip_translation:
            self.translate()

        self._process_art(apply_overlay)

        content_structure.update(
            {
                os.path.join("assets", "output", "Store Art"): os.path.join("Store Art"),
                os.path.join("assets", "output", "Marketing Art"): os.path.join("Marketing Art"),
                "resource_packs": os.path.join("Content", "world_template", "resource_packs"),
                "behavior_packs": os.path.join("Content", "world_template", "behavior_packs"),
                "texts": os.path.join("Content", "world_template", "texts"),
                "level.dat": os.path.join("Content", "world_template"),
                "levelname.txt": os.path.join("Content", "world_template"),
                "manifest.json": os.path.join("Content", "world_template"),
                "world_icon.jpeg": os.path.join("Content", "world_template"),
                "world_behavior_packs.json": os.path.join("Content", "world_template"),
                "world_resource_packs.json": os.path.join("Content", "world_template"),
            }
        )

        if not self.config._RANDOM_SEED:
            content_structure.update(
                {
                    "db": os.path.join("Content", "world_template", "db"),
                }
            )

        if self.config._TARGET == "addon":
            if len(self.config._RP_UUID) > 1:
                self.config.Logger.multiple_rp_uuids()
            if len(self.config._BP_UUID) > 1:
                self.config.Logger.multiple_bp_uuids()

        zipit(
            os.path.join("assets", "output", f"{self.config.PROJECT_NAME}.zip"),
            content_structure,
        )

        RemoveDirectory(os.path.join("assets", "output", "Store Art"))
        RemoveDirectory(os.path.join("assets", "output", "Marketing Art"))

    def mcaddon(self):
        """Packages the project into a .mcaddon file."""
        if not self._compiled:
            self.config.Logger.not_compiled()
        self.config.Logger.packaging_mcaddon()

        source = os.path.join("assets", "marketing")
        output = os.path.join("assets", "output")
        if FileExists(os.path.join(source, "pack_icon.png")):
            CopyFiles(
                source,
                os.path.join("behavior_packs", f"BP_{self.config._PASCAL_PROJECT_NAME}"),
                "pack_icon.png",
            )
            CopyFiles(
                source,
                os.path.join("resource_packs", f"RP_{self.config._PASCAL_PROJECT_NAME}"),
                "pack_icon.png",
            )

        resource_packs_structure = {
            os.path.join("resource_packs", f"RP_{self.config._PASCAL_PROJECT_NAME}"): "",
        }
        behavior_packs_structure = {
            os.path.join("behavior_packs", f"BP_{self.config._PASCAL_PROJECT_NAME}"): "",
        }
        content_structure = {
            os.path.join(output, f"{self.config.PROJECT_NAME}_RP.mcpack"): "",
            os.path.join(output, f"{self.config.PROJECT_NAME}_BP.mcpack"): "",
        }

        zipit(
            os.path.join(output, f"{self.config.PROJECT_NAME}_RP.mcpack"),
            resource_packs_structure,
        )
        zipit(
            os.path.join(output, f"{self.config.PROJECT_NAME}_BP.mcpack"),
            behavior_packs_structure,
        )
        zipit(os.path.join(output, f"{self.config.PROJECT_NAME}.mcaddon"), content_structure)
        RemoveFile(os.path.join(output, f"{self.config.PROJECT_NAME}_RP.mcpack"))
        RemoveFile(os.path.join(output, f"{self.config.PROJECT_NAME}_BP.mcpack"))

    def mcworld(self):
        """Packages the project into a .mcworld file."""
        if not self._compiled:
            self.config.Logger.not_compiled()
        self.config.Logger.packaging_mcworld()

        content_structure = {
            "resource_packs": os.path.join("resource_packs"),
            "behavior_packs": os.path.join("behavior_packs"),
            "texts": os.path.join("texts"),
            "db": os.path.join("db"),
            "level.dat": os.path.join(""),
            "levelname.txt": os.path.join(""),
            "manifest.json": os.path.join(""),
            "world_icon.jpeg": os.path.join(""),
            "world_behavior_packs.json": os.path.join(""),
            "world_resource_packs.json": os.path.join(""),
        }

        zipit(
            os.path.join("assets", "output", f"{self.config.PROJECT_NAME}.mcworld"),
            content_structure,
        )

    def generate_technical_notes(self):
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer,
                                        Table, TableStyle)

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

            table = Table(converted_data, hAlign="LEFT", colWidths=doc.width / len(converted_data[0]))

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
            os.path.join("assets", "output", "technical_notes.pdf"),
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
            Paragraph("The following technical notes have been entirely generated from source code using Anvil.", body_style),
            Paragraph("Features overwriting vanilla defaults will be highlighted in green.", bullet_style, "*"),
            Spacer(1, 1 * cm),
            *add_table("Entities:", self.config.Report.dict[ReportType.ENTITY]),
            *add_table("Attachables:", self.config.Report.dict[ReportType.ATTACHABLE]),
            *add_table("Items:", self.config.Report.dict[ReportType.ITEM]),
            *add_table("Blocks:", self.config.Report.dict[ReportType.BLOCK]),
            *add_table("Particles:", self.config.Report.dict[ReportType.PARTICLE]),
            *add_table("Sounds:", self.config.Report.dict[ReportType.SOUND]),
        ]

        doc.build(elements)
