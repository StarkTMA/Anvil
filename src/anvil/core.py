"""Provides the core functionality of the Anvil library."""
from .lib import *
from .lib import _Config, _JsonSchemes, _Logger


class ReportCollector:
    def __init__(self) -> None:
        """A dictionary where keys are ReportType and values are `list[defaultdict]`.
        These inner `defaultdict` will automatically create a key if it doesn't exist
        and initialize it to a dictionary of empty sets.

        The dictionary is later used to generate a report of what have been added to the pack.
        """
        self.dict = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

    def add_headers(self):
        self.add_report(ReportType.SOUND, col0 = "Sound Identifier", col1 = "Sounds", vanilla=False)
        self.add_report(ReportType.ENTITY, col0 = "Entity Name", col1 = "Entity Identifier", col2="Entity Events", vanilla = False)
        self.add_report(ReportType.ATTACHABLE, col0 = "Attachable Name", col1 = "Attachable Identifier", vanilla = False)
        self.add_report(ReportType.ITEM, col0 = "Item Name", col1 = "Item Identifier", vanilla = False)
        self.add_report(ReportType.BLOCK, col0 = "Block Name", col1 = "Block Identifier", col2 = "Block States", vanilla = False)
        self.add_report(ReportType.PARTICLE, col0 = "Particle Name", col1 = "Particle Identifier", vanilla = False)
        return self

    def add_report(self, report_type: ReportType, col0, **columns):
        for col_name, col_value in columns.items():
            if isinstance(col_value, tuple | set | list):
                self.dict[report_type][col0][col_name].update(col_value)
            else:
                self.dict[report_type][col0][col_name].add(str(col_value))


class AddonObject:
    """
    An object representing an addon with functionality to modify its content, queue it for processing, and export it.

    Attributes:
        _extensions (dict): A mapping of file extension types with the different namespace formats.
        _name (str): The name of the addon object.
        _path (str): The path of the addon object.
        _content (dict): The content of the addon object.
        _directory (str): The directory where the addon object is located.
        _shorten (bool): A flag indicating whether the content should be shortened.
    """

    _extensions = {0: ".json", 1: ".json"}

    def __init__(self, name: str, path: str) -> None:
        """
        Constructs all the necessary attributes for the AddonObject object.

        Args:
            name (str): The name of the addon object.
            path (str): The path of the addon object.
        """
        self._shorten = True

        self._name = name
        self._path = path

        self._content = {}
        self._directory = ""
        _logger.object_initiated(self._name)

    @classmethod
    @property
    def _extension(self):
        """
        Gets the file extension for the addon object based on the namespace format bit.
        """
        return self._extensions[ANVIL.NAMESPACE_FORMAT_BIT]

    @property
    def do_not_shorten(self):
        """
        Setter property that disables shortening of the content when exporting.
        """
        self._shorten = False

    def content(self, content):
        """
        Sets the content of the addon object and returns the object.

        Args:
            content (any): The content to be set for the addon object.

        Returns:
            self: The instance of the current AddonObject.
        """
        self._content = content
        return self

    def queue(self, directory: str = ""):
        """
        Queues the addon object for processing and logs the event.

        Args:
            directory (str, optional): The directory of the addon object. Defaults to ''.

        Returns:
            self: The instance of the current AddonObject.
        """
        self._directory = directory if not directory is None else ""
        self._path = os.path.join(self._path, self._directory)
        ANVIL._queue(self)
        _logger.object_queued(self._name)
        return self

    def _export(self):
        """
        Exports the addon object after potentially shortening its content and replacing backslashes.
        Logs the event and writes the object to a file.
        """

        def _shorten_dict(d):
            if isinstance(d, dict):
                return {
                    k: v
                    for k, v in ((k, _shorten_dict(v)) for k, v in d.items())
                    if v != {} and v != [] or str(k).startswith("minecraft:")
                }

            elif isinstance(d, list):
                return [v for v in map(_shorten_dict, d) if v != []]

            return d

        def _replace_backslashes(obj):
            if isinstance(obj, str):
                return obj.replace("\\", "/").replace('"/n"', '"\\n"')
            elif isinstance(obj, list):
                return [_replace_backslashes(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: _replace_backslashes(value) for key, value in obj.items()}
            else:
                return obj

        path = (
            self._path.removeprefix("resource_packs/")
            .removeprefix("behavior_packs/")
            .removeprefix(f"RP_{ANVIL.PASCAL_PROJECT_NAME}/")
            .removeprefix(f"BP_{ANVIL.PASCAL_PROJECT_NAME}/")
        )
        path = os.path.join(path, self._name + self._extension)
        if len(path) > 80:
            ANVIL.Logger.path_length_error(path)

        if self._shorten and type(self._content) is dict:
            self._content = _shorten_dict(self._content)

        self._content = _replace_backslashes(self._content)
        _logger.object_exported(self._name)
        File(f"{self._name}{self._extension}", self._content, self._path, "w")


class RawTextConstructor:
    """
    A class that constructs raw text with various possible styling and structures.

    Attributes:
        _raw_text (list): The raw text being constructed, stored as a list of dictionaries representing different parts.
    """

    def __init__(self):
        """Initializes a new RawTextConstructor instance."""
        self._raw_text = []

    def style(self, *styles: Style):
        """
        Applies the provided styles to the raw text.

        Args:
            styles (Style): The styles to be applied.

        Returns:
            self: The instance of the current RawTextConstructor.
        """
        self._raw_text.append({"text": "".join(map(lambda a: a.value, styles))})
        return self

    def text(self, text):
        """
        Appends the given text to the raw text.

        Args:
            text (str): The text to be appended.

        Returns:
            self: The instance of the current RawTextConstructor.
        """
        self._raw_text.append({"text": str(text)})
        return self

    def translate(self, text):
        """
        Localizes the given text and appends it to the raw text.

        Args:
            text (str): The text to be localized and appended.

        Returns:
            self: The instance of the current RawTextConstructor.
        """
        self.id = f"raw_text_{ANVIL._tellraw_index}"
        ANVIL.localize(self.id, text)
        ANVIL._tellraw_index += 1
        self._raw_text.append({"translate": self.id, "with": ["\n"]})
        return self

    def score(self, objective, target: Selector | Target | str):
        """
        Appends the score of the given target under the given objective to the raw text.

        Args:
            objective (str): The objective under which the target's score is tracked.
            target (Selector | Target | str): The target whose score is to be appended.

        Returns:
            self: The instance of the current RawTextConstructor.
        """
        t = target.value if isinstance(target, Target) else target

        self._raw_text.append({"score": {"name": t, "objective": objective}})
        return self

    def selector(self, target: Selector | Target | str):
        """
        Appends the selector of the given target to the raw text.

        Args:
            target (Selector | Target | str): The target whose selector is to be appended.

        Returns:
            self: The instance of the current RawTextConstructor.
        """
        t = target.value if isinstance(target, Target) else target

        self._raw_text.append({"selector": t})
        return self

    def __str__(self) -> str:
        """
        Converts the RawTextConstructor instance to a string.

        Returns:
            str: A string representation of the raw text.
        """
        return f'{{"rawtext":{json.dumps(self._raw_text, ensure_ascii=False)}}}'


class _MinecraftDescription:
    """Handles Minecraft descriptions.

    Attributes:
        name (str): The name of the Minecraft object.
        is_vanilla (bool, optional): If the object is from vanilla Minecraft. Defaults to False.
    """

    def _validate_name(self, name: str):
        """Validates the name of the Minecraft object.

        Args:
            name (str): The name of the Minecraft object.
        """
        if ":" in name:
            _logger.namespaces_not_allowed(name)

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Initializes a _MinecraftDescription instance.

        Args:
            name (str): The name of the Minecraft object.
            is_vanilla (bool, optional): If the object is from vanilla Minecraft. Defaults to False.
        """
        self._validate_name(name)
        self._name = name
        self._namespace_format = "minecraft" if is_vanilla else ANVIL.NAMESPACE_FORMAT
        self._description: dict = _JsonSchemes.description(self._namespace_format, self._name)

    @property
    def identifier(self):
        """Formulates the identifier for the Minecraft object.

        Returns:
            str: The identifier in the format 'namespace_format:name'
        """
        return f"{self._namespace_format}:{self._name}"

    @property
    def _export(self):
        """Returns the description of the Minecraft object.

        Returns:
            dict: The description
        """
        return self._description


class _ItemTextures(AddonObject):
    """Handles item textures for the addon."""

    def __init__(self) -> None:
        """Initializes a _ItemTextures instance."""
        super().__init__(
            "item_texture",
            os.path.join("resource_packs", f"RP_{PASCAL_PROJECT_NAME}", "textures"),
        )

        self.content(_JsonSchemes.item_texture(PROJECT_NAME))

    def add_item(self, item_name: str, directory, *item_sprites: str):
        """Adds item textures to the content.

        Args:
            item_name (str): The name of the item.
            directory (str): The directory path for the textures.
            item_sprites (str): The names of the item sprites.
        """
        for item in item_sprites:
            if not FileExists(os.path.join("assets", "textures", "items", f"{item}.png")):
                ANVIL.Logger.file_exist_error(f"{item}.png", os.path.join("assets", "textures", "items"))

        self._content["texture_data"][f"{ANVIL.NAMESPACE}:{item_name}"] = {
            "textures": [*[os.path.join("textures", ANVIL.NAMESPACE, "items", directory, sprite).replace("\\", "/") for sprite in item_sprites]]
        }

    @property
    def queue(self):
        """Queues the item textures.

        Returns:
            object: The parent's queue method result.
        """
        return super().queue("")

    def _export(self):
        """Exports the item textures if at least one item was added.

        Returns:
            object: The parent's export method result.
        """
        if len(self._content["texture_data"]) > 0:
            for items in self._content["texture_data"].values():
                for sprite in items["textures"]:
                    CopyFiles(
                        os.path.join("assets", "textures", "items"),
                        os.path.join(
                            "resource_packs",
                            f"RP_{ANVIL.PASCAL_PROJECT_NAME}",
                            sprite.rstrip(sprite.split("/")[-1]),
                        ),
                        sprite.split("/")[-1] + ".png",
                    )
            return super()._export()


class _TerrainTextures(AddonObject):
    """Handles terrain textures for the addon."""

    def __init__(self) -> None:
        """Initializes a _TerrainTextures instance."""
        super().__init__(
            "terrain_texture",
            os.path.join("resource_packs", f"RP_{PASCAL_PROJECT_NAME}", "textures"),
        )
        self.content(_JsonSchemes.terrain_texture(PROJECT_NAME))

    def add_block(self, block_name: str, directory: str, *block_textures: str):
        """Adds block textures to the content.

        Args:
            block_name (str): The name of the block.
            directory (str): The directory path for the textures.
            block_textures (str): The names of the block textures.
        """
        self._content["texture_data"][f"{ANVIL.NAMESPACE}:{block_name}"] = {
            "textures": [*[os.path.join("textures", ANVIL.NAMESPACE, "blocks", directory, face).replace("\\", "/") for face in block_textures]]
        }

    @property
    def queue(self):
        """Queues the block textures.

        Returns:
            object: The parent's queue method result.
        """
        return super().queue()

    def _export(self):
        """Exports the block textures if at least one block texture was added.

        Returns:
            object: The parent's export method result.
        """
        if len(self._content["texture_data"]) > 0:
            for items in self._content["texture_data"].values():
                for sprite in items["textures"]:
                    CopyFiles(
                        os.path.join("assets", "textures", "blocks"),
                        os.path.join(
                            "resource_packs",
                            f"RP_{ANVIL.PASCAL_PROJECT_NAME}",
                            sprite.rstrip(sprite.split("/")[-1]),
                        ),
                        sprite.split("/")[-1] + ".png",
                    )
            return super()._export()


class _BlocksJSON(AddonObject):
    _extensions = {0: ".json", 1: ".json"}

    def __init__(self) -> None:
        super().__init__("blocks", os.path.join("resource_packs", f"RP_{ANVIL.PASCAL_PROJECT_NAME}"))
        self.content(_JsonSchemes.blocks(ANVIL.PROJECT_NAME))

    def add_block(self, block_name: str):
        self._content["texture_data"][block_name] = {
            "sound": "",
            # "textures":{},
            # "carried_textures":{},
            # "brightness_gamma": 0,
            # "isotropic":True
        }


# Used for individual sounds
class _SoundDescription:

    def __init__(
        self,
        sound_reference: str,
        category: SoundCategory,
        use_legacy_max_distance: bool = False,
        max_distance: float = 0,
        min_distance: float = 9999,
    ) -> None:
        """Initializes a _SoundDescription instance.

        Args:
            sound_reference (str): The definition of the sound.
            category (SoundCategory): The category of the sound.
            use_legacy_max_distance (bool, optional): Use legacy max distance if True. Defaults to False.
            max_distance (int, optional): The maximum distance for the sound. Defaults to 0.
            min_distance (int, optional): The minimum distance for the sound. Defaults to 9999.
        """
        self._category = category.value
        self._sound_definition = f"{ANVIL.NAMESPACE}:{sound_reference}"
        self._sound = _JsonSchemes.sound(self._sound_definition, self._category)

        if use_legacy_max_distance != False:
            self._sound[self._sound_definition].update({"__use_legacy_max_distance": use_legacy_max_distance})
        if max_distance != 0:
            self._sound[self._sound_definition].update({"max_distance": max_distance})
        if min_distance != 9999:
            self._sound[self._sound_definition].update({"min_distance": min_distance})
        self._sounds = []

    def add_sound(
        self,
        sound_name,
        volume: int = 1,
        weight: int = 1,
        pitch: int = [1, 1],
        is_3d: bool = None,
        stream: bool = None,
        load_on_low_memory: bool = False,
    ):
        """Adds a sound to the _SoundDescription instance.

        Args:
            sound_name (str): The name of the sound.
            volume (int, optional): The volume of the sound. Defaults to 1.
            weight (int, optional): The weight of the sound. Defaults to 1.
            pitch (list[int], optional): The pitch of the sound. Defaults to [1, 1].
            is_3d (bool, optional): If the sound is 3D. Defaults to None.
            stream (bool, optional): If the sound is streamed. Defaults to None.
            load_on_low_memory (bool, optional): If the sound is loaded on low memory. Defaults to False.
        """
        if not FileExists(os.path.join("assets", "sounds", f"{sound_name}.ogg")):
            ANVIL.Logger.file_exist_error(f"{sound_name}.ogg", os.path.join("assets", "sounds"))

        self._sound_name = sound_name
        splits = self._sound_definition.removeprefix(f"{ANVIL.NAMESPACE}:").split(".")
        self._path = ANVIL.NAMESPACE
        for i in range(len(splits) - 1):
            self._path = os.path.join(self._path, splits[i])
        sound = {"name": os.path.join("sounds", self._path, self._sound_name), "load_on_low_memory": load_on_low_memory}
        if pitch != [1, 1]:
            sound.update({"pitch": pitch})
        if not is_3d is None:
            sound.update({"is3D": is_3d})
        if not stream is None:
            sound.update({"stream": stream})
        if volume != 1:
            sound.update({"volume": volume})
        if weight != 1:
            sound.update({"weight": weight})
        self._sounds.append(sound)

        ANVIL._report.add_report(
            ReportType.SOUND, 
            col0 = self._sound_definition, 
            col1 = self._sound_name,
            vanilla = False
        )
        return self

    @property
    def identifier(self):
        return self._sound_reference
    
    @property
    def _export(self):
        """Returns the sound description.

        Returns:
            dict: The sound description
        """
        for sound in self._sounds:
            s = sound["name"].split("\\")[-1]
            CopyFiles(
                os.path.join("assets", "sounds"),
                os.path.join(
                    "resource_packs",
                    f"RP_{ANVIL.PASCAL_PROJECT_NAME}",
                    "sounds",
                    self._path,
                ),
                f"{s}.ogg",
            )
        self._sound[self._sound_definition]["sounds"] = self._sounds
        return self._sound


class _SoundDefinition(AddonObject):
    """Handles sound definitions.

    Attributes:
        _sounds (list[_SoundDescription], optional): A list of sound descriptions. Defaults to empty list.
    """

    def __init__(self) -> None:
        """Initializes a _SoundDefinition instance."""
        super().__init__(
            "sound_definitions",
            os.path.join("resource_packs", f"RP_{PASCAL_PROJECT_NAME}", "sounds"),
        )
        self.content(_JsonSchemes.sound_definitions())
        self._sounds: list[_SoundDescription] = []

    def sound_reference(
        self,
        sound_reference: str,
        category: SoundCategory,
        use_legacy_max_distance: bool = False,
        max_distance: float = 0,
        min_distance: float = 9999,
    ):
        """Defines a sound for the _SoundDefinition instance.

        Args:
            sound_reference (str): The sound_reference of the sound.
            category (SoundCategory): The category of the sound.
            use_legacy_max_distance (bool, optional): Use legacy max distance if True. Defaults to False.
            max_distance (int, optional): The maximum distance for the sound. Defaults to 0.
            min_distance (int, optional): The minimum distance for the sound. Defaults to 9999.

        Returns:
            _SoundDescription: The created sound description instance.
        """
        sound = _SoundDescription(
            sound_reference,
            category,
            use_legacy_max_distance,
            max_distance,
            min_distance,
        )
        self._sounds.append(sound)
        return sound

    @property
    def queue(self):
        """Returns the queue for the sound definition.

        Returns:
            queue: The queue for the sound definition.
        """
        return super().queue("")

    def _export(self):
        """Returns the sound definition.

        Returns:
            dict: The sound definition.
        """
        for sound in self._sounds:
            self._content["sound_definitions"].update(sound._export)
        return super()._export()


class _MusicDefinition(AddonObject):
    """Handles music definitions.

    Attributes:
        _extensions (dict): The file extensions for the music definition.
        _sounds (list[_SoundDescription], optional): A list of sound descriptions. Defaults to empty list.
    """

    def __init__(self) -> None:
        """Initializes a _MusicDefinition instance."""
        super().__init__(
            "music_definitions",
            os.path.join("resource_packs", f"RP_{PASCAL_PROJECT_NAME}", "sounds"),
        )
        self.content(_JsonSchemes.music_definitions())
        self._sounds: list[_SoundDescription] = []

    def music_definition(self, music_category: MusicCategory, min_delay: int = 60, max_delay: int = 180):
        """Defines a music for the _MusicDefinition instance.

        Args:
            music_category (MusicCategory): The category of the music.
            min_delay (int, optional): The minimum delay for the music. Defaults to 60.
            max_delay (int, optional): The maximum delay for the music. Defaults to 180.

        Returns:
            _SoundDescription: The created sound description instance.
        """
        self._content.update(
            {
                music_category.value: {
                    "event_name": f"music.{music_category}",
                    "max_delay": max_delay,
                    "min_delay": min_delay,
                }
            }
        )
        sound = ANVIL.sound(f"music.{music_category}", SoundCategory.Music)
        self._sounds.append(sound)
        return sound

    @property
    def queue(self):
        """Returns the queue for the music definition.

        Returns:
            queue: The queue for the music definition.
        """
        return super().queue("")

    def _export(self):
        """Returns the music definition.

        Returns:
            dict: The music definition.
        """
        return super()._export()


class _SoundEvent(AddonObject):
    """Handles sound events."""

    def __init__(self) -> None:
        """Initializes a _SoundEvent instance."""
        super().__init__("sounds", os.path.join("resource_packs", f"RP_{PASCAL_PROJECT_NAME}"))
        self.content(_JsonSchemes.sounds())

    def add_entity_event(
        self,
        identifier: Identifier,
        sound_identifier: str,
        sound_event: EntitySoundEvent,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
    ):
        """Adds an entity event to the _SoundEvent instance.

        Args:
            identifier (Identifier): The identifier of the entity.
            sound_event (EntitySoundEvent): The sound event for the entity.
            sound_identifier (str): The identifier of the sound.
            volume (float, optional): The volume of the event. Defaults to 1.0.
            pitch (tuple[float, float], optional): The pitch of the event. Defaults to (0.8, 1.2).
        """

        if not identifier in self._content["entity_sounds"]["entities"]:
            self._content["entity_sounds"]["entities"][identifier] = {"volume": volume, "pitch": (0.8, 1.2), "events": {}}

        self._content["entity_sounds"]["entities"][identifier]["events"][sound_event.value] = {"sound": f"{ANVIL.NAMESPACE}:{sound_identifier}"}

        if pitch != (0.8, 1.2):
            self._content["entity_sounds"]["entities"][identifier]["events"][sound_event.value]["pitch"] = pitch

    @property
    def queue(self):
        """Returns the queue for the sound event.

        Returns:
            queue: The queue for the sound event.
        """
        return super().queue()


class _Materials(AddonObject):
    """Handles materials.

    Attributes:
        _materials (list[_Material], optional): A list of materials. Defaults to empty list.
    """

    _extensions = {0: ".material", 1: ".material"}

    def __init__(self) -> None:
        """Initializes a _Materials instance."""
        super().__init__(
            "entity",
            os.path.join("resource_packs", f"RP_{PASCAL_PROJECT_NAME}", "materials"),
        )
        self._materials: list[_Material] = []

    def add_material(self, material_name, base_material):
        """Adds a material to the _Materials instance.

        Args:
            material_name (str): The name of the material.
            base_material (str): The base material.

        Returns:
            _Material: The created material instance.
        """
        material = _Material(material_name, base_material)
        self._materials.append(material)
        return material

    @property
    def queue(self):
        """Returns the queue for the materials.

        Returns:
            queue: The queue for the materials.
        """
        if len(self._materials) > 0:
            self._content = _JsonSchemes.materials()
            for m in self._materials:
                self._content["materials"].update(m._queue)
            super().queue("")


class _Material:
    """A class representing a material with customizable states and definitions.

    Attributes:
        _material_name (str): The name of the material.
        _material (dict): The attributes and states of the material.
    """

    def __init__(self, material_name, base_material) -> None:
        """
        Initializes a _Material instance.

        Args:
            material_name (str): The name of the material.
            base_material (str): The base material's name, if any.
        """
        self._material_name = f"{material_name}" + f":{base_material}" if not base_material is None else ""
        self._material = {self._material_name: {}}

    def states(self, *states: MaterialStates):
        """
        Sets the states for the material.

        Args:
            states (MaterialStates): The material states to be set.

        Returns:
            _Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["states"] = [s.value for s in states]
        return self

    def remove_states(self, *states: MaterialStates):
        """
        Removes the states for the material.

        Args:
            states (MaterialStates): The material states to be removed.

        Returns:
            _Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["-states"] = [s.value for s in states]
        return self

    def add_states(self, *states: MaterialStates):
        """
        Adds states to the material.

        Args:
            states (MaterialStates): The material states to be added.

        Returns:
            _Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["+states"] = [s.value for s in states]
        return self

    def frontFace(
        self,
        stencilFunc: MaterialFunc = None,
        stencilFailOp: MaterialOperation = None,
        stencilDepthFailOp: MaterialOperation = None,
        stencilPassOp: MaterialOperation = None,
        stencilPass: MaterialOperation = None,
    ):
        """
        Sets the front face stencil properties of the material.

        Args:
            stencilFunc (MaterialFunc, optional): The function for the stencil.
            stencilFailOp (MaterialOperation, optional): The operation on fail for the stencil.
            stencilDepthFailOp (MaterialOperation, optional): The operation on depth fail for the stencil.
            stencilPassOp (MaterialOperation, optional): The operation on pass for the stencil.
            stencilPass (MaterialOperation, optional): The pass for the stencil.

        Returns:
            _Material: The instance of the class to enable method chaining.
        """
        a = {
            "stencilFunc": stencilFunc,
            "stencilFailOp": stencilFailOp,
            "stencilDepthFailOp": stencilDepthFailOp,
            "stencilPassOp": stencilPassOp,
            "stencilPass": stencilPass,
        }
        self._material[self._material_name]["frontFace"] = {key: value.value for key, value in a.items() if value != None}
        return self

    def backFace(
        self,
        stencilFunc: MaterialFunc = None,
        stencilFailOp: MaterialOperation = None,
        stencilDepthFailOp: MaterialOperation = None,
        stencilPassOp: MaterialOperation = None,
        stencilPass: MaterialOperation = None,
    ):
        """
        Sets the back face stencil properties of the material.

        Args:
            stencilFunc (MaterialFunc, optional): The function for the stencil.
            stencilFailOp (MaterialOperation, optional): The operation on fail for the stencil.
            stencilDepthFailOp (MaterialOperation, optional): The operation on depth fail for the stencil.
            stencilPassOp (MaterialOperation, optional): The operation on pass for the stencil.
            stencilPass (MaterialOperation, optional): The pass for the stencil.

        Returns:
            _Material: The instance of the class to enable method chaining.
        """
        a = {
            "stencilFunc": stencilFunc,
            "stencilFailOp": stencilFailOp,
            "stencilDepthFailOp": stencilDepthFailOp,
            "stencilPassOp": stencilPassOp,
            "stencilPass": stencilPass,
        }
        self._material[self._material_name]["backFace"] = {key: value.value for key, value in a.items() if value != None}
        return self

    def stencilRef(self, stencilRef: int):
        """
        Sets the stencil reference value of the material.

        Args:
            stencilRef (int): The reference value for the stencil.

        Returns:
            _Material: The instance of the class to enable method chaining.
        """

        self._material[self._material_name]["stencilRef"] = stencilRef
        return self

    def depthFunc(self, depthFunc: MaterialFunc):
        """
        Sets the depth function of the material.

        Args:
            depthFunc (MaterialFunc): The function for the depth.

        Returns:
            _Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["depthFunc"] = depthFunc.value
        return self

    def defines(self, *defines: MaterialDefinitions):
        """
        Sets the defines for the material.

        Args:
            defines (MaterialDefinitions): The defines for the material.

        Returns:
            _Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["defines"] = [s.value for s in defines]
        return self

    def remove_defines(self, *defines: MaterialDefinitions):
        """
        Removes the defines for the material.

        Args:
            defines (MaterialDefinitions): The defines to be removed.

        Returns:
            _Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["-defines"] = [s.value for s in defines]
        return self

    def add_defines(self, *defines: MaterialDefinitions):
        """
        Adds defines to the material.

        Args:
            defines (MaterialDefinitions): The defines to be added.

        Returns:
            _Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["+defines"] = [s.value for s in defines]
        return self

    @property
    def _queue(self):
        """
        Provides the dictionary representing the material's states and properties.

        Returns:
            dict: The material dictionary.
        """
        return self._material


class _Anvil:
    """A class representing an Anvil instance."""

    def _manifests_and_langs(self):
        l = _JsonSchemes.pack_name_lang(self.DISPLAY_NAME, self.PROJECT_DESCRIPTION)
        l.extend([f"{k}={v}" for k, v in self._langs.items()])

        File(
            "languages.json",
            _JsonSchemes.languages(),
            os.path.join("behavior_packs", f"BP_{self.PASCAL_PROJECT_NAME}", "texts"),
            "w",
        )
        File(
            "languages.json",
            _JsonSchemes.languages(),
            os.path.join("resource_packs", f"RP_{self.PASCAL_PROJECT_NAME}", "texts"),
            "w",
        )
        File("languages.json", _JsonSchemes.languages(), "texts", "w")

        File("en_US.lang", "\n".join(l), f"resource_packs/RP_{self.PASCAL_PROJECT_NAME}/texts", "w")
        File(
            "en_US.lang",
            "\n".join(_JsonSchemes.pack_name_lang(self.DISPLAY_NAME, self.PROJECT_DESCRIPTION)),
            f"behavior_packs/BP_{self.PASCAL_PROJECT_NAME}/texts",
            "w",
        )
        File("en_US.lang", "\n".join(_JsonSchemes.pack_name_lang(self.DISPLAY_NAME, self.PROJECT_DESCRIPTION)), "texts", "w")

        File(
            "manifest.json",
            _JsonSchemes.manifest_rp(self.RELEASE, self.Config.get_option("build", "rp_uuid"), self.Config.get_option("anvil", "pbr")),
            os.path.join("resource_packs", f"RP_{self.PASCAL_PROJECT_NAME}"),
            "w",
        )
        File(
            "manifest.json",
            _JsonSchemes.manifest_bp(
                self.RELEASE, self.Config.get_option("build", "bp_uuid"), self.Config.get_option("anvil", "scriptapi"), self.Config.get_option("anvil", "scriptui")
            ),
            os.path.join("behavior_packs", f"BP_{self.PASCAL_PROJECT_NAME}"),
            "w",
        )
        File(
            "manifest.json",
            _JsonSchemes.manifest_world(
                self.RELEASE, self.Config.get_option("build", "pack_uuid"), self.COMPANY, self.Config.get_option("anvil", "random_seed")
            ),
            "",
            "w",
        )

        File("world_resource_packs.json", _JsonSchemes.world_packs(self.Config.get_option("build", "rp_uuid"), self.RELEASE), ".", "w")
        File("world_behavior_packs.json", _JsonSchemes.world_packs(self.Config.get_option("build", "bp_uuid"), self.RELEASE), ".", "w")
        if self.Config.get_option("anvil", "scriptapi"):
            File(
                "package.json",
                _JsonSchemes.packagejson(
                    self.PROJECT_NAME, self.RELEASE, self.PROJECT_DESCRIPTION, self.COMPANY
                ),
                "",
                "w",
                True,
            )

    def get_github_file(self, path: str):
        if not FileExists(os.path.join("assets", "vanilla", path)):
            self._clone_vanilla()

        with open(os.path.join("assets", "vanilla", path), "r") as file:
            r = json.load(file)
        return r

    def __init__(self, config: _Config, logger: _Logger):
        """Initializes an Anvil instance.

        Args:
            config (_Config): The config of the Anvil instance.
            logger (_Logger): The logger of the Anvil instance.
        """
        # ------------------------------------------------------------------------
        self.Logger = logger
        self.Logger.header()

        self.Config = config
        # ------------------------------------------------------------------------
        self.VANILLA_VERSION = self.Config.get_option("minecraft", "vanilla_version")
        self.COMPANY = self.Config.get_option("package", "company")
        self.NAMESPACE = self.Config.get_option("package", "namespace")
        self.PROJECT_NAME = self.Config.get_option("package", "project_name")
        self.DISPLAY_NAME = self.Config.get_option("package", "display_name")
        self.PROJECT_DESCRIPTION = self.Config.get_option("package", "project_description")
        self.RELEASE = self.Config.get_option("build", "release")
        self.DEBUG = self.Config.get_option("anvil", "debug")
        self.NAMESPACE_FORMAT_BIT = int(self.Config.get_option("anvil", "namespace_format"))
        self.NAMESPACE_FORMAT = self.NAMESPACE + f".{self.PROJECT_NAME}" * self.NAMESPACE_FORMAT_BIT
        self.PASCAL_PROJECT_NAME = self.Config.get_option("anvil", "pascal_project_name")
        self.LAST_CHECK = self.Config.get_option("anvil", "last_check")

        validate_namespace_project_name(self.NAMESPACE, self.PROJECT_NAME)

        global PASCAL_PROJECT_NAME, PROJECT_NAME
        PASCAL_PROJECT_NAME = self.PASCAL_PROJECT_NAME
        PROJECT_NAME = self.PROJECT_NAME
        # ------------------------------------------------------------------------
        self._objects_list: list[AddonObject] = []
        self._item_texture = _ItemTextures()
        self._terrain_texture = _TerrainTextures()
        self._sound_definition = _SoundDefinition()
        self._music_definition = _MusicDefinition()
        self._sound_event = _SoundEvent()
        self._materials = _Materials()
        self._debug = RawTextConstructor()
        # ------------------------------------------------------------------------
        # Tracks scores
        self._scores = {
            self.PROJECT_NAME: 0,  # Fake player, used to track everything,
            "negative_one": -1,  # Constant, useful for mathematical operations
        }
        # Tracks key-value langs
        self._langs = {}
        # Tracks skins key-value langs
        self._skins_langs = {}
        self._tags = []
        # ----------------------------------
        self._report = ReportCollector().add_headers()
        self._tellraw_index = 0
        self._score_index = 0
        self._deltatime = int((datetime.now() - datetime.strptime(self.LAST_CHECK, "%Y-%m-%d %H:%M:%S")).total_seconds())
        self._github = None
        self._compiled = False
        # click.echo(EXECUTION_TIME(datetime.now().strptime(LAST_CHECK, "%Y-%m-%d %H:%M:%S")))
        # 12 Hours
        if self._deltatime > 12 * 3600:
            self.Logger.check_update()
            try:
                j = requests.get("https://raw.githubusercontent.com/Mojang/bedrock-samples/main/version.json")
                self.LATEST_BUILD = json.loads(j.text)["latest"]["version"]
            except:
                self.LATEST_BUILD = self.VANILLA_VERSION
            if self.VANILLA_VERSION < self.LATEST_BUILD:
                self.Logger.new_minecraft_build(self.VANILLA_VERSION, self.LATEST_BUILD)
            else:
                click.echo(self.Logger.minecraft_build_up_to_date())

            self.Config.add_option("minecraft", "vanilla_version", self.LATEST_BUILD)
            self.Config.add_option("anvil", "last_check", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def require_config(self, *options):
        """Checks if the config has the required options.

        Args:
            options (str): The options to check.
        """
        missing = False

        if not ANVIL.Config.has_section(PROJECT_NAME) or any(
            [not self.Config.has_option(PROJECT_NAME, option) for option in options]
        ):
            self.Logger.project_missing_config()
            if not self.Config.has_section(PROJECT_NAME):
                ANVIL.Config.add_section(PROJECT_NAME)

        for option in options:
            if not self.Config.has_option(PROJECT_NAME, option):
                missing = True
                ANVIL.Config.add_option(PROJECT_NAME, str(option), input(f"Enter {option}: "))
                self.Logger.config_added_option(PROJECT_NAME, option)

        if missing:
            self.Logger.config_option_changeable(*options)

    def sound(
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
        return self._sound_definition.sound_reference(
            sound_reference,
            category,
            use_legacy_max_distance,
            max_distance,
            min_distance,
        )

    def music(self, music_category: MusicCategory, min_delay: int = 60, max_delay: int = 180):
        """Adds a music to the music definition.

        Args:
            music_category (MusicCategory): The category of the music.
            min_delay (int, optional): The min delay of the music. Defaults to 60.
            max_delay (int, optional): The max delay of the music. Defaults to 180.

        """
        return self._music_definition.music_definition(music_category, min_delay, max_delay)

    def localize(self, key, text) -> None:
        """
        Adds a localized string to en_US. Translatable.

        Parameters:
        ---------
        `texts` : `kwargs`
            Minecraft lang key-value pair.

        Examples:
        ---------
        >>> ANVIL.localize(raw_text_0, "Created with Anvil")
        """
        if key not in self._langs:
            self._langs[key] = text

    def score(self, **score_id_value) -> None:
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
                self.Logger.score_error(score_id)
            if score_id not in self._scores.keys():
                self._scores[score_id] = score_value

    @property
    def new_score(self):
        id = f"{ANVIL.NAMESPACE}{ANVIL._score_index}"
        self._score_index += 1
        self.score(**{id: 0})
        return id

    def tag(self, *tags: str) -> None:
        """
        Adds the provided tags to the setup functions by clearing them from all entities on setup.

        Parameters:
        ---------
        `tags` : `str`
            String tags to be added.

        Examples:
        ---------
        >>> ANVIL.tag('is_alive')
        >>> ANVIL.tag('fly','interact')
        """

        for tag in tags:
            if tag not in self._tags:
                self._tags.append(tag)

    def add_material(self, material_name, base_material: str | None = None):
        """Adds a material to the materials.json file.

        Args:
            material_name (_type_): The name of the material.
            base_material (str | None, optional): The name of the base material. Defaults to None.

        """
        return self._materials.add_material(material_name=material_name, base_material=base_material)

    @Halo(text="Translating")
    def _translate(self, include_skin_pack: bool = False) -> None:
        """
        Translates en_US to all supported Minecraft languages.
        This is a time consuming function, it will be executed with anvil.package(), so it's better to avoid it unless you really want to use it.


        Usage:
        ---------
        >>> ANVIL.translate
        """
        from deep_translator import GoogleTranslator

        def _to_lang(translator: GoogleTranslator, langs: dict, skins: bool = False):
            if skins:
                translated = _JsonSchemes.skin_pack_name_lang(self.PROJECT_NAME, self.PROJECT_NAME + " Skin Pack")
            else:
                translated = _JsonSchemes.pack_name_lang(self.PROJECT_NAME, self.PROJECT_NAME)
            for k, v in langs.items():
                translated.append(f"{k}={translator.translate(v)}")
            return translated

        for language in _JsonSchemes.languages():
            destination_language = (
                language.replace("zh_CN", "zh-CN").replace("zh_TW", "zh-TW").replace("nb_NO", "no").split("_")[0]
            )
            if not FileExists(
                os.path.join(
                    "resource_packs",
                    f"RP_{self.PASCAL_PROJECT_NAME}",
                    "texts",
                    f"{language}.lang",
                )
            ):
                self._langs = dict(sorted(self._langs.items()))
                Translator = GoogleTranslator(target=destination_language)
                File(
                    f"{language}.lang",
                    "\n".join(_to_lang(Translator, self._langs)),
                    os.path.join("resource_packs", f"RP_{self.PASCAL_PROJECT_NAME}", "texts"),
                    "w",
                )
                File(
                    f"{language}.lang",
                    "\n".join(_JsonSchemes.pack_name_lang(self.DISPLAY_NAME, self.PROJECT_DESCRIPTION)),
                    os.path.join("behavior_packs", f"BP_{self.PASCAL_PROJECT_NAME}", "texts"),
                    "w",
                )
                File(
                    f"{language}.lang",
                    "\n".join(_JsonSchemes.pack_name_lang(self.DISPLAY_NAME, self.PROJECT_DESCRIPTION)),
                    os.path.join("texts"),
                    "w",
                )
                if include_skin_pack:
                    self._skins_langs = dict(sorted(self._skins_langs.items()))
                    File(
                        f"{language}.lang",
                        "\n".join(_to_lang(Translator, self._skins_langs, True)),
                        os.path.join("assets", "skins", "texts"),
                        "w",
                    )

    @Halo(
        text="Compiling",
        spinner={
            "interval": 80,
            "frames": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        },
    )
    def compile(self) -> None:
        """Compiles the project."""
        from anvil.api.commands import Say, Scoreboard, Tag, Tellraw
        from anvil.api.features import Function, _Tick

        self._manifests_and_langs()

        if FileExists("assets/textures/gui"):
            CopyFolder(
                "assets/textures/gui",
                f"resource_packs/RP_{self.PASCAL_PROJECT_NAME}/textures/gui",
            )
        if FileExists("assets/textures/environment"):
            CopyFolder(
                "assets/textures/environment",
                f"resource_packs/RP_{self.PASCAL_PROJECT_NAME}/textures/environment",
            )

        for ui in [
            "hotbar_start_cap.png",
            "hotbar_0.png",
            "hotbar_1.png",
            "hotbar_2.png",
            "hotbar_3.png",
            "hotbar_4.png",
            "hotbar_5.png",
            "hotbar_6.png",
            "hotbar_7.png",
            "hotbar_8.png",
            "hotbar_end_cap.png",
            "selected_hotbar_slot.png",
        ]:
            if FileExists(f"assets/textures/ui/{ui}"):
                CopyFiles(
                    "assets/textures/ui",
                    f"resource_packs/RP_{self.PASCAL_PROJECT_NAME}/textures/ui",
                    ui,
                )

        if self.DEBUG:
            f = Function("debug")
            f.add(f"execute as @a run titleraw @s actionbar {self._debug}")
            f.queue()
            f.tick

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
            Tellraw(Target.A).text.text(f"Minecraft Version: {self.VANILLA_VERSION}"),
            Tellraw(Target.A).text.text(f"Pack Version: {self.RELEASE}"),
        ).queue()
        for score, value in self._scores.items():
            self._setup_scores.add(
                Scoreboard().objective.add(score, score.title()),
                Scoreboard().players.set(self.PROJECT_NAME, score, value),
            )
            self._remove_scores.add(Scoreboard().objective.remove(score))

        for tag in self._tags:
            self._remove_tags.add(Tag(Target.E).remove(tag))

        self._setup_scores.queue()
        self._remove_scores.queue()
        self._remove_tags.queue()

        self._setup_function.add(self._remove_tags.execute).add(self._remove_scores.execute).add(self._setup_scores.execute)
        self._setup_function.queue()

        self._item_texture.queue
        self._terrain_texture.queue
        self._sound_definition.queue
        self._music_definition.queue
        self._sound_event.queue
        self._materials.queue

        for object in self._objects_list:
            object._export()

        if self.Config.get_option("anvil", "scriptapi"):
            source = os.path.join("assets", "javascript")
            target = os.path.join("behavior_packs", f"BP_{self.PASCAL_PROJECT_NAME}", "scripts")

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
                        tsconfig["compilerOptions"]["outDir"] = f"behavior_packs/BP_{ANVIL.PASCAL_PROJECT_NAME}/scripts"
                        tsconfig["include"] = ["assets/javascript/**/*"]
                else:
                    tsconfig = _JsonSchemes.tsconfig(ANVIL.PASCAL_PROJECT_NAME)
                
                File("tsconfig.json", tsconfig, "", "w", False)
                process_subcommand("tsc", "Typescript compilation error")

        self._compiled = True

    @Halo(
        text="Packaging",
        spinner={
            "interval": 80,
            "frames": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        },
    )
    def package(
        self,
        skip_translation: bool = False,
        include_skin_pack: bool = False,
        apply_overlay: bool = False,
    ) -> None:
        """
        Compiles queued anvil objects, translates and packages the project.
        This function should be called at the end of development and playtesting, it packages the project and exports a submission ready .zip file.

        Notes:
        ---------
        List of items that must exist under assets/marketing
        `0-4.png`: Marketing art, must all be `1920x1080`
        `keyart.png`: Marketing Keyart, must be `1920x1080`

        Usage:
        ---------
        >>> ANVIL.package()
        >>> ANVIL.package(True)
        """

        if not self._compiled:
            self.Logger.not_compiled()
        self.Logger.packaging_zip()

        content_structure = {}

        def art():
            pack_icon_size = (256, 256)
            marketing_screenshot_size = (1920, 1080)
            store_screenshot_size = (800, 450)

            source = os.path.join("assets", "marketing")
            output_store = os.path.join("assets", "output", "Store Art")
            output_marketing = os.path.join("assets", "output", "Marketing Art")

            CreateDirectory(output_store)
            CreateDirectory(output_marketing)

            if FileExists(os.path.join(source, "pack_icon.png")):
                CopyFiles(
                    source,
                    os.path.join("behavior_packs", f"BP_{self.PASCAL_PROJECT_NAME}"),
                    "pack_icon.png",
                )
                CopyFiles(
                    source,
                    os.path.join("resource_packs", f"RP_{self.PASCAL_PROJECT_NAME}"),
                    "pack_icon.png",
                )
                original = Image.open(os.path.join(source, "pack_icon.png"))
                resized = original.resize(pack_icon_size)
                resized.convert("RGB").save(
                    os.path.join(output_store, f"{self.PROJECT_NAME}_packicon_0.jpg"),
                    dpi=(72, 72),
                    quality=95,
                )
            else:
                self.Logger.file_exist_warning("pack_icon.png")
            if FileExists(os.path.join(source, "keyart.png")):
                original = Image.open(os.path.join(source, "keyart.png")).convert("RGB")
                if apply_overlay:
                    overlay = Image.open(os.path.join(source, "keyart_overlay.png"))

                resized = original.resize(store_screenshot_size)
                if apply_overlay:
                    resize_overlay = overlay.resize(store_screenshot_size)
                    resized.paste(resize_overlay, mask=resize_overlay.split()[3])
                resized.save("world_icon.jpeg", dpi=(72, 72), quality=300)
                resized.save(
                    os.path.join(output_store, f"{self.PROJECT_NAME}_Thumbnail_0.jpg"),
                    dpi=(72, 72),
                    quality=300,
                )

                resized = original.resize(marketing_screenshot_size)
                if apply_overlay:
                    resize_overlay = overlay.resize(store_screenshot_size)
                    resized.paste(resize_overlay, mask=overlay.split()[3])
                resized.save(
                    os.path.join(output_marketing, f"{self.PROJECT_NAME}_MarketingKeyArt.jpg"),
                    dpi=(300, 300),
                    quality=300,
                )

            else:
                self.Logger.file_exist_warning("keyart.png")
            if FileExists(os.path.join(source, "panorama.png")):
                original = Image.open(os.path.join(source, "panorama.png"))
                scale_factor = 450 / original.size[1]
                resized = original.resize((round(original.size[0] * scale_factor), 450))
                resized.convert("RGB").save(
                    os.path.join(output_store, f"{self.PROJECT_NAME}_panorama_0.jpg"),
                    dpi=(72, 72),
                    quality=95,
                )
            else:
                self.Logger.file_exist_warning("panorama.png")
            
            for i in range(5):
                if FileExists(os.path.join(source, f"{i}.png")):
                    original = Image.open(os.path.join(source, f"{i}.png"))
                    resized = original.resize(store_screenshot_size)
                    resized.convert("RGB").save(
                        os.path.join(output_store, f"{self.PROJECT_NAME}_screenshot_{i}.jpg"),
                        dpi=(72, 72),
                        quality=95,
                    )
                    resized = original.resize(marketing_screenshot_size)
                    resized.convert("RGB").save(
                        os.path.join(
                            output_marketing,
                            f"{self.PROJECT_NAME}_MarketingScreenshot_{i}.jpg",
                        ),
                        dpi=(300, 300),
                        quality=100,
                    )
                else:
                    self.Logger.file_exist_warning(f"{i}.png")

            for i in range(6, 100):
                if not FileExists(os.path.join(source, f"{i}.png")):
                    break
                else:
                    original = Image.open(os.path.join(source, f"{i}.png"))
                    resized = original.resize(store_screenshot_size)
                    resized.convert("RGB").save(
                        os.path.join(output_store, f"{self.PROJECT_NAME}_screenshot_{i}.jpg"),
                        dpi=(72, 72),
                        quality=95,
                    )
                    resized = original.resize(marketing_screenshot_size)
                    resized.convert("RGB").save(
                        os.path.join(
                            output_marketing,
                            f"{self.PROJECT_NAME}_MarketingScreenshot_{i}.jpg",
                        ),
                        dpi=(300, 300),
                        quality=100,
                    )

            if FileExists(os.path.join(source, "partner_art.png")):
                original = Image.open(os.path.join(source, "partner_art.png"))
                resized = original.resize(marketing_screenshot_size)
                resized.convert("RGB").save(
                    os.path.join(output_marketing, f"{self.PROJECT_NAME}_PartnerArt.jpg"),
                    dpi=(300, 300),
                    quality=100,
                )
            else:
                self.Logger.file_exist_warning("partner_art.png")

        if not skip_translation:
            self._translate(include_skin_pack)
        if include_skin_pack:
            content_structure.update(
                {
                    os.path.join("assets", "skins"): os.path.join("Content", "skin_pack"),
                }
            )

        art()
        content_structure.update(
            {
                os.path.join("assets", "output", "Store Art"): os.path.join("Store Art"),
                os.path.join("assets", "output", "Marketing Art"): os.path.join("Marketing Art"),
                "resource_packs": os.path.join("Content", "world_template", "resource_packs"),
                "behavior_packs": os.path.join("Content", "world_template", "behavior_packs"),
                "texts": os.path.join("Content", "world_template", "texts"),
                "db": os.path.join("Content", "world_template", "db"),
                "level.dat": os.path.join("Content", "world_template"),
                "levelname.txt": os.path.join("Content", "world_template"),
                "manifest.json": os.path.join("Content", "world_template"),
                "world_icon.jpeg": os.path.join("Content", "world_template"),
                "world_behavior_packs.json": os.path.join("Content", "world_template"),
                "world_resource_packs.json": os.path.join("Content", "world_template"),
            }
        )
        zipit(
            os.path.join("assets", "output", f"{self.PROJECT_NAME}.zip"),
            content_structure,
        )

        RemoveDirectory(os.path.join("assets", "output", "Store Art"))
        RemoveDirectory(os.path.join("assets", "output", "Marketing Art"))

    @Halo(
        text="Packaging .mcaddon",
        spinner={
            "interval": 80,
            "frames": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        },
    )
    def mcaddon(self):
        """Packages the project into a .mcaddon file."""
        if not self._compiled:
            self.Logger.not_compiled()
        self.Logger.packaging_mcaddon()

        source = os.path.join("assets", "marketing")
        output = os.path.join("assets", "output")
        if FileExists(os.path.join(source, "pack_icon.png")):
            CopyFiles(
                source,
                os.path.join("behavior_packs", f"BP_{self.PASCAL_PROJECT_NAME}"),
                "pack_icon.png",
            )
            CopyFiles(
                source,
                os.path.join("resource_packs", f"RP_{self.PASCAL_PROJECT_NAME}"),
                "pack_icon.png",
            )

        resource_packs_structure = {
            os.path.join("resource_packs", f"RP_{self.PASCAL_PROJECT_NAME}"): "",
        }
        behavior_packs_structure = {
            os.path.join("behavior_packs", f"BP_{self.PASCAL_PROJECT_NAME}"): "",
        }
        content_structure = {
            os.path.join(output, f"{self.PROJECT_NAME}_RP.mcpack"): "",
            os.path.join(output, f"{self.PROJECT_NAME}_BP.mcpack"): "",
        }

        zipit(
            os.path.join(output, f"{self.PROJECT_NAME}_RP.mcpack"),
            resource_packs_structure,
        )
        zipit(
            os.path.join(output, f"{self.PROJECT_NAME}_BP.mcpack"),
            behavior_packs_structure,
        )
        zipit(os.path.join(output, f"{self.PROJECT_NAME}.mcaddon"), content_structure)
        RemoveFile(os.path.join(output, f"{self.PROJECT_NAME}_RP.mcpack"))
        RemoveFile(os.path.join(output, f"{self.PROJECT_NAME}_BP.mcpack"))

    @Halo(
        text="Packaging .mcworld",
        spinner={
            "interval": 80,
            "frames": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        },
    )
    def mcworld(self):
        """Packages the project into a .mcworld file."""
        if not self._compiled:
            self.Logger.not_compiled()
        self.Logger.packaging_mcworld()

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
            os.path.join("assets", "output", f"{self.PROJECT_NAME}.mcworld"),
            content_structure,
        )

    @Halo(
        text="Generating Technical Notes",
        spinner={
            "interval": 80,
            "frames": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        },
    )
    def generate_technical_notes(self):
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer,
                                        Table, TableStyle)

        from .__version__ import __version__

        def add_table(section_name: str, data: dict[bool, set[str]]):
            styles = getSampleStyleSheet()
            title_style = styles["Heading1"]
            title_style.spaceBefore = 0
            title_style.fontSize = 14
            title_style.textColor = colors.royalblue
            title = Paragraph(section_name, title_style)

            converted_data = []
            vanilla_true_rows = []

            for idx, (row, columns) in enumerate(data.items()):
                vals = []
                for col_name, col_values in columns.items():
                    value_string = '<br/>'.join(col_values)
                    if col_name != "vanilla":
                        vals.append(Paragraph(value_string, styles["Normal"]))
                    elif value_string == "True":
                        vanilla_true_rows.append(idx)
                converted_data.append([Paragraph(row, styles["Normal"]), *vals])
                
            table = Table(converted_data, hAlign="LEFT", colWidths=doc.width/len(converted_data[0]))
            
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
            title=f"{ANVIL.DISPLAY_NAME} Technical Notes",
            author=ANVIL.COMPANY,
            subject=f"{ANVIL.DISPLAY_NAME} Technical Notes",
            creator=f"Anvil@stark_lg {__version__}"
        )

        elements = [
            *add_table("Entities:", self._report.dict[ReportType.ENTITY]),
            *add_table("Attachables:", self._report.dict[ReportType.ATTACHABLE]),
            *add_table("Items:", self._report.dict[ReportType.ITEM]),
            *add_table("Blocks:", self._report.dict[ReportType.BLOCK]),
            *add_table("Particles:", self._report.dict[ReportType.PARTICLE]),
            *add_table("Sounds:", self._report.dict[ReportType.SOUND]),
        ]

        doc.build(elements)

    def _queue(self, object: object):
        """Queues an object to be compiled."""
        self._objects_list.append(object)


_logger = _Logger()
ANVIL = _Anvil(_Config(), _logger)
