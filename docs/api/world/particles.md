# World - Particles Module

::: anvil.api.world.particles

## Usage Example

```python
from anvil.api.world.particles import Particle
from anvil.api.pbr.pbr import TextureComponents

# Define a particle using a texture from assets/textures/particles
Particle(
    "my_particle",
    TextureComponents(color="my_particle_texture")
).queue()
```
