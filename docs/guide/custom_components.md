# Custom Components Guide

Custom Components allow you to run custom Logic in your blocks and items using the Minecraft Script API. This guide explains how to use them in Anvil, following a modular pattern.

## 1. Defining the Component in Python

Define your own component class by subclassing `BlockCustomComponent` or `ItemCustomComponent`. A component is a dataclass: set its `identifier` and declare its parameters as fields with `json_field`. Don't write an `__init__`.

The identifier is in your project namespace. A bare name such as `"my_block_logic"` becomes `<namespace>:my_block_logic`.

### Block Component

```python
from anvil.api.blocks.components import BlockCustomComponent
from anvil.lib.jsonmodel import json_field

class MyBlockLogic(BlockCustomComponent):
    identifier = "my_block_logic"

# Usage in your block definition
block.server.components.add(MyBlockLogic())
```

### Item Component

```python
from anvil.api.items.components import ItemCustomComponent
from anvil.lib.jsonmodel import json_field

class MyItemLogic(ItemCustomComponent):
    identifier = "my_item_logic"

# Usage in your item definition
item.server.components.add(MyItemLogic())
```

### Parameters

Each field is a parameter your script reads. The annotation says what the field accepts, and Anvil checks it when the pack is exported. Bounds and JSON shapes go in `Annotated`, after the real type, so the field still shows exactly what to pass:

```python
from typing import Annotated

from anvil.api.blocks.components import BlockCustomComponent
from anvil.api.core.types import RGB, RGB255, RGBA, RGBA255, HexRGB, HexRGBA
from anvil.lib.jsonmodel import Hex, InRange, MinMax, json_field

class GravityWell(BlockCustomComponent):
    identifier = "gravity_well"

    pull: Annotated[float, InRange(0, 10)] = json_field()
    delay: Annotated[float | tuple[float, float], MinMax] = json_field(default=1)
    color: Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, Hex] | None = json_field(
        default=None
    )

block.server.components.add(GravityWell(pull=4, delay=(1, 3), color=(255, 0, 0)))
# {"<namespace>:gravity_well": {"pull": 4, "delay": {"min": 1, "max": 3}, "color": "#ff0000"}}
```

A field set to `None` is left out of the JSON. The metadata Anvil provides is in `anvil.lib.jsonmodel`: bounds (`InRange`, `NonNegative`, `Chance`, `Length`), JSON shapes (`MinMax`, `Wrapped`, `Keyed`, `Hex`, `Trigger`...) and more. `GravityWell.__schema__()` returns the JSON Schema of the component.

## 2. Implementing Logic in TypeScript

It is recommended to split your logic into separate files for each block or item, and then register them in your main entry file.

### Block Logic Example (`blocks/myBlock.ts`)

```typescript
import { BlockCustomComponent, StartupEvent } from "@minecraft/server";

const myBlockLogic: BlockCustomComponent = {
	onPlace(e) {
		// Logic when block is placed
	},
	onPlayerInteract(e) {
		// Logic when player interacts with block
	},
};

export function registerMyBlock(startup: StartupEvent) {
	// Note: Use the same identifier as defined in Python
	// Assuming NAMESPACE is imported from your constants file
	startup.blockComponentRegistry.registerCustomComponent(`${NAMESPACE}:my_block_logic`, myBlockLogic);
}
```

### Item Logic Example (`items/myItem.ts`)

```typescript
import { ItemCustomComponent, StartupEvent } from "@minecraft/server";

const myItemLogic: ItemCustomComponent = {
	onBeforeDurabilityDamage(e) {
		// Logic before durability damage
	},
};

export function registerMyItem(startup: StartupEvent) {
	startup.itemComponentRegistry.registerCustomComponent(`${NAMESPACE}:my_item_logic`, myItemLogic);
}
```

### Registering in Main (`main.ts`)

In your main entry file, listen to the `startup` event and call your registration functions.

```typescript
import { system } from "@minecraft/server";
import { registerMyBlock } from "./blocks/myBlock";
import { registerMyItem } from "./items/myItem";

system.beforeEvents.startup.subscribe((startup) => {
	registerMyBlock(startup);
	registerMyItem(startup);
});
```

## 3. Passing Custom Parameters

You can pass parameters from Python to your TypeScript component.

### Python Definition

Create a class that inherits from `BlockCustomComponents` (or `ItemCustomComponents`) and add your parameters using `_add_field`.

```python
from anvil import CONFIG
from anvil.api.blocks.components import BlockCustomComponents

class MyBlockLogic(BlockCustomComponents):
    _identifier = f"{CONFIG.NAMESPACE}:my_block_logic"

    def __init__(self, speed: float, active: bool) -> None:
        super().__init__(self._identifier)
        self._add_field("speed", speed)
        self._add_field("active", active)

# Usage
block.server.components.add(
    MyBlockLogic(speed=5.0, active=True)
)
```

### TypeScript Usage

Define an interface for your parameters and cast `customComponentParameters.params` to it.

```typescript
import { BlockComponentStepOnEvent, CustomComponentParameters } from "@minecraft/server";

interface MyBlockParams {
	speed: number;
	active: boolean;
}

const myBlockLogic: BlockCustomComponent = {
	onStepOn(e: BlockComponentStepOnEvent, params: CustomComponentParameters) {
		const myParams = params.params as MyBlockParams;

		if (myParams.active) {
			console.log(`Speed is: ${myParams.speed}`);
		}
	},
};
```

Ensure your `scriptapi` flag is enabled when creating your project or added to your `anvilconfig.json`.
