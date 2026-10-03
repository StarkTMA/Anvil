"""Internal Blockbench importer: loads ``assets/bbmodels/<name>.bbmodel`` and turns it
into the builders of `anvil.api.models` (geometry, animations, voxel shapes) plus textures.

Not meant to be used directly: entities, blocks and items load models through it.
"""

import json
import os

import click
from packaging.version import Version

from anvil.api.core.types import Vector2D
from anvil.lib.blockbench.animations import _AnimationsManager
from anvil.lib.blockbench.common import _BlockBenchSource, _blockbench_geometry_name
from anvil.lib.blockbench.model import (
    _BlockCulling,
    _ModelManager,
    _geometry_block_culling,
)
from anvil.lib.blockbench.textures import _TexturesManager


class _Blockbench:
    _loaded_blockbench_models: dict[str, "_Blockbench"] = {}

    def __new__(cls, filename, source: str = "actors"):
        if filename not in _Blockbench._loaded_blockbench_models:
            _Blockbench._loaded_blockbench_models[filename] = super(
                _Blockbench, cls
            ).__new__(cls)
        return _Blockbench._loaded_blockbench_models[filename]

    def __init__(self, filename: str, source: str = "actors") -> None:
        """Handles loading and managing Blockbench models.

        Parameters:
            filename (str): The name of the model file (without extension).
            source (str, optional): The source of the model. Defaults to "actors".

        Raises:
            ValueError: If the model identifier does not match the filename.
            FileNotFoundError: If the model file is not found.
        """
        if hasattr(self, "_path"):
            if source != self._source:
                raise ValueError(
                    f"Blockbench model '{filename}' was already loaded as '{self._source}' and cannot also be used as '{source}'."
                )
            return

        try:
            self._load(filename, source)
        except Exception:
            # Do not leave a half-initialised model in the cache.
            _Blockbench._loaded_blockbench_models.pop(filename, None)
            raise

    def _load(self, filename: str, source: str) -> None:
        self._path = os.path.join("assets", "bbmodels", f"{filename}.bbmodel")
        self._source = source

        if os.path.exists(self._path):
            with open(self._path, "r", encoding="utf-8") as model:
                self.bbmodel = json.load(model)
                if self.bbmodel["model_identifier"] != filename:
                    raise ValueError(
                        f"Blockbench model identifier mismatch: expected '{filename}', found '{self.bbmodel['model_identifier']}'."
                    )

                if Version(self.bbmodel["meta"]["format_version"]) < Version("5.0"):
                    raise ValueError(
                        f"'{filename}.bbmodel' Blockbench model format version '{self.bbmodel['meta']['format_version']}' is not supported. Please update your models with Blockbench 5.0 or higher to export the model."
                    )
        else:
            raise FileNotFoundError(
                f"{filename}.bbmodel not found in {os.path.join('assets', 'bbmodels')}. Please ensure the file exists."
            )

        self.model = _ModelManager(filename, source, self.bbmodel)
        self.animations = _AnimationsManager(filename, source, self.bbmodel)
        self.textures = _TexturesManager(filename, source, self.bbmodel)

    def override_bounding_box(self, bounding_box: Vector2D) -> None:
        self.model.override_bounding_box(bounding_box)

    @classmethod
    def __export__(cls):
        meshes = []
        for bb in _Blockbench._loaded_blockbench_models.values():
            bb.model.__export__()
            bb.animations.__export__()
            bb.textures.__export__()
            if bb.model._is_wavefront:
                meshes.append(bb.model._name)
        if len(meshes) > 0:
            click.echo(
                click.style(
                    f"\r[INFO]: Some Blockbench models are using a Wavefront format. This is not fully supported and it may not work correctly.",
                    fg="yellow",
                )
            )


# Used by the API modules (and tests) through `anvil.lib.blockbench`
__all__ = [
    "_Blockbench",
    "_BlockBenchSource",
    "_BlockCulling",
    "_ModelManager",
    "_AnimationsManager",
    "_TexturesManager",
    "_blockbench_geometry_name",
    "_geometry_block_culling",
]
