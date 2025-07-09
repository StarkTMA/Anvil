import os
import zipfile
from datetime import datetime

import commentjson
from halo import Halo
from PIL import Image

from anvil.api.actors.materials import _MaterialsObject
from anvil.api.logic.molang import Molang
from anvil.lib.blockbench import _Blockbench
from anvil.lib.config import _AnvilConfig, ConfigPackageTarget
from anvil.lib.lib import (CopyFiles, CreateDirectory, File, FileExists,
                           RemoveDirectory, process_subcommand,
                           validate_namespace_project_name, zipit)
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject, JsonSchemes
from anvil.lib.sounds import (EntitySoundEvent, MusicCategory, MusicDefinition,
                              SoundCategory, SoundDefinition, SoundEvent)
from anvil.lib.textures import (BlocksJSONObject, ItemTexturesObject,
                                TerrainTexturesObject)
from anvil.lib.types import Identifier

from ..__version__ import __version__


class _AnvilSkinPack(AddonObject):
    _extension = ".json"
    _path = os.path.join("assets", "skins")

    def __init__(self, config) -> None:
        """Initializes a SkinPack instance."""
        super().__init__("skins")
        self._config = config
        self._languages = []
        self._skins = []
        self.content(JsonSchemes.skins_json(self._config.PROJECT_NAME))

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
            raise FileNotFoundError(f"{filename}.png not found in {self._path}. Please ensure the file exists.")
        self._skins.append(JsonSchemes.skin_json(filename, is_slim, free))
        self._languages[f"skin.{self._config.PROJECT_NAME}.{filename}"] = display_name

    def _export(self):
        """Exports the SkinPack to the file system."""
        self._content["skins"] = self._skins
        l = JsonSchemes.skin_pack_name_lang(self._config.PROJECT_NAME, self._config.PROJECT_NAME + " Skin Pack")
        l.extend([f"{k}={v}" for k, v in self._languages.items()])

        File("languages.json", JsonSchemes.languages(), self._path, "w")
        File("manifest.json", JsonSchemes.manifest_skins(self._config._RELEASE), self._path, "w")
        File("en_US.lang", "\n".join(l), os.path.join(self._path, "texts"), "w")

        super()._export()


class _AnvilDefinitions:
    _materials_object: _MaterialsObject = None
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
        self._materials_object = _MaterialsObject()

    def register_sound_definition(
        self,
        sound_reference: str,
        category: SoundCategory,
        use_legacy_max_distance: bool = False,
        max_distance: int = 0,
        min_distance: int = 9999,
    ):
        """Adds a sound to the sound definition.

        Parameters:
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

    def register_entity_sound_event(
        self,
        entity_identifier: Identifier,
        sound_reference,
        sound_event: EntitySoundEvent,
        category: SoundCategory = SoundCategory.Neutral,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
        variant_query: Molang = None,
        variant_map: str = None,
        max_distance: int = 0,
        min_distance: int = 9999,
    ):
        if self._sound_event_object is None:
            self._sound_event_object = SoundEvent()
        if self._sound_definition_object is None:
            self._sound_definition_object = SoundDefinition()

        self._sound_event_object.add_entity_event(
            entity_identifier, sound_reference, sound_event, volume, pitch, variant_query, variant_map
        )
        return self._sound_definition_object.sound_reference(
            sound_reference, category, max_distance=max_distance, min_distance=min_distance
        )

    def register_individual_named_sounds(
        self,
        sound_reference,
        category: SoundCategory = SoundCategory.Ambient,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
    ):
        if self._sound_event_object is None:
            self._sound_event_object = SoundEvent()

        self._sound_event_object.add_individual_event(sound_reference, volume, pitch)
        return self._sound_definition_object.sound_reference(sound_reference, category)

    def register_block_sound_event(self):
        """# TO IMPLEMENT
        Registers a block sound event."""
        pass

    def register_item_textures(self, item_name: str, directory: str, *item_sprites: str):
        if self._item_textures_object is None:
            self._item_textures_object = ItemTexturesObject()
        return self._item_textures_object.add_item(item_name, directory, *item_sprites)

    def register_music(self, music_reference: MusicCategory | str, min_delay: int = 60, max_delay: int = 180):
        """Adds a music to the music definition.

        Parameters:
            music_category (MusicCategory): The category of the music.
            min_delay (int, optional): The min delay of the music. Defaults to 60.
            max_delay (int, optional): The max delay of the music. Defaults to 180.

        """
        if self._music_definition_object is None:
            self._music_definition_object = MusicDefinition()
        if self._sound_definition_object is None:
            self._sound_definition_object = SoundDefinition()
        self._music_definition_object.music_definition(music_reference, min_delay, max_delay)
        return self._sound_definition_object.sound_reference(f"music.{music_reference}", SoundCategory.Music)

    def register_scores(self, **score_id_value: dict[str, int]):
        """
        Adds the provided scores to the setup functions as well as setting the global score values.
        Score objective must be 16 characters or less.

        Parameters:
        ---------
        `score_id_value` : `kwParameters`
            The score and it's initial value.

        Examples:
        ---------
        >>> ANVIL.score(player_id=0,test=4)
        >>> ANVIL.score(**{'level':5,'type':1})
        """
        for score_id, score_value in score_id_value.items():
            if len(score_id) > 16:
                raise ValueError(
                    f"Score objective must be 16 characters or less. Error at {score_id}."
                )

            start = f"{self.config.NAMESPACE}."
            if not score_id.startswith(start) and self.config._TARGET == ConfigPackageTarget.ADDON:
                raise ValueError(
                    f"Scores must start with the namespace [{start}]. Error at {score_id}."
                )

            if not score_id in self._scores.keys():
                self._scores[score_id] = score_value

    def register_lang(self, key: str, value: str):
        """Adds a localized string to en_US. Translatable."""
        if key not in self._language:
            self._language.update({key: value})

    def register_tag(self, *tags: str):
        """Registers tags.

        Parameters:
            tags (str): The tags to register.
        """
        for tag in tags:

            start = f"{self.config.NAMESPACE}."
            if not tag.startswith(start) and self.config._TARGET == ConfigPackageTarget.ADDON:
                self.config.Logger.invalid_tag_format(start, tag)
                raise ValueError(
                    f"Tags must start with the namespace [{start}]. Error at {tag}."
                )

            if not tag in self._tags:
                self._tags.add(tags)

    def register_block(self, block_identifier: Identifier, block_data: dict):
        """Registers blocks.

        Parameters:
            blocks (dict): The blocks to register.
        """
        if self._blocks_object is None:
            self._blocks_object = BlocksJSONObject()

        self._blocks_object.add_block(block_identifier, block_data)

    def register_terrain_texture(self, texture_name: str, texture_path: str, *block_textures):
        """Registers a terrain texture.

        Parameters:
            texture_name (str): The name of the texture.
            texture_path (str): The path to the texture.
        """
        if self._terrain_texture_object is None:
            self._terrain_texture_object = TerrainTexturesObject()
        self._terrain_texture_object.add_block(texture_name, texture_path, *block_textures)

    def register_skin_pack(self):
        """Registers a skin pack."""
        if self.config._TARGET == ConfigPackageTarget.ADDON:
            raise ValueError("Skin packs are only supported for world templates.")
        
        else:
            return _AnvilSkinPack()

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

    def _export_manifest(self, extract_world: bool = False):
        release_list = [int(i) for i in self.config._RELEASE.split(".")]

        File("manifest.json", JsonSchemes.manifest_rp(version=release_list), self.config.RP_PATH, "w")
        File("manifest.json", JsonSchemes.manifest_bp(version=release_list), self.config.BP_PATH, "w")
        if extract_world:
            File("manifest.json", JsonSchemes.manifest_world(version=release_list), self.config._WORLD_PATH, "w")

            File(
                "world_resource_packs.json",
                JsonSchemes.world_packs(release_list, self.config._RP_UUID),
                self.config._WORLD_PATH,
                "w",
            )
            File(
                "world_behavior_packs.json",
                JsonSchemes.world_packs(release_list, self.config._BP_UUID),
                self.config._WORLD_PATH,
                "w",
            )

    def _export_language(self):
        default_langs = JsonSchemes.pack_name_lang(self.config.DISPLAY_NAME, self.config.RESOURCE_DESCRIPTION)
        langs = default_langs.copy()
        langs.extend([f"{k}={v}" for k, v in self._language.items()])
        langs.sort(reverse=True)

        File("languages.json", ["en_US"], os.path.join(self.config.BP_PATH, "texts"), "w")
        File("languages.json", ["en_US"], os.path.join(self.config.RP_PATH, "texts"), "w")

        File("en_US.lang", "\n".join(langs), os.path.join(self.config.RP_PATH, "texts"), "w")
        File(
            "en_US.lang",
            "\n".join(JsonSchemes.pack_name_lang(self.config.DISPLAY_NAME, self.config.BEHAVIOUR_DESCRIPTION)),
            os.path.join(self.config.BP_PATH, "texts"),
            "w",
        )

        if self.config._TARGET == "world":
            File("languages.json", ["en_US"], os.path.join(self.config._WORLD_PATH, "texts"), "w")
            File(
                "en_US.lang",
                "\n".join(JsonSchemes.pack_name_lang(self.config.DISPLAY_NAME, self.config.PROJECT_DESCRIPTION)),
                os.path.join(self.config._WORLD_PATH, "texts"),
                "w",
            )

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
        from anvil.api.logic.commands import (Scoreboard, ScriptEvent, Tag,
                                              Target, Tellraw)
        from anvil.api.logic.functions import Function, Tick

        self._setup_function = Function("setup")
        for f in Function._setup:
            self._setup_function.add(f.execute)
        self._setup_function.queue()

        Tick().add_function(*Function._ticking).queue

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

    def queue(self, extract_world: bool = False):
        if self._materials_object.size > 0:
            self._materials_object.queue()
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

        self._export_manifest(extract_world)
        self._export_language()
        # self._export_helper_functions()

        if any([self.config._SCRIPT_API, self.config._SCRIPT_UI]):
            self._export_scripts()


class _AnvilCore:
    _instance = None
    _objects_list: list[AddonObject] = []
    _definitions: _AnvilDefinitions
    _config: _AnvilConfig

    def __init__(self, config: _AnvilConfig):
        """Initializes an Anvil instance.

        Parameters:
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

        Parameters:
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
        """

        from deep_translator import GoogleTranslator

        def _to_lang(translator: GoogleTranslator, langs: dict):
            lang = JsonSchemes.pack_name_lang(self.config.DISPLAY_NAME, self.config.PROJECT_DESCRIPTION)
            translated = translator.translate_batch(langs.values())
            for k, v in zip(langs.keys(), translated):
                lang.append(f"{k}={v}")
            return lang

        File("languages.json", JsonSchemes.languages(), os.path.join(self.config.BP_PATH, "texts"), "w")
        File("languages.json", JsonSchemes.languages(), os.path.join(self.config.RP_PATH, "texts"), "w")

        if self.config._TARGET == "world":
            File("languages.json", JsonSchemes.languages(), os.path.join(self.config._WORLD_PATH, "texts"), "w")

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
                    "\n".join(JsonSchemes.pack_name_lang(self.config.DISPLAY_NAME, self.config.BEHAVIOUR_DESCRIPTION)),
                    os.path.join(self.config.BP_PATH, "texts"),
                    "w",
                )
                if self.config._TARGET == "world":
                    File(
                        f"{language}.lang",
                        "\n".join(JsonSchemes.pack_name_lang(self.config.DISPLAY_NAME, self.config.PROJECT_DESCRIPTION)),
                        os.path.join(self.config._WORLD_PATH, "texts"),
                        "w",
                    )

    def compile(self, extract_world: str = None) -> None:
        """Compiles the project."""

        if extract_world != None and type(extract_world) is str:
            RemoveDirectory(self.config._WORLD_PATH)
            with zipfile.ZipFile(os.path.join("assets", "world", f"{extract_world}.mcworld"), "r") as zip_ref:
                zip_ref.extractall(self.config._WORLD_PATH)

        self._definitions.queue(extract_world != None)
        _Blockbench._export()

        for object in self._objects_list:
            try:
                object._export()
            except Exception as e:
                self.config.Logger.object_export_error(object._name, e)

        from anvil.api.blocks.blocks import _PermutationComponents

        if _PermutationComponents._count > 10000:
            if self.config._TARGET == ConfigPackageTarget.ADDON:
                raise RuntimeError(
                    f"Total Block permutations exceeded 10000 ({_PermutationComponents._count}). Addons cannot exceed this limit."
                )
            else:
                raise RuntimeError(
                    f"Total Block permutations exceeded 10000 ({_PermutationComponents._count}). For minimal performance impact, consider reducing the number of permutations."
                )

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
    """A class representing an Anvil instance."""

    def __init__(self, config: _AnvilConfig):
        super().__init__(config)

    def _process_art(self, apply_overlay: bool = False, zip: bool = True):
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

        pack_icon_size = (256, 256)
        store_screenshot_size = (800, 450)
        marketing_screenshot_size = (1920, 1080)

        source = os.path.join("assets", "marketing")
        output_store = os.path.join("assets", "output", "Store Art")
        output_marketing = os.path.join("assets", "output", "Marketing Art")

        if FileExists(os.path.join(source, "pack_icon.png")):
            original = Image.open(os.path.join(source, "pack_icon.png"))
            resize(original, "pack_icon.png", self.config.BP_PATH, pack_icon_size)
            resize(original, "pack_icon.png", self.config.RP_PATH, pack_icon_size)

        else:
            self.config.Logger.file_exist_warning("pack_icon.png")

        if zip:
            CreateDirectory(output_store)
            CreateDirectory(output_marketing)

            if FileExists(os.path.join(source, "keyart.png")):
                original = Image.open(os.path.join(source, "keyart.png")).convert("RGB")
                overlay = None

                if apply_overlay:
                    overlay = Image.open(os.path.join(source, "keyart_overlay.png"))

                resize(original, "world_icon.jpeg", self.config._WORLD_PATH, store_screenshot_size, 95, 72, overlay)
                resize(
                    original, f"{self.config.PROJECT_NAME}_Thumbnail_0.jpg", output_store, store_screenshot_size, 95, 72, overlay
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
                self.config.Logger.file_exist_info("panorama.png")

            for i in range(999):
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
                self.config.Logger.file_exist_warning("partner_art.png")

            if FileExists(os.path.join(source, "pack_icon.png")):
                original = Image.open(os.path.join(source, "pack_icon.png"))
                resize(original, f"{self.config.PROJECT_NAME}_packicon_0.jpg", output_store, pack_icon_size)
            else:
                self.config.Logger.file_exist_warning("pack_icon.png")

    def package_zip(
        self,
        skip_translation: bool = False,
        apply_overlay: bool = False,
    ) -> None:
        """Packages the project into a zip file for Marketplace."""
        if not self._compiled:
            raise RuntimeError("Project must be compiled before packaging.")
        self.config.Logger.packaging_zip()

        if not skip_translation:
            self.translate()

        self._process_art(apply_overlay)

        content_structure = {
            os.path.join("assets", "output", "Store Art"): os.path.join("Store Art"),
            os.path.join("assets", "output", "Marketing Art"): os.path.join("Marketing Art"),
        }

        if self.config._TARGET == ConfigPackageTarget.ADDON:
            if len(self.config._RP_UUID) > 1:
                raise RuntimeError(
                    "Multiple resource pack UUIDs found. Please ensure only one UUID is set for the resource pack."
                )
            if len(self.config._BP_UUID) > 1:
                raise RuntimeError(
                    "Multiple behavior pack UUIDs found. Please ensure only one UUID is set for the behavior pack."
                )

            content_structure.update(
                {
                    self.config.RP_PATH: os.path.join("Content", "resource_packs", f"RP_{self.config._PASCAL_PROJECT_NAME}"),
                    self.config.BP_PATH: os.path.join("Content", "behavior_packs", f"BP_{self.config._PASCAL_PROJECT_NAME}"),
                }
            )

        else:
            content_structure.update(
                {
                    self.config.RP_PATH: os.path.join(
                        "Content", "world_template", "resource_packs", f"RP_{self.config._PASCAL_PROJECT_NAME}"
                    ),
                    self.config.BP_PATH: os.path.join(
                        "Content", "world_template", "behavior_packs", f"BP_{self.config._PASCAL_PROJECT_NAME}"
                    ),
                    os.path.join(self.config._WORLD_PATH, "texts"): os.path.join("Content", "world_template", "texts"),
                    os.path.join(self.config._WORLD_PATH, "level.dat"): os.path.join("Content", "world_template"),
                    os.path.join(self.config._WORLD_PATH, "levelname.txt"): os.path.join("Content", "world_template"),
                    os.path.join(self.config._WORLD_PATH, "manifest.json"): os.path.join("Content", "world_template"),
                    os.path.join(self.config._WORLD_PATH, "world_icon.jpeg"): os.path.join("Content", "world_template"),
                    os.path.join(self.config._WORLD_PATH, "world_behavior_packs.json"): os.path.join("Content", "world_template"),
                    os.path.join(self.config._WORLD_PATH, "world_resource_packs.json"): os.path.join("Content", "world_template"),
                }
            )
            if not self.config._RANDOM_SEED:
                content_structure.update(
                    {
                        os.path.join(self.config._WORLD_PATH, "db"): os.path.join("Content", "world_template", "db"),
                    }
                )

        zipit(
            os.path.join("assets", "output", f"{self.config.PROJECT_NAME}.zip"),
            content_structure,
        )

        RemoveDirectory(os.path.join("assets", "output", "Store Art"))
        RemoveDirectory(os.path.join("assets", "output", "Marketing Art"))

    def mcaddon(self):
        """Packages the project into a .mcaddon file."""
        if not self._compiled:
            raise RuntimeError("Project must be compiled before packaging.")
        self.config.Logger.packaging_mcaddon()

        self._process_art(False, False)

        content_structure = {
            self.config.RP_PATH: f"RP_{self.config.PROJECT_NAME}",
            self.config.BP_PATH: f"BP_{self.config.PROJECT_NAME}",
        }

        zipit(os.path.join("assets", "output", f"{self.config.PROJECT_NAME}.mcaddon"), content_structure)

    def mcworld(self):
        """Packages the project into a .mcworld file."""
        if not self._compiled:
            raise RuntimeError("Project must be compiled before packaging.")
        self.config.Logger.packaging_mcworld()

        self._process_art(False, False)

        content_structure = {
            self.config.RP_PATH: os.path.join("resource_packs", f"RP_{self.config.PROJECT_NAME}"),
            self.config.BP_PATH: os.path.join("behavior_packs", f"BP_{self.config.PROJECT_NAME}"),
            os.path.join(self.config._WORLD_PATH, "texts"): "texts",
            os.path.join(self.config._WORLD_PATH, "level.dat"): "",
            os.path.join(self.config._WORLD_PATH, "levelname.txt"): "",
            os.path.join(self.config._WORLD_PATH, "manifest.json"): "",
            os.path.join(self.config._WORLD_PATH, "world_icon.jpeg"): "",
            os.path.join(self.config._WORLD_PATH, "world_behavior_packs.json"): "",
            os.path.join(self.config._WORLD_PATH, "world_resource_packs.json"): "",
        }

        zipit(
            os.path.join("assets", "output", f"{self.config.PROJECT_NAME}.mcworld"),
            content_structure,
        )

    def generate_technical_notes(self):
        """Generates a technical notes PDF that contains information about included entities, blocks, items, sounds and more."""
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
