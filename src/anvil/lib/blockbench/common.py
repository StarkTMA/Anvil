"""Shared names of the Blockbench importer."""

from enum import StrEnum
from typing import Optional


class _BlockBenchSource(StrEnum):
    ACTOR = "actors"
    BLOCK = "blocks"
    ITEM = "items"


def _blockbench_geometry_name(model_name: str, collection: Optional[str] = None) -> str:
    if collection is None:
        return model_name

    collection_name = collection.strip()
    if len(collection_name) == 0:
        raise ValueError("Collection names cannot be empty.")

    return f"{model_name}.{collection_name}"
