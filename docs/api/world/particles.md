# World - Particles Module

::: anvil.api.world.particles

## Usage Example

```python
from anvil.api.world.particles import Particle
from anvil.api.pbr.texture_set import TextureComponents

# Exports assets/particles/my_particle.particle.json and its texture my_particle_texture.png
Particle(
    "my_particle",
    TextureComponents(color="my_particle_texture")
).queue()
```
