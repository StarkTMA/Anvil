import pytest
from anvil.api.vanilla.biomes import MinecraftBiomeTypes
from anvil.api.biomes.components import (
    BiomeSurfaceBuilder,
    BiomeSubSurfaceBuilder,
    BiomeNoiseGradient,
)
from anvil.lib.schemas import MinecraftBlockDescriptor, NoiseDescriptor, NoiseBlockSpecifier
from anvil.lib.lib import AnvilIO


def test_new_biomes():
    # Verify SulfurCaves biome is promoted and accessible
    assert MinecraftBiomeTypes.SulfurCaves == "minecraft:sulfur_caves"


def test_biome_components():
    # Verify BiomeSurfaceBuilder and BiomeSubSurfaceBuilder components can be initialized
    sb = BiomeSurfaceBuilder()
    assert sb._identifier == "minecraft:surface_builder"

    ssb = BiomeSubSurfaceBuilder()
    assert ssb._identifier == "minecraft:subsurface_builder"

    # Verify BiomeNoiseGradient supports negative ranges in [-1.0, 1.0]
    ng = BiomeNoiseGradient()
    ng.noise_type("minecraft:noise_gradient")
    
    # Try adding a valid range with negative values (e.g. [-0.5, 0.5])
    stone = MinecraftBlockDescriptor("minecraft:stone")
    ng.noise_block_specifier((-0.5, 0.5), stone)
    assert len(ng._noise_block_specifiers) == 1
    assert ng._noise_block_specifiers[0]["noise_range"] == [-0.5, 0.5]

    # Verify that a value outside [-1.0, 1.0] still raises a ValueError
    with pytest.raises(ValueError):
        ng.noise_block_specifier((-1.5, 0.5), stone)


def test_noise_descriptor():
    # Valid
    nd = NoiseDescriptor("test_noise", 4, [1.0, 0.5, 0.25])
    assert nd.name == "test_noise"
    assert nd.first_octave == 4
    assert nd.amplitudes == [1.0, 0.5, 0.25]
    assert nd.descriptor() == {
        "name": "test_noise",
        "first_octave": 4,
        "amplitudes": [1.0, 0.5, 0.25],
    }

    # Invalid types
    with pytest.raises(ValueError):
        NoiseDescriptor(123, 4, [1.0])
    with pytest.raises(ValueError):
        NoiseDescriptor("test", "4", [1.0])
    with pytest.raises(ValueError):
        NoiseDescriptor("test", 4, "not_a_list")
    with pytest.raises(ValueError):
        NoiseDescriptor("test", 4, [])
    with pytest.raises(ValueError):
        NoiseDescriptor("test", 4, ["not_a_number"])


def test_noise_block_specifier():
    stone = MinecraftBlockDescriptor("minecraft:stone")
    dirt = MinecraftBlockDescriptor("minecraft:dirt")
    
    # Valid specifiers
    nbs1 = NoiseBlockSpecifier(stone, threshold=0.5)
    assert nbs1.block == stone
    assert nbs1.threshold == 0.5
    assert nbs1.range is None
    assert nbs1.noise is None

    nbs2 = NoiseBlockSpecifier(dirt, range=(0.1, 0.9), noise="custom_noise")
    assert nbs2.block == dirt
    assert nbs2.range == {"min": 0.1, "max": 0.9}
    assert nbs2.noise == "custom_noise"

    # Test dictionary range input
    nbs3 = NoiseBlockSpecifier(dirt, range={"min": 0.2, "max": 0.8})
    assert nbs3.range == {"min": 0.2, "max": 0.8}

    # Test negative range values inside [-1, 1]
    nbs_neg = NoiseBlockSpecifier(dirt, range=(-0.5, 0.5))
    assert nbs_neg.range == {"min": -0.5, "max": 0.5}

    # Invalid range interval (must be [-1, 1])
    with pytest.raises(ValueError):
        NoiseBlockSpecifier(stone, range=(-1.1, 0.9))
    with pytest.raises(ValueError):
        NoiseBlockSpecifier(stone, range=(0.1, 1.1))
    with pytest.raises(ValueError):
        NoiseBlockSpecifier(stone, range={"min": -1.1, "max": 0.9})
    # Invalid types
    with pytest.raises(ValueError):
        NoiseBlockSpecifier(None, threshold=0.5)
    with pytest.raises(ValueError):
        NoiseBlockSpecifier(stone, noise=123)
    with pytest.raises(ValueError):
        NoiseBlockSpecifier(stone, threshold="0.5")
    with pytest.raises(ValueError):
        NoiseBlockSpecifier(stone, range="0.1-0.9")
    with pytest.raises(ValueError):
        NoiseBlockSpecifier(stone, range={"min": "0.1", "max": 0.9})
    with pytest.raises(ValueError):
        NoiseBlockSpecifier(stone)  # Neither threshold nor range


def test_biome_noise_gradient():
    nd = NoiseDescriptor("test_noise", 4, [1.0, 0.5, 0.25])
    stone = MinecraftBlockDescriptor("minecraft:stone")
    dirt = MinecraftBlockDescriptor("minecraft:dirt")
    nbs1 = NoiseBlockSpecifier(stone, threshold=0.5)
    nbs2 = NoiseBlockSpecifier(dirt, range=(0.1, 0.9), noise="custom_noise")

    ng = BiomeNoiseGradient()
    ng.noise(nd)
    ng.noise_block_specifiers([nbs1, nbs2])
    ng.non_replaceable_blocks([stone])

    # Check that it exports correctly under json normalization
    serialized = AnvilIO._normalize_json_like(ng)
    assert serialized == {
        "minecraft:noise_gradient": {
            "noise": {
                "name": "test_noise",
                "first_octave": 4,
                "amplitudes": [1.0, 0.5, 0.25],
            },
            "noise_block_specifiers": [
                {
                    "threshold": 0.5,
                    "block": "minecraft:stone",
                },
                {
                    "noise": "custom_noise",
                    "range": {"min": 0.1, "max": 0.9},
                    "block": "minecraft:dirt",
                },
            ],
            "non_replaceable_blocks": ["minecraft:stone"],
        }
    }

    # Test BiomeNoiseGradient.noise_block_specifier builder-style addition of new object
    ng2 = BiomeNoiseGradient()
    ng2.noise_block_specifier(nbs1)
    assert ng2._noise_block_specifiers == [nbs1]


def test_surface_builder_noise_gradient():
    nd = NoiseDescriptor("test_noise", 4, [1.0, 0.5, 0.25])
    stone = MinecraftBlockDescriptor("minecraft:stone")
    dirt = MinecraftBlockDescriptor("minecraft:dirt")
    nbs1 = NoiseBlockSpecifier(stone, threshold=0.5)
    nbs2 = NoiseBlockSpecifier(dirt, range=(0.1, 0.9), noise="custom_noise")

    sb = BiomeSurfaceBuilder()
    sb.set_noise_gradient_builder(
        noise=nd,
        noise_block_specifiers=[nbs1, nbs2],
        non_replaceable_blocks=[stone],
    )
    serialized_sb = AnvilIO._normalize_json_like(sb)
    assert serialized_sb == {
        "minecraft:surface_builder": {
            "builder": {
                "type": "minecraft:noise_gradient",
                "noise": {
                    "name": "test_noise",
                    "first_octave": 4,
                    "amplitudes": [1.0, 0.5, 0.25],
                },
                "noise_block_specifiers": [
                    {
                        "threshold": 0.5,
                        "block": "minecraft:stone",
                    },
                    {
                        "noise": "custom_noise",
                        "range": {"min": 0.1, "max": 0.9},
                        "block": "minecraft:dirt",
                    },
                ],
                "non_replaceable_blocks": ["minecraft:stone"],
            }
        }
    }
