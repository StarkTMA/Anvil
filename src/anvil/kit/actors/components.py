from typing import Optional
from xml.dom.minidom import Entity

from anvil import CONFIG
from anvil.api.core.types import Vector3D
from anvil.api.items.components import ItemCustomComponents
from anvil.lib.lib import clamp


class ItemCustomProjectile(ItemCustomComponents):
    """Custom projectile component with optimized parameter handling"""

    _identifier = f"{CONFIG.NAMESPACE}:custom_projectile"

    def __init__(
        self,
        projectile: Entity,
        spawn_event: Optional[str] = None,
        offset: Vector3D = (0, 0, 0),
        power: float = 1.0,
        angle_offset: float = 0.0,
    ) -> None:
        super().__init__(self._identifier)
        self._add_field("identifier", str(projectile))

        # Only add non-default values to reduce component size
        if spawn_event:
            self._add_field("spawn_event", spawn_event)
        if offset != (0, 0, 0):
            self._add_field("offset", list(offset))
        if power != 1.0:
            self._add_field("power", clamp(power, 0.0, 10.0))
        if angle_offset != 0.0:
            self._add_field("angle_offset", angle_offset)
