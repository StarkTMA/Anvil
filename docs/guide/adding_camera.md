# Adding a Custom Camera

This guide shows how to create a custom **Camera Preset** in Anvil. Camera presets allow you to define custom camera perspectives for players, useful for cutscenes, vehicles, or unique gameplay mechanics.

---

## Define the Camera

```python title="misc/my_camera.py"
from anvil.api.core.camera import CameraPreset
from anvil.api.core.enums import CameraPresets

def register_my_camera():
    # 1. Create a preset inheriting from a base behavior
    camera = CameraPreset("my_custom_camera", CameraPresets.FollowOrbit)

    # 2. Configure properties
    camera.extend_player_rendering(True) # Render player model
    camera.radius(5.0) # Distance from target

    # 3. Queue for export
    camera.queue()
```

---

## Using the Camera

Once registered, you can activate this camera using the `/camera` command or script API.

```mcfunction
# The namespace is defined in your anvilconfig.json
/camera @s set <namespace>:my_custom_camera
```

---