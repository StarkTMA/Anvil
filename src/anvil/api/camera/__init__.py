"""Camera presets, and the aim assist presets and categories they use."""

from .aim_assist import AimAssistCategories, AimAssistCategory, AimAssistPreset
from .camera import CameraPreset

__all__ = [
    "AimAssistCategories",
    "AimAssistCategory",
    "AimAssistPreset",
    "CameraPreset",
]
