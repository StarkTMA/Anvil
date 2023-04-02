from anvil import NAMESPACE, Dimension


class VanillaBlocksItems:
    class _block:
        def __init__(self, identifier, dimension, is_vanilla, creative, *states):
            self._identifier = identifier
            self.dimension = dimension
            self._vanilla = is_vanilla
            self._creative = creative

            self.states = {}
            for state in states:
                self.add_state(state)

        def add_state(self, state):
            self.states[state.name] = state
            setattr(self, state.name, state)

        def __str__(self):
            return f"{'minecraft' if self._vanilla else NAMESPACE}:{self._identifier}"
        
        def __repr__(self):
            return f"{'minecraft' if self._vanilla else NAMESPACE}:{self._identifier}"
        
    class _state:
        def __init__(self, name, values):
            self.name = name
            self.values = values

        def __getattr__(self, name):
            if name in self.values:
                return str(name)
            else:
                raise AttributeError(
                    f"'{self.__class__.__name__}' object has no attribute '{name}'")

    CherryBoat = _block("cherry_boat", Dimension.Overworld, True, False)
    CherryButton = _block("cherry_button", Dimension.Overworld, True, False)
    CherryChestBoat = _block(
        "cherry_chest_boat", Dimension.Overworld, True, False)
    CherryDoor = _block("cherry_door", Dimension.Overworld, True, False)
    CherryFence = _block("cherry_fence", Dimension.Overworld, True, False)
    CherryFenceGate = _block(
        "cherry_fence_gate", Dimension.Overworld, True, False)
    CherryHangingSign = _block(
        "cherry_hanging_sign", Dimension.Overworld, True, False)
    CherryLeaves = _block("cherry_leaves", Dimension.Overworld, True, False)
    CherryLog = _block("cherry_log", Dimension.Overworld, True, False)
    CherryPlanks = _block("cherry_planks", Dimension.Overworld, True, False)
    CherryPressurePlate = _block(
        "cherry_pressure_plate", Dimension.Overworld, True, False)
    CherrySapling = _block("cherry_sapling", Dimension.Overworld, True, False)
    CherrySign = _block("cherry_sign", Dimension.Overworld, True, False)
    CherrySlab = _block("cherry_slab", Dimension.Overworld, True, False)
    CherryStairs = _block("cherry_stairs", Dimension.Overworld, True, False)
    CherryTrapdoor = _block(
        "cherry_trapdoor", Dimension.Overworld, True, False)
    CherryWood = _block("cherry_wood", Dimension.Overworld, True, False)
    StrippedCherryLog = _block(
        "stripped_cherry_log", Dimension.Overworld, True, False)
    StrippedCherryWood = _block(
        "stripped_cherry_wood", Dimension.Overworld, True, False)
    PinkPetals = _block("pink_petals", Dimension.Overworld, True, False)
    Brush = _block("brush", Dimension.Overworld, True, False)
    DecoratedPot = _block("decorated_pot", Dimension.Overworld, True, False)
    ArmsUpPotteryShard = _block(
        "arms_up_pottery_shard", Dimension.Overworld, True, False)
    SkullPotteryShard = _block(
        "skull_pottery_shard", Dimension.Overworld, True, False)
    PrizePotteryShard = _block(
        "prize_pottery_shard", Dimension.Overworld, True, False)
    ArcherPotteryShard = _block(
        "archer_pottery_shard", Dimension.Overworld, True, False)
    SuspiciousSand = _block(
        "suspicious_sand", Dimension.Overworld, True, False)
    Tourchflower = _block("tourchflower", Dimension.Overworld, True, False)
    TourchflowerSeeds = _block(
        "tourchflower_seeds", Dimension.Overworld, True, False)
    BambooBlock = _block("bamboo_block", Dimension.Overworld, True, False)
    StrippedBambooBlock = _block(
        "stripped_bamboo_block", Dimension.Overworld, True, False)
    BambooPlanks = _block("bamboo_planks", Dimension.Overworld, True, False)
    BambooMosaic = _block("bamboo_mosaic", Dimension.Overworld, True, False)
    BambooFence = _block("bamboo_fence", Dimension.Overworld, True, False)
    BambooFenceGate = _block(
        "bamboo_fence_gate", Dimension.Overworld, True, False)
    BambooStairs = _block("bamboo_stairs", Dimension.Overworld, True, False)
    BambooDoor = _block("bamboo_door", Dimension.Overworld, True, False)
    BambooTrapdoor = _block(
        "bamboo_trapdoor", Dimension.Overworld, True, False)
    BambooSlab = _block("bamboo_slab", Dimension.Overworld, True, False)
    BambooMosaicSlab = _block("bamboo_mosaic_slab",
                              Dimension.Overworld, True, False)
    BambooMosaicStairs = _block(
        "bamboo_mosaic_stairs", Dimension.Overworld, True, False)
    BambooBoat = _block("bamboo_boat", Dimension.Overworld, True, False)
    BambooChestBoat = _block(
        "bamboo_chest_boat", Dimension.Overworld, True, False)
    BambooButton = _block("bamboo_button", Dimension.Overworld, True, False)
    BambooPressurePlate = _block(
        "bamboo_pressure_plate", Dimension.Overworld, True, False)
    BambooSign = _block("bamboo_sign", Dimension.Overworld, True, False)
    CamelSpawnEgg = _block("camel_spawn_egg", Dimension.Overworld, True, True)
    ChiseledBookshelf = _block(
        "chiseled_bookshelf", Dimension.Overworld, True, True)
    BambooHangingSign = _block(
        "bamboo_hanging_sign", Dimension.Overworld, True, True)
    MangroveHangingSign = _block(
        "mangrove_hanging_sign", Dimension.Overworld, True, True)
    WarpedHangingSign = _block(
        "warped_hanging_sign", Dimension.Overworld, True, True)
    CrimsonHangingSign = _block(
        "crimson_hanging_sign", Dimension.Overworld, True, True)
    DarkOakHangingSign = _block(
        "dark_oak_hanging_sign", Dimension.Overworld, True, True)
    AcaciaHangingSign = _block(
        "acacia_hanging_sign", Dimension.Overworld, True, True)
    JungleHangingSign = _block(
        "jungle_hanging_sign", Dimension.Overworld, True, True)
    BirchHangingSign = _block("birch_hanging_sign",
                              Dimension.Overworld, True, True)
    SpruceHangingSign = _block(
        "spruce_hanging_sign", Dimension.Overworld, True, True)
    OakHangingSign = _block(
        "oak_hanging_sign", Dimension.Overworld, True, True)
    Planks = _block("planks", Dimension.Overworld, True, False,
                    _state("variant", ["oak_planks", "spruce_planks", "birch_planks", "jungle_planks", "acacia_planks", "dark_oak_planks"]))
    MangrovePlanks = _block(
        "mangrove_planks", Dimension.Overworld, True, False)
    CrimsonPlanks = _block("crimson_planks", Dimension.Nether, True, False)
    WarpedPlanks = _block("warped_planks", Dimension.Nether, True, False)
    CobblestoneWall = _block("cobblestone_wall", Dimension.Overworld, True, False,
                             _state("variant", ["cobblestone_wall", "mossy_cobblestone_wall", "granite_wall", "diorite_wall", "andesite_wall", "sandstone_wall", "red_sandstone_wall", "stone_brick_wall", "mossy_stone_brick_wall", "brick_wall", "nether_brick_wall", "red_nether_brick_wall", "end_stone_brick_wall", "prismarine_wall", ]))
    BlackstoneWall = _block("blackstone_wall", Dimension.Nether, True, False)
    PolishedBlackstoneWall = _block(
        "polished_blackstone_wall", Dimension.Nether, True, False)
    PolishedBlackstoneBrickWall = _block(
        "polished_blackstone_brick_wall", Dimension.Nether, True, False)
    CobbledDeepslateWall = _block(
        "cobbled_deepslate_wall", Dimension.Overworld, True, False)
    DeepslateTileWall = _block(
        "deepslate_tile_wall", Dimension.Overworld, True, False)
    PolishedDeepslateWall = _block(
        "polished_deepslate_wall", Dimension.Overworld, True, False)
    DeepslateBrickWall = _block(
        "deepslate_brick_wall", Dimension.Overworld, True, False)
    MudBrickWall = _block("mud_brick_wall", Dimension.Overworld, True, False)
    Fence = _block("fence", Dimension.Overworld, True, False,
                   _state("variant", ["oak_fence", "spruce_fence", "birch_fence", "jungle_fence", "acacia_fence", "dark_oak_fence", ]))
    MangroveFence = _block("mangrove_fence", Dimension.Overworld, True, False)
    NetherBrickFence = _block("nether_brick_fence",
                              Dimension.Nether, True, False)
    CrimsonFence = _block("crimson_fence", Dimension.Nether, True, False)
    WarpedFence = _block("warped_fence", Dimension.Nether, True, False)
    FenceGate = _block("fence_gate", Dimension.Overworld, True, False)
    SpruceFenceGate = _block(
        "spruce_fence_gate", Dimension.Overworld, True, False)
    BirchFenceGate = _block(
        "birch_fence_gate", Dimension.Overworld, True, False)
    JungleFenceGate = _block(
        "jungle_fence_gate", Dimension.Overworld, True, False)
    AcaciaFenceGate = _block(
        "acacia_fence_gate", Dimension.Overworld, True, False)
    DarkOakFenceGate = _block("dark_oak_fence_gate",
                              Dimension.Overworld, True, False)
    MangroveFenceGate = _block(
        "mangrove_fence_gate", Dimension.Overworld, True, False)
    CrimsonFenceGate = _block("crimson_fence_gate",
                              Dimension.Nether, True, False)
    WarpedFenceGate = _block(
        "warped_fence_gate", Dimension.Nether, True, False)
    NormalStoneStairs = _block(
        "normal_stone_stairs", Dimension.Overworld, True, False)
    StoneStairs = _block("stone_stairs", Dimension.Overworld, True, False)
    MossyCobblestoneStairs = _block(
        "mossy_cobblestone_stairs", Dimension.Overworld, True, False)
    OakStairs = _block("oak_stairs", Dimension.Overworld, True, False)
    SpruceStairs = _block("spruce_stairs", Dimension.Overworld, True, False)
    BirchStairs = _block("birch_stairs", Dimension.Overworld, True, False)
    JungleStairs = _block("jungle_stairs", Dimension.Overworld, True, False)
    AcaciaStairs = _block("acacia_stairs", Dimension.Overworld, True, False)
    DarkOakStairs = _block("dark_oak_stairs", Dimension.Overworld, True, False)
    MangroveStairs = _block(
        "mangrove_stairs", Dimension.Overworld, True, False)
    StoneBrickStairs = _block("stone_brick_stairs",
                              Dimension.Overworld, True, False)
    MossyStoneBrickStairs = _block(
        "mossy_stone_brick_stairs", Dimension.Overworld, True, False)
    SandstoneStairs = _block(
        "sandstone_stairs", Dimension.Overworld, True, False)
    SmoothSandstoneStairs = _block(
        "smooth_sandstone_stairs", Dimension.Overworld, True, False)
    RedSandstoneStairs = _block(
        "red_sandstone_stairs", Dimension.Overworld, True, False)
    SmoothRedSandstoneStairs = _block(
        "smooth_red_sandstone_stairs", Dimension.Overworld, True, False)
    GraniteStairs = _block("granite_stairs", Dimension.Overworld, True, False)
    PolishedGraniteStairs = _block(
        "polished_granite_stairs", Dimension.Overworld, True, False)
    DioriteStairs = _block("diorite_stairs", Dimension.Overworld, True, False)
    PolishedDioriteStairs = _block(
        "polished_diorite_stairs", Dimension.Overworld, True, False)
    AndesiteStairs = _block(
        "andesite_stairs", Dimension.Overworld, True, False)
    PolishedAndesiteStairs = _block(
        "polished_andesite_stairs", Dimension.Overworld, True, False)
    BrickStairs = _block("brick_stairs", Dimension.Overworld, True, False)
    NetherBrickStairs = _block(
        "nether_brick_stairs", Dimension.Nether, True, False)
    RedNetherBrickStairs = _block(
        "red_nether_brick_stairs", Dimension.Nether, True, False)
    EndBrickStairs = _block("end_brick_stairs",
                            Dimension.End,
                            True,
                            False, )
    QuartzStairs = _block("quartz_stairs", Dimension.Nether, True, False)
    SmoothQuartzStairs = _block(
        "smooth_quartz_stairs", Dimension.Nether, True, False)
    PurpurStairs = _block("purpur_stairs",
                          Dimension.End,
                          True,
                          False, )
    PrismarineStairs = _block(
        "prismarine_stairs", Dimension.Overworld, True, False)
    DarkPrismarineStairs = _block(
        "dark_prismarine_stairs", Dimension.Overworld, True, False)
    PrismarineBricksStairs = _block(
        "prismarine_bricks_stairs", Dimension.Overworld, True, False)
    CrimsonStairs = _block("crimson_stairs", Dimension.Nether, True, False)
    WarpedStairs = _block("warped_stairs", Dimension.Nether, True, False)
    BlackstoneStairs = _block(
        "blackstone_stairs", Dimension.Nether, True, False)
    PolishedBlackstoneStairs = _block(
        "polished_blackstone_stairs", Dimension.Nether, True, False)
    PolishedBlackstoneBrickStairs = _block(
        "polished_blackstone_brick_stairs", Dimension.Nether, True, False)
    CutCopperStairs = _block(
        "cut_copper_stairs", Dimension.Overworld, True, False)
    ExposedCutCopperStairs = _block(
        "exposed_cut_copper_stairs", Dimension.Overworld, True, False)
    WeatheredCutCopperStairs = _block(
        "weathered_cut_copper_stairs", Dimension.Overworld, True, False)
    OxidizedCutCopperStairs = _block(
        "oxidized_cut_copper_stairs", Dimension.Overworld, True, False)
    WaxedCutCopperStairs = _block(
        "waxed_cut_copper_stairs", Dimension.Overworld, True, False)
    WaxedExposedCutCopperStairs = _block(
        "waxed_exposed_cut_copper_stairs", Dimension.Overworld, True, False)
    WaxedWeatheredCutCopperStairs = _block(
        "waxed_weathered_cut_copper_stairs", Dimension.Overworld, True, False)
    WaxedOxidizedCutCopperStairs = _block(
        "waxed_oxidized_cut_copper_stairs", Dimension.Overworld, True, False)
    CobbledDeepslateStairs = _block(
        "cobbled_deepslate_stairs", Dimension.Overworld, True, False)
    DeepslateTileStairs = _block(
        "deepslate_tile_stairs", Dimension.Overworld, True, False)
    PolishedDeepslateStairs = _block(
        "polished_deepslate_stairs", Dimension.Overworld, True, False)
    DeepslateBrickStairs = _block(
        "deepslate_brick_stairs", Dimension.Overworld, True, False)
    MudBrickStairs = _block(
        "mud_brick_stairs", Dimension.Overworld, True, False)
    WoodenDoor = _block("wooden_door", Dimension.Overworld, True, False)
    SpruceDoor = _block("spruce_door", Dimension.Overworld, True, False)
    BirchDoor = _block("birch_door", Dimension.Overworld, True, False)
    JungleDoor = _block("jungle_door", Dimension.Overworld, True, False)
    AcaciaDoor = _block("acacia_door", Dimension.Overworld, True, False)
    DarkOakDoor = _block("dark_oak_door", Dimension.Overworld, True, False)
    MangroveDoor = _block("mangrove_door", Dimension.Overworld, True, False)
    IronDoor = _block("iron_door", Dimension.Overworld, True, False)
    CrimsonDoor = _block("crimson_door", Dimension.Nether, True, False)
    WarpedDoor = _block("warped_door", Dimension.Nether, True, False)
    Trapdoor = _block("trapdoor", Dimension.Overworld, True, False)
    SpruceTrapdoor = _block(
        "spruce_trapdoor", Dimension.Overworld, True, False)
    BirchTrapdoor = _block("birch_trapdoor", Dimension.Overworld, True, False)
    JungleTrapdoor = _block(
        "jungle_trapdoor", Dimension.Overworld, True, False)
    AcaciaTrapdoor = _block(
        "acacia_trapdoor", Dimension.Overworld, True, False)
    DarkOakTrapdoor = _block(
        "dark_oak_trapdoor", Dimension.Overworld, True, False)
    MangroveTrapdoor = _block(
        "mangrove_trapdoor", Dimension.Overworld, True, False)
    IronTrapdoor = _block("iron_trapdoor", Dimension.Overworld, True, False)
    CrimsonTrapdoor = _block("crimson_trapdoor", Dimension.Nether, True, False)
    WarpedTrapdoor = _block("warped_trapdoor", Dimension.Nether, True, False)
    IronBars = _block("iron_bars", Dimension.Overworld, True, False)
    Glass = _block("glass", Dimension.Overworld, True, False)
    StainedGlass = _block("stained_glass", Dimension.Overworld, True, False,
                          _state("variant", ["white_stained_glass", "gray_stained_glass", "light_gray_stained_glass", "black_stained_glass", "brown_stained_glass", "red_stained_glass", "orange_stained_glass", "yellow_stained_glass", "lime_stained_glass", "green_stained_glass", "cyan_stained_glass", "light_blue_stained_glass", "blue_stained_glass", "purple_stained_glass", "magenta_stained_glass", "pink_stained_glass", ]))
    TintedGlass = _block("tinted_glass", Dimension.Overworld, True, False)
    GlassPane = _block("glass_pane", Dimension.Overworld, True, False)
    StainedGlassPane = _block("stained_glass_pane", Dimension.Overworld, True, False,
                              _state("variant", ["white_stained_glass_pane", "gray_stained_glass_pane", "light_gray_stained_glass_pane", "black_stained_glass_pane", "brown_stained_glass_pane", "red_stained_glass_pane", "orange_stained_glass_pane", "yellow_stained_glass_pane", "lime_stained_glass_pane", "green_stained_glass_pane", "cyan_stained_glass_pane", "light_blue_stained_glass_pane", "blue_stained_glass_pane", "purple_stained_glass_pane", "magenta_stained_glass_pane", "pink_stained_glass_pane", ]))
    Ladder = _block("ladder", Dimension.Overworld, True, False)
    Scaffolding = _block("scaffolding", Dimension.Overworld, True, False)
    StoneSlab4 = _block("stone_slab4", Dimension.Overworld, True, False,
                        _state("variant", ["stone_slab", "mossy_stone_brick_slab", "cut_sandstone_slab", "cut_red_sandstone_slab", "smooth_quartz_slab", ]))
    StoneSlab = _block("stone_slab", Dimension.Overworld, True, False,
                       _state("variant", ["smooth_stone_slab", "cobblestone_slab", "stone_brick_slab", "sandstone_slab", "brick_slab", "nether_brick_slab", "quartz_slab", ]))
    StoneSlab2 = _block("stone_slab2", Dimension.Overworld, True, False,
                        _state("variant", ["mossy_cobblestone_slab", "smooth_sandstone_slab", "red_sandstone_slab", "red_nether_brick_slab", "purpur_slab", "prismarine_slab", "dark_prismarine_slab", "prismarine_brick_slab", ]))
    WoodenSlab = _block("wooden_slab", Dimension.Overworld, True, False,
                        _state("variant", ["oak_slab", "spruce_slab", "birch_slab", "jungle_slab", "acacia_slab", "dark_oak_slab", ]))
    MangroveSlab = _block("mangrove_slab", Dimension.Overworld, True, False)
    StoneSlab3 = _block("stone_slab3", Dimension.Overworld, True, False,
                        _state("variant", ["smooth_red_sandstone_slab", "granite_slab", "polished_granite_slab", "diorite_slab", "polished_diorite_slab", "andesite_slab", "polished_andesite_slab", "end_stone_slab", ]))
    CrimsonSlab = _block("crimson_slab", Dimension.Nether, True, False)
    WarpedSlab = _block("warped_slab", Dimension.Nether, True, False)
    BlackstoneSlab = _block("blackstone_slab", Dimension.Nether, True, False)
    PolishedBlackstoneSlab = _block(
        "polished_blackstone_slab", Dimension.Nether, True, False)
    PolishedBlackstoneBrickSlab = _block(
        "polished_blackstone_brick_slab", Dimension.Nether, True, False)
    CutCopperSlab = _block("cut_copper_slab", Dimension.Overworld, True, False)
    ExposedCutCopperSlab = _block(
        "exposed_cut_copper_slab", Dimension.Overworld, True, False)
    WeatheredCutCopperSlab = _block(
        "weathered_cut_copper_slab", Dimension.Overworld, True, False)
    OxidizedCutCopperSlab = _block(
        "oxidized_cut_copper_slab", Dimension.Overworld, True, False)
    WaxedCutCopperSlab = _block(
        "waxed_cut_copper_slab", Dimension.Overworld, True, False)
    WaxedExposedCutCopperSlab = _block(
        "waxed_exposed_cut_copper_slab", Dimension.Overworld, True, False)
    WaxedWeatheredCutCopperSlab = _block(
        "waxed_weathered_cut_copper_slab", Dimension.Overworld, True, False)
    WaxedOxidizedCutCopperSlab = _block(
        "waxed_oxidized_cut_copper_slab", Dimension.Overworld, True, False)
    CobbledDeepslateSlab = _block(
        "cobbled_deepslate_slab", Dimension.Overworld, True, False)
    PolishedDeepslateSlab = _block(
        "polished_deepslate_slab", Dimension.Overworld, True, False)
    DeepslateTileSlab = _block(
        "deepslate_tile_slab", Dimension.Overworld, True, False)
    DeepslateBrickSlab = _block(
        "deepslate_brick_slab", Dimension.Overworld, True, False)
    MudBrickSlab = _block("mud_brick_slab", Dimension.Overworld, True, False)
    BrickBlock = _block("brick_block", Dimension.Overworld, True, False)
    ChiseledNetherBricks = _block(
        "chiseled_nether_bricks", Dimension.Nether, True, False)
    CrackedNetherBricks = _block(
        "cracked_nether_bricks", Dimension.Nether, True, False)
    QuartzBricks = _block("quartz_bricks", Dimension.Nether, True, False)
    Stonebrick = _block("stonebrick", Dimension.Overworld, True, False,
                        _state("variant", ["stone_bricks", "mossy_stone_bricks", "cracked_stone_bricks", "chiseled_stone_bricks", ]))
    EndBricks = _block("end_bricks",
                       Dimension.End,
                       True,
                       False, )
    Prismarine = _block("prismarine", Dimension.Overworld, True, False,
                        _state("variant", ["prismarine_bricks", "prismarine", "dark_prismarine", ]))
    PolishedBlackstoneBricks = _block(
        "polished_blackstone_bricks", Dimension.Nether, True, False)
    CrackedPolishedBlackstoneBricks = _block(
        "cracked_polished_blackstone_bricks", Dimension.Nether, True, False)
    GildedBlackstone = _block(
        "gilded_blackstone", Dimension.Nether, True, False)
    ChiseledPolishedBlackstone = _block(
        "chiseled_polished_blackstone", Dimension.Nether, True, False)
    DeepslateTiles = _block(
        "deepslate_tiles", Dimension.Overworld, True, False)
    CrackedDeepslateTiles = _block(
        "cracked_deepslate_tiles", Dimension.Overworld, True, False)
    DeepslateBricks = _block(
        "deepslate_bricks", Dimension.Overworld, True, False)
    CrackedDeepslateBricks = _block(
        "cracked_deepslate_bricks", Dimension.Overworld, True, False)
    ChiseledDeepslate = _block(
        "chiseled_deepslate", Dimension.Overworld, True, False)
    Cobblestone = _block("cobblestone", Dimension.Overworld, True, False)
    MossyCobblestone = _block(
        "mossy_cobblestone", Dimension.Overworld, True, False)
    CobbledDeepslate = _block(
        "cobbled_deepslate", Dimension.Overworld, True, False)
    SmoothStone = _block("smooth_stone", Dimension.Overworld, True, False)
    Sandstone = _block("sandstone", Dimension.Overworld, True, False,
                       _state("variant", ["sandstone", "chiseled_sandstone", "cut_sandstone", "smooth_sandstone", ]))
    RedSandstone = _block("red_sandstone", Dimension.Overworld, True, False,
                          _state("variant", ["red_sandstone", "chiseled_red_sandstone", "cut_red_sandstone", "smooth_red_sandstone", ]))
    CoalBlock = _block("coal_block", Dimension.Overworld, True, False)
    DriedKelpBlock = _block(
        "dried_kelp_block", Dimension.Overworld, True, False)
    GoldBlock = _block("gold_block", Dimension.Overworld, True, False)
    IronBlock = _block("iron_block", Dimension.Overworld, True, False)
    CopperBlock = _block("copper_block", Dimension.Overworld, True, False)
    ExposedCopper = _block("exposed_copper", Dimension.Overworld, True, False)
    WeatheredCopper = _block(
        "weathered_copper", Dimension.Overworld, True, False)
    OxidizedCopper = _block(
        "oxidized_copper", Dimension.Overworld, True, False)
    WaxedCopper = _block("waxed_copper", Dimension.Overworld, True, False)
    WaxedExposedCopper = _block(
        "waxed_exposed_copper", Dimension.Overworld, True, False)
    WaxedWeatheredCopper = _block(
        "waxed_weathered_copper", Dimension.Overworld, True, False)
    WaxedOxidizedCopper = _block(
        "waxed_oxidized_copper", Dimension.Overworld, True, False)
    CutCopper = _block("cut_copper", Dimension.Overworld, True, False)
    ExposedCutCopper = _block("exposed_cut_copper",
                              Dimension.Overworld, True, False)
    WeatheredCutCopper = _block(
        "weathered_cut_copper", Dimension.Overworld, True, False)
    OxidizedCutCopper = _block(
        "oxidized_cut_copper", Dimension.Overworld, True, False)
    WaxedCutCopper = _block(
        "waxed_cut_copper", Dimension.Overworld, True, False)
    WaxedExposedCutCopper = _block(
        "waxed_exposed_cut_copper", Dimension.Overworld, True, False)
    WaxedWeatheredCutCopper = _block(
        "waxed_weathered_cut_copper", Dimension.Overworld, True, False)
    WaxedOxidizedCutCopper = _block(
        "waxed_oxidized_cut_copper", Dimension.Overworld, True, False)
    EmeraldBlock = _block("emerald_block", Dimension.Overworld, True, False)
    DiamondBlock = _block("diamond_block", Dimension.Overworld, True, False)
    LapisBlock = _block("lapis_block", Dimension.Overworld, True, False)
    RawIronBlock = _block("raw_iron_block", Dimension.Overworld, True, False)
    RawCopperBlock = _block(
        "raw_copper_block", Dimension.Overworld, True, False)
    RawGoldBlock = _block("raw_gold_block", Dimension.Overworld, True, False)
    QuartzBlock = _block("quartz_block",
                         Dimension.Nether,
                         True,
                         False,
                         _state("variant", ["quartz_block", "quartz_pillar", "chiseled_quartz_block", "smooth_quartz", ]))
    Slime = _block("slime", Dimension.Overworld, True, False)
    HoneyBlock = _block("honey_block", Dimension.Overworld, True, False)
    HoneycombBlock = _block(
        "honeycomb_block", Dimension.Overworld, True, False)
    HayBlock = _block("hay_block", Dimension.Overworld, True, False)
    BoneBlock = _block("bone_block", Dimension.Overworld, True, False)
    NetherBrick = _block("nether_brick", Dimension.Nether, True, False)
    RedNetherBrick = _block("red_nether_brick", Dimension.Nether, True, False)
    NetheriteBlock = _block("netherite_block", Dimension.Nether, True, False)
    Lodestone = _block("lodestone", Dimension.Overworld, True, False)
    Wool = _block("wool", Dimension.Overworld, True, False,
                  _state("variant", ["white_wool", "light_gray_wool", "gray_wool", "black_wool", "brown_wool", "red_wool", "orange_wool", "yellow_wool", "lime_wool", "green_wool", "cyan_wool", "light_blue_wool", "blue_wool", "purple_wool", "magenta_wool", "pink_wool", ]))
    Carpet = _block("carpet", Dimension.Overworld, True, False,
                    _state("variant", ["white_carpet", "light_gray_carpet", "gray_carpet", "black_carpet", "brown_carpet", "red_carpet", "orange_carpet", "yellow_carpet", "lime_carpet", "green_carpet", "cyan_carpet", "light_blue_carpet", "blue_carpet", "purple_carpet", "magenta_carpet", "pink_carpet", ]))
    ConcretePowder = _block("concrete_powder", Dimension.Overworld, True, False,
                            _state("variant", ["white_concrete_powder", "light_gray_concrete_powder", "gray_concrete_powder", "black_concrete_powder", "brown_concrete_powder", "red_concrete_powder", "orange_concrete_powder", "yellow_concrete_powder", "lime_concrete_powder", "green_concrete_powder", "cyan_concrete_powder", "light_blue_concrete_powder", "blue_concrete_powder", "purple_concrete_powder", "magenta_concrete_powder", "pink_concrete_powder", ]))
    Concrete = _block("concrete", Dimension.Overworld, True, False,
                      _state("variant", ["white_concrete", "light_gray_concrete", "gray_concrete", "black_concrete", "brown_concrete", "red_concrete", "orange_concrete", "yellow_concrete", "lime_concrete", "green_concrete", "cyan_concrete", "light_blue_concrete", "blue_concrete", "purple_concrete", "magenta_concrete", "pink_concrete", ]))
    Clay = _block("clay", Dimension.Overworld, True, False)
    HardenedClay = _block("hardened_clay", Dimension.Overworld, True, False)
    StainedHardenedClay = _block("stained_hardened_clay", Dimension.Overworld, True, False,
                                 _state("variant", ["white_terracotta", "light_gray_terracotta", "gray_terracotta", "black_terracotta", "brown_terracotta", "red_terracotta", "orange_terracotta", "yellow_terracotta", "lime_terracotta", "green_terracotta", "cyan_terracotta", "light_blue_terracotta", "blue_terracotta", "purple_terracotta", "magenta_terracotta", "pink_terracotta", ]))
    WhiteGlazedTerracotta = _block(
        "white_glazed_terracotta", Dimension.Overworld, True, False)
    SilverGlazedTerracotta = _block(
        "silver_glazed_terracotta", Dimension.Overworld, True, False)
    GrayGlazedTerracotta = _block(
        "gray_glazed_terracotta", Dimension.Overworld, True, False)
    BlackGlazedTerracotta = _block(
        "black_glazed_terracotta", Dimension.Overworld, True, False)
    BrownGlazedTerracotta = _block(
        "brown_glazed_terracotta", Dimension.Overworld, True, False)
    RedGlazedTerracotta = _block(
        "red_glazed_terracotta", Dimension.Overworld, True, False)
    OrangeGlazedTerracotta = _block(
        "orange_glazed_terracotta", Dimension.Overworld, True, False)
    YellowGlazedTerracotta = _block(
        "yellow_glazed_terracotta", Dimension.Overworld, True, False)
    LimeGlazedTerracotta = _block(
        "lime_glazed_terracotta", Dimension.Overworld, True, False)
    GreenGlazedTerracotta = _block(
        "green_glazed_terracotta", Dimension.Overworld, True, False)
    CyanGlazedTerracotta = _block(
        "cyan_glazed_terracotta", Dimension.Overworld, True, False)
    LightBlueGlazedTerracotta = _block(
        "light_blue_glazed_terracotta", Dimension.Overworld, True, False)
    BlueGlazedTerracotta = _block(
        "blue_glazed_terracotta", Dimension.Overworld, True, False)
    PurpleGlazedTerracotta = _block(
        "purple_glazed_terracotta", Dimension.Overworld, True, False)
    MagentaGlazedTerracotta = _block(
        "magenta_glazed_terracotta", Dimension.Overworld, True, False)
    PinkGlazedTerracotta = _block(
        "pink_glazed_terracotta", Dimension.Overworld, True, False)
    PurpurBlock = _block("purpur_block",
                         Dimension.End,
                         True,
                         False,
                         _state("variant", ["purpur_block", "purpur_pillar", ]))
    PackedMud = _block("packed_mud", Dimension.Overworld, True, False)
    MudBricks = _block("mud_bricks", Dimension.Overworld, True, False)
    NetherWartBlock = _block(
        "nether_wart_block", Dimension.Nether, True, False)
    WarpedWartBlock = _block(
        "warped_wart_block", Dimension.Nether, True, False)
    Shroomlight = _block("shroomlight", Dimension.Nether, True, False)
    CrimsonNylium = _block("crimson_nylium", Dimension.Nether, True, False)
    WarpedNylium = _block("warped_nylium", Dimension.Nether, True, False)
    Basalt = _block("basalt", Dimension.Nether, True, False)
    PolishedBasalt = _block("polished_basalt", Dimension.Nether, True, False)
    SmoothBasalt = _block("smooth_basalt", Dimension.Nether, True, False)
    SoulSoil = _block("soul_soil", Dimension.Nether, True, False)
    Dirt = _block("dirt", Dimension.Overworld, True, False,
                  _state("variant", ["dirt", "coarse_dirt", ]))
    Farmland = _block("farmland", Dimension.Overworld, True, False)
    Grass = _block("grass", Dimension.Overworld, True, False)
    GrassPath = _block("grass_path", Dimension.Overworld, True, False)
    Podzol = _block("podzol", Dimension.Overworld, True, False)
    Mycelium = _block("mycelium", Dimension.Overworld, True, False)
    Mud = _block("mud", Dimension.Overworld, True, False)
    Stone = _block("stone", Dimension.Overworld, True, False,
                   _state("variant", ["stone", "granite", "diorite", "andesite", "polished_granite", "polished_diorite", "polished_andesite", ]))
    IronOre = _block("iron_ore", Dimension.Overworld, True, False)
    GoldOre = _block("gold_ore", Dimension.Overworld, True, False)
    DiamondOre = _block("diamond_ore", Dimension.Overworld, True, False)
    LapisOre = _block("lapis_ore", Dimension.Overworld, True, False)
    RedstoneOre = _block("redstone_ore", Dimension.Overworld, True, False)
    CoalOre = _block("coal_ore", Dimension.Overworld, True, False)
    CopperOre = _block("copper_ore", Dimension.Overworld, True, False)
    EmeraldOre = _block("emerald_ore", Dimension.Overworld, True, False)
    QuartzOre = _block("quartz_ore", Dimension.Nether, True, False)
    NetherGoldOre = _block("nether_gold_ore", Dimension.Nether, True, False)
    AncientDebris = _block("ancient_debris", Dimension.Nether, True, False)
    DeepslateIronOre = _block("deepslate_iron_ore",
                              Dimension.Overworld, True, False)
    DeepslateGoldOre = _block("deepslate_gold_ore",
                              Dimension.Overworld, True, False)
    DeepslateDiamondOre = _block(
        "deepslate_diamond_ore", Dimension.Overworld, True, False)
    DeepslateLapisOre = _block(
        "deepslate_lapis_ore", Dimension.Overworld, True, False)
    DeepslateRedstoneOre = _block(
        "deepslate_redstone_ore", Dimension.Overworld, True, False)
    DeepslateEmeraldOre = _block(
        "deepslate_emerald_ore", Dimension.Overworld, True, False)
    DeepslateCoalOre = _block("deepslate_coal_ore",
                              Dimension.Overworld, True, False)
    DeepslateCopperOre = _block(
        "deepslate_copper_ore", Dimension.Overworld, True, False)
    Gravel = _block("gravel", Dimension.Overworld, True, False)
    Blackstone = _block("blackstone", Dimension.Nether, True, False)
    Deepslate = _block("deepslate", Dimension.Overworld, True, False)
    PolishedBlackstone = _block(
        "polished_blackstone", Dimension.Nether, True, False)
    PolishedDeepslate = _block(
        "polished_deepslate", Dimension.Overworld, True, False)
    Sand = _block("sand", Dimension.Overworld, True, False,
                  _state("variant", ["sand", "red_sand", ]))
    Cactus = _block("cactus", Dimension.Overworld, True, False)
    Log = _block("log", Dimension.Overworld, True, False,
                 _state("variant", ["oak_log", "spruce_log", "birch_log", "jungle_log", ]))
    StrippedOakLog = _block(
        "stripped_oak_log", Dimension.Overworld, True, False)
    StrippedSpruceLog = _block(
        "stripped_spruce_log", Dimension.Overworld, True, False)
    StrippedBirchLog = _block("stripped_birch_log",
                              Dimension.Overworld, True, False)
    StrippedJungleLog = _block(
        "stripped_jungle_log", Dimension.Overworld, True, False)
    Log2 = _block("log2", Dimension.Overworld, True, False,
                  _state("variant", ["acacia_log", "dark_oak_log", ]))
    StrippedAcaciaLog = _block(
        "stripped_acacia_log", Dimension.Overworld, True, False)
    StrippedDarkOakLog = _block(
        "stripped_dark_oak_log", Dimension.Overworld, True, False)
    MangroveLog = _block("mangrove_log", Dimension.Overworld, True, False)
    StrippedMangroveLog = _block(
        "stripped_mangrove_log", Dimension.Overworld, True, False)
    CrimsonStem = _block("crimson_stem", Dimension.Nether, True, False)
    StrippedCrimsonStem = _block(
        "stripped_crimson_stem", Dimension.Nether, True, False)
    WarpedStem = _block("warped_stem", Dimension.Nether, True, False)
    StrippedWarpedStem = _block(
        "stripped_warped_stem", Dimension.Nether, True, False)
    Wood = _block("wood", Dimension.Overworld, True, False,
                  _state("variant", ["oak_wood", "stripped_oak_wood", "spruce_wood", "stripped_spruce_wood", "birch_wood", "stripped_birch_wood", "jungle_wood", "stripped_jungle_wood", "acacia_wood", "stripped_acacia_wood", "dark_oak_wood", "stripped_dark_oak_wood", ]))
    MangroveWood = _block("mangrove_wood", Dimension.Overworld, True, False)
    StrippedMangroveWood = _block(
        "stripped_mangrove_wood", Dimension.Overworld, True, False)
    CrimsonHyphae = _block("crimson_hyphae", Dimension.Nether, True, False)
    StrippedCrimsonHyphae = _block(
        "stripped_crimson_hyphae", Dimension.Nether, True, False)
    WarpedHyphae = _block("warped_hyphae", Dimension.Nether, True, False)
    StrippedWarpedHyphae = _block(
        "stripped_warped_hyphae", Dimension.Nether, True, False)
    Leaves = _block("leaves", Dimension.Overworld, True, False,
                    _state("variant", ["oak_leaves", "spruce_leaves", "birch_leaves", "jungle_leaves", ]))
    Leaves2 = _block("leaves2", Dimension.Overworld, True, False,
                     _state("variant", ["acacia_leaves", "dark_oak_leaves", ]))
    MangroveLeaves = _block(
        "mangrove_leaves", Dimension.Overworld, True, False)
    AzaleaLeaves = _block("azalea_leaves", Dimension.Overworld, True, False)
    AzaleaLeavesFlowered = _block(
        "azalea_leaves_flowered", Dimension.Overworld, True, False)
    Sapling = _block("sapling", Dimension.Overworld, True, False,
                     _state("variant", ["oak_sapling", "spruce_sapling", "birch_sapling", "jungle_sapling", "acacia_sapling", "dark_oak_sapling", ]))
    MangrovePropagule = _block(
        "mangrove_propagule", Dimension.Overworld, True, False)
    BeeNest = _block("bee_nest", Dimension.Overworld, True, False)
    WheatSeeds = _block("wheat_seeds", Dimension.Overworld, True, False)
    PumpkinSeeds = _block("pumpkin_seeds", Dimension.Overworld, True, False)
    MelonSeeds = _block("melon_seeds", Dimension.Overworld, True, False)
    BeetrootSeeds = _block("beetroot_seeds", Dimension.Overworld, True, False)
    Wheat = _block("wheat", Dimension.Overworld, True, False)
    Beetroot = _block("beetroot", Dimension.Overworld, True, False)
    Potato = _block("potato", Dimension.Overworld, True, False)
    PoisonousPotato = _block(
        "poisonous_potato", Dimension.Overworld, True, False)
    Carrot = _block("carrot", Dimension.Overworld, True, False)
    GoldenCarrot = _block("golden_carrot", Dimension.Overworld, True, False)
    Apple = _block("apple", Dimension.Overworld, True, False)
    GoldenApple = _block("golden_apple", Dimension.Overworld, True, False)
    EnchantedGoldenApple = _block(
        "enchanted_golden_apple", Dimension.Overworld, True, False)
    MelonBlock = _block("melon_block", Dimension.Overworld, True, False)
    MelonSlice = _block("melon_slice", Dimension.Overworld, True, False)
    GlisteringMelonSlice = _block(
        "glistering_melon_slice", Dimension.Overworld, True, False)
    SweetBerries = _block("sweet_berries", Dimension.Overworld, True, False)
    GlowBerries = _block("glow_berries", Dimension.Overworld, True, False)
    Pumpkin = _block("pumpkin", Dimension.Overworld, True, False)
    CarvedPumpkin = _block("carved_pumpkin", Dimension.Overworld, True, False)
    LitPumpkin = _block("lit_pumpkin", Dimension.Overworld, True, False)
    Honeycomb = _block("honeycomb", Dimension.Overworld, True, False)
    Tallgrass = _block("tallgrass", Dimension.Overworld, True, False,
                       _state("variant", ["fern", "grass", ]))
    DoublePlant = _block("double_plant", Dimension.Overworld, True, False,
                         _state("variant", ["large_fern", "tall_grass", "sunflower", "lilac", "rose_bush", "peony", ]))
    NetherSprouts = _block("nether_sprouts", Dimension.Nether, True, False)
    Coral = _block("coral", Dimension.Overworld, True, False,
                   _state("variant", ["fire_coral", "brain_coral", "bubble_coral", "tube_coral", "horn_coral", "dead_fire_coral", "dead_brain_coral", "dead_bubble_coral", "dead_tube_coral", "dead_horn_coral", ]))
    CoralFan = _block("coral_fan", Dimension.Overworld, True, False,
                      _state("variant", ["fire_coral_fan", "brain_coral_fan", "bubble_coral_fan", "tube_coral_fan", "horn_coral_fan", ]))
    CoralFanDead = _block("coral_fan_dead", Dimension.Overworld, True, False,
                          _state("variant", ["dead_fire_coral_fan", "dead_brain_coral_fan", "dead_bubble_coral_fan", "dead_tube_coral_fan", "dead_horn_coral_fan", ]))
    Kelp = _block("kelp", Dimension.Overworld, True, False)
    Seagrass = _block("seagrass", Dimension.Overworld, True, False)
    CrimsonRoots = _block("crimson_roots", Dimension.Nether, True, False)
    WarpedRoots = _block("warped_roots", Dimension.Nether, True, False)
    YellowFlower = _block("yellow_flower", Dimension.Overworld, True, False)
    RedFlower = _block("red_flower", Dimension.Overworld, True, False,
                       _state("variant", ["poppy", "blue_orchid", "allium", "azure_bluet", "red_tulip", "orange_tulip", "white_tulip", "pink_tulip", "oxeye_daisy", "cornflower", "lily_of_the_valley", ]))
    WitherRose = _block("wither_rose", Dimension.Overworld, True, False)
    WhiteDye = _block("white_dye", Dimension.Overworld, True, False)
    LightGrayDye = _block("light_gray_dye", Dimension.Overworld, True, False)
    GrayDye = _block("gray_dye", Dimension.Overworld, True, False)
    BrownDye = _block("brown_dye", Dimension.Overworld, True, False)
    BlackDye = _block("black_dye", Dimension.Overworld, True, False)
    RedDye = _block("red_dye", Dimension.Overworld, True, False)
    OrangeDye = _block("orange_dye", Dimension.Overworld, True, False)
    YellowDye = _block("yellow_dye", Dimension.Overworld, True, False)
    LimeDye = _block("lime_dye", Dimension.Overworld, True, False)
    GreenDye = _block("green_dye", Dimension.Overworld, True, False)
    CyanDye = _block("cyan_dye", Dimension.Overworld, True, False)
    LightBlueDye = _block("light_blue_dye", Dimension.Overworld, True, False)
    BlueDye = _block("blue_dye", Dimension.Overworld, True, False)
    PurpleDye = _block("purple_dye", Dimension.Overworld, True, False)
    MagentaDye = _block("magenta_dye", Dimension.Overworld, True, False)
    PinkDye = _block("pink_dye", Dimension.Overworld, True, False)
    InkSac = _block("ink_sac", Dimension.Overworld, True, False)
    GlowInkSac = _block("glow_ink_sac", Dimension.Overworld, True, False)
    CocoaBeans = _block("cocoa_beans", Dimension.Overworld, True, False)
    LapisLazuli = _block("lapis_lazuli", Dimension.Overworld, True, False)
    BoneMeal = _block("bone_meal", Dimension.Overworld, True, False)
    Vine = _block("vine", Dimension.Overworld, True, False)
    WeepingVines = _block("weeping_vines", Dimension.Nether, True, False)
    TwistingVines = _block("twisting_vines", Dimension.Nether, True, False)
    Waterlily = _block("waterlily", Dimension.Overworld, True, False)
    Deadbush = _block("deadbush", Dimension.Overworld, True, False)
    Bamboo = _block("bamboo", Dimension.Overworld, True, False)
    Snow = _block("snow", Dimension.Overworld, True, False)
    Ice = _block("ice", Dimension.Overworld, True, False)
    PackedIce = _block("packed_ice", Dimension.Overworld, True, False)
    BlueIce = _block("blue_ice", Dimension.Overworld, True, False)
    SnowLayer = _block("snow_layer", Dimension.Overworld, True, False)
    PointedDripstone = _block(
        "pointed_dripstone", Dimension.Overworld, True, False)
    DripstoneBlock = _block(
        "dripstone_block", Dimension.Overworld, True, False)
    MossCarpet = _block("moss_carpet", Dimension.Overworld, True, False)
    MossBlock = _block("moss_block", Dimension.Overworld, True, False)
    DirtWithRoots = _block("dirt_with_roots", Dimension.Overworld, True, False)
    HangingRoots = _block("hanging_roots", Dimension.Overworld, True, False)
    MangroveRoots = _block("mangrove_roots", Dimension.Overworld, True, False)
    MuddyMangroveRoots = _block(
        "muddy_mangrove_roots", Dimension.Overworld, True, False)
    BigDripleaf = _block("big_dripleaf", Dimension.Overworld, True, False)
    SmallDripleafBlock = _block(
        "small_dripleaf_block", Dimension.Overworld, True, False)
    SporeBlossom = _block("spore_blossom", Dimension.Overworld, True, False)
    Azalea = _block("azalea", Dimension.Overworld, True, False)
    FloweringAzalea = _block(
        "flowering_azalea", Dimension.Overworld, True, False)
    GlowLichen = _block("glow_lichen", Dimension.Overworld, True, False)
    AmethystBlock = _block("amethyst_block", Dimension.Overworld, True, False)
    BuddingAmethyst = _block(
        "budding_amethyst", Dimension.Overworld, True, False)
    AmethystCluster = _block(
        "amethyst_cluster", Dimension.Overworld, True, False)
    LargeAmethystBud = _block("large_amethyst_bud",
                              Dimension.Overworld, True, False)
    MediumAmethystBud = _block(
        "medium_amethyst_bud", Dimension.Overworld, True, False)
    SmallAmethystBud = _block("small_amethyst_bud",
                              Dimension.Overworld, True, False)
    Tuff = _block("tuff", Dimension.Overworld, True, False)
    Calcite = _block("calcite", Dimension.Overworld, True, False)
    Chicken = _block("chicken", Dimension.Overworld, True, False)
    Porkchop = _block("porkchop", Dimension.Overworld, True, False)
    Beef = _block("beef", Dimension.Overworld, True, False)
    Mutton = _block("mutton", Dimension.Overworld, True, False)
    Rabbit = _block("rabbit", Dimension.Overworld, True, False)
    Cod = _block("cod", Dimension.Overworld, True, False)
    Salmon = _block("salmon", Dimension.Overworld, True, False)
    TropicalFish = _block("tropical_fish", Dimension.Overworld, True, False)
    Pufferfish = _block("pufferfish", Dimension.Overworld, True, False)
    BrownMushroom = _block("brown_mushroom", Dimension.Overworld, True, False)
    RedMushroom = _block("red_mushroom", Dimension.Overworld, True, False)
    CrimsonFungus = _block("crimson_fungus", Dimension.Nether, True, False)
    WarpedFungus = _block("warped_fungus", Dimension.Nether, True, False)
    BrownMushroomBlock = _block("brown_mushroom_block", Dimension.Overworld, True, False,
                                _state("variant", ["brown_mushroom_block", "mushroom_stem", "mushroom", ]))
    RedMushroomBlock = _block("red_mushroom_block",
                              Dimension.Overworld, True, False)
    Egg = _block("egg", Dimension.Overworld, True, False)
    SugarCane = _block("sugar_cane", Dimension.Overworld, True, False)
    Sugar = _block("sugar", Dimension.Overworld, True, False)
    RottenFlesh = _block("rotten_flesh", Dimension.Overworld, True, False)
    Bone = _block("bone", Dimension.Overworld, True, False)
    Web = _block("web", Dimension.Overworld, True, False)
    SpiderEye = _block("spider_eye", Dimension.Overworld, True, False)
    MobSpawner = _block("mob_spawner", Dimension.Nether, True, False)
    MonsterEgg = _block("monster_egg", Dimension.Overworld, True, False,
                        _state("variant", ["infested_stone", "infested_cobblestone", "infested_stone_bricks", "infested_mossy_stone_bricks", "infested_cracked_stone_bricks", "infested_chiseled_stone_bricks", ]))
    InfestedDeepslate = _block(
        "infested_deepslate", Dimension.Overworld, True, False)
    DragonEgg = _block("dragon_egg",
                       Dimension.End,
                       True,
                       False, )
    TurtleEgg = _block("turtle_egg", Dimension.Overworld, True, False)
    FrogSpawn = _block("frog_spawn", Dimension.Overworld, True, False)
    PearlescentFroglight = _block(
        "pearlescent_froglight", Dimension.Overworld, True, False)
    VerdantFroglight = _block(
        "verdant_froglight", Dimension.Overworld, True, False)
    OchreFroglight = _block(
        "ochre_froglight", Dimension.Overworld, True, False)
    ChickenSpawnEgg = _block(
        "chicken_spawn_egg", Dimension.Overworld, True, True)
    BeeSpawnEgg = _block("bee_spawn_egg", Dimension.Overworld, True, True)
    CowSpawnEgg = _block("cow_spawn_egg", Dimension.Overworld, True, True)
    PigSpawnEgg = _block("pig_spawn_egg", Dimension.Overworld, True, True)
    SheepSpawnEgg = _block("sheep_spawn_egg", Dimension.Overworld, True, True)
    WolfSpawnEgg = _block("wolf_spawn_egg", Dimension.Overworld, True, True)
    PolarBearSpawnEgg = _block(
        "polar_bear_spawn_egg", Dimension.Overworld, True, True)
    OcelotSpawnEgg = _block(
        "ocelot_spawn_egg", Dimension.Overworld, True, True)
    CatSpawnEgg = _block("cat_spawn_egg", Dimension.Overworld, True, True)
    MooshroomSpawnEgg = _block(
        "mooshroom_spawn_egg", Dimension.Overworld, True, True)
    BatSpawnEgg = _block("bat_spawn_egg", Dimension.Overworld, True, True)
    ParrotSpawnEgg = _block(
        "parrot_spawn_egg", Dimension.Overworld, True, True)
    RabbitSpawnEgg = _block(
        "rabbit_spawn_egg", Dimension.Overworld, True, True)
    LlamaSpawnEgg = _block("llama_spawn_egg", Dimension.Overworld, True, True)
    HorseSpawnEgg = _block("horse_spawn_egg", Dimension.Overworld, True, True)
    DonkeySpawnEgg = _block(
        "donkey_spawn_egg", Dimension.Overworld, True, True)
    MuleSpawnEgg = _block("mule_spawn_egg", Dimension.Overworld, True, True)
    SkeletonHorseSpawnEgg = _block(
        "skeleton_horse_spawn_egg", Dimension.Overworld, True, True)
    ZombieHorseSpawnEgg = _block(
        "zombie_horse_spawn_egg", Dimension.Overworld, True, True)
    TropicalFishSpawnEgg = _block(
        "tropical_fish_spawn_egg", Dimension.Overworld, True, True)
    CodSpawnEgg = _block("cod_spawn_egg", Dimension.Overworld, True, True)
    PufferfishSpawnEgg = _block(
        "pufferfish_spawn_egg", Dimension.Overworld, True, True)
    SalmonSpawnEgg = _block(
        "salmon_spawn_egg", Dimension.Overworld, True, True)
    DolphinSpawnEgg = _block(
        "dolphin_spawn_egg", Dimension.Overworld, True, True)
    TurtleSpawnEgg = _block(
        "turtle_spawn_egg", Dimension.Overworld, True, True)
    PandaSpawnEgg = _block("panda_spawn_egg", Dimension.Overworld, True, True)
    FoxSpawnEgg = _block("fox_spawn_egg", Dimension.Overworld, True, True)
    CreeperSpawnEgg = _block(
        "creeper_spawn_egg", Dimension.Overworld, True, True)
    EndermanSpawnEgg = _block("enderman_spawn_egg",
                              Dimension.End,
                              True,
                              True, )
    SilverfishSpawnEgg = _block(
        "silverfish_spawn_egg", Dimension.Overworld, True, True)
    SkeletonSpawnEgg = _block("skeleton_spawn_egg",
                              Dimension.Overworld, True, True)
    WitherSkeletonSpawnEgg = _block(
        "wither_skeleton_spawn_egg", Dimension.Overworld, True, True)
    StraySpawnEgg = _block("stray_spawn_egg", Dimension.Overworld, True, True)
    SlimeSpawnEgg = _block("slime_spawn_egg", Dimension.Overworld, True, True)
    SpiderSpawnEgg = _block(
        "spider_spawn_egg", Dimension.Overworld, True, True)
    ZombieSpawnEgg = _block(
        "zombie_spawn_egg", Dimension.Overworld, True, True)
    ZombiePigmanSpawnEgg = _block(
        "zombie_pigman_spawn_egg", Dimension.Overworld, True, True)
    HuskSpawnEgg = _block("husk_spawn_egg", Dimension.Overworld, True, True)
    DrownedSpawnEgg = _block(
        "drowned_spawn_egg", Dimension.Overworld, True, True)
    SquidSpawnEgg = _block("squid_spawn_egg", Dimension.Overworld, True, True)
    GlowSquidSpawnEgg = _block(
        "glow_squid_spawn_egg", Dimension.Overworld, True, True)
    CaveSpiderSpawnEgg = _block(
        "cave_spider_spawn_egg", Dimension.Overworld, True, True)
    WitchSpawnEgg = _block("witch_spawn_egg", Dimension.Overworld, True, True)
    GuardianSpawnEgg = _block("guardian_spawn_egg",
                              Dimension.Overworld, True, True)
    ElderGuardianSpawnEgg = _block(
        "elder_guardian_spawn_egg", Dimension.Overworld, True, True)
    EndermiteSpawnEgg = _block("endermite_spawn_egg",
                               Dimension.End,
                               True,
                               True, )
    MagmaCubeSpawnEgg = _block(
        "magma_cube_spawn_egg", Dimension.Nether, True, True)
    StriderSpawnEgg = _block(
        "strider_spawn_egg", Dimension.Overworld, True, True)
    HoglinSpawnEgg = _block(
        "hoglin_spawn_egg", Dimension.Overworld, True, True)
    PiglinSpawnEgg = _block(
        "piglin_spawn_egg", Dimension.Overworld, True, True)
    ZoglinSpawnEgg = _block(
        "zoglin_spawn_egg", Dimension.Overworld, True, True)
    PiglinBruteSpawnEgg = _block(
        "piglin_brute_spawn_egg", Dimension.Overworld, True, True)
    GoatSpawnEgg = _block("goat_spawn_egg", Dimension.Overworld, True, True)
    AxolotlSpawnEgg = _block(
        "axolotl_spawn_egg", Dimension.Overworld, True, True)
    WardenSpawnEgg = _block(
        "warden_spawn_egg", Dimension.Overworld, True, True)
    AllaySpawnEgg = _block("allay_spawn_egg", Dimension.Overworld, True, True)
    FrogSpawnEgg = _block("frog_spawn_egg", Dimension.Overworld, True, True)
    TadpoleSpawnEgg = _block(
        "tadpole_spawn_egg", Dimension.Overworld, True, True)
    GhastSpawnEgg = _block("ghast_spawn_egg", Dimension.Overworld, True, True)
    BlazeSpawnEgg = _block("blaze_spawn_egg", Dimension.Overworld, True, True)
    ShulkerSpawnEgg = _block(
        "shulker_spawn_egg", Dimension.Overworld, True, True)
    VindicatorSpawnEgg = _block(
        "vindicator_spawn_egg", Dimension.Overworld, True, True)
    EvokerSpawnEgg = _block(
        "evoker_spawn_egg", Dimension.Overworld, True, True)
    VexSpawnEgg = _block("vex_spawn_egg", Dimension.Overworld, True, True)
    VillagerSpawnEgg = _block("villager_spawn_egg",
                              Dimension.Overworld, True, True)
    WanderingTraderSpawnEgg = _block(
        "wandering_trader_spawn_egg", Dimension.Overworld, True, True)
    ZombieVillagerSpawnEgg = _block(
        "zombie_villager_spawn_egg", Dimension.Overworld, True, True)
    PhantomSpawnEgg = _block(
        "phantom_spawn_egg", Dimension.Overworld, True, True)
    PillagerSpawnEgg = _block("pillager_spawn_egg",
                              Dimension.Overworld, True, True)
    RavagerSpawnEgg = _block(
        "ravager_spawn_egg", Dimension.Overworld, True, True)
    Obsidian = _block("obsidian", Dimension.Overworld, True, False)
    CryingObsidian = _block("crying_obsidian", Dimension.Nether, True, False)
    Bedrock = _block("bedrock", Dimension.Overworld, True, False)
    SoulSand = _block("soul_sand", Dimension.Nether, True, False)
    Netherrack = _block("netherrack", Dimension.Nether, True, False)
    Magma = _block("magma", Dimension.Nether, True, False)
    NetherWart = _block("nether_wart", Dimension.Nether, True, False)
    EndStone = _block("end_stone",
                      Dimension.End,
                      True,
                      False, )
    ChorusFlower = _block("chorus_flower",
                          Dimension.End,
                          True,
                          False, )
    ChorusPlant = _block("chorus_plant",
                         Dimension.End,
                         True,
                         False, )
    ChorusFruit = _block("chorus_fruit",
                         Dimension.End,
                         True,
                         False, )
    PoppedChorusFruit = _block("popped_chorus_fruit",
                               Dimension.End,
                               True,
                               False, )
    Sponge = _block("sponge", Dimension.Overworld, True, False,
                    _state("variant", ["sponge", "wet_sponge", ]))
    CoralBlock = _block("coral_block", Dimension.Overworld, True, False,
                        _state("variant", ["tube_coral_block", "brain_coral_block", "bubble_coral_block", "fire_coral_block", "horn_coral_block", "dead_tube_coral_block", "dead_brain_coral_block", "dead_bubble_coral_block", "dead_fire_coral_block", "dead_horn_coral_block", ]))
    Sculk = _block("sculk", Dimension.Overworld, True, False)
    SculkVein = _block("sculk_vein", Dimension.Overworld, True, False)
    SculkCatalyst = _block("sculk_catalyst", Dimension.Overworld, True, False)
    SculkShrieker = _block("sculk_shrieker", Dimension.Overworld, True, False)
    SculkSensor = _block("sculk_sensor", Dimension.Overworld, True, False)
    ReinforcedDeepslate = _block(
        "reinforced_deepslate", Dimension.Overworld, True, False)
    LeatherHelmet = _block("leather_helmet", Dimension.Overworld, True, False)
    ChainmailHelmet = _block(
        "chainmail_helmet", Dimension.Overworld, True, False)
    IronHelmet = _block("iron_helmet", Dimension.Overworld, True, False)
    GoldenHelmet = _block("golden_helmet", Dimension.Overworld, True, False)
    DiamondHelmet = _block("diamond_helmet", Dimension.Overworld, True, False)
    NetheriteHelmet = _block("netherite_helmet", Dimension.Nether, True, False)
    LeatherChestplate = _block(
        "leather_chestplate", Dimension.Overworld, True, False)
    ChainmailChestplate = _block(
        "chainmail_chestplate", Dimension.Overworld, True, False)
    IronChestplate = _block(
        "iron_chestplate", Dimension.Overworld, True, False)
    GoldenChestplate = _block(
        "golden_chestplate", Dimension.Overworld, True, False)
    DiamondChestplate = _block(
        "diamond_chestplate", Dimension.Overworld, True, False)
    NetheriteChestplate = _block(
        "netherite_chestplate", Dimension.Nether, True, False)
    LeatherLeggings = _block(
        "leather_leggings", Dimension.Overworld, True, False)
    ChainmailLeggings = _block(
        "chainmail_leggings", Dimension.Overworld, True, False)
    IronLeggings = _block("iron_leggings", Dimension.Overworld, True, False)
    GoldenLeggings = _block(
        "golden_leggings", Dimension.Overworld, True, False)
    DiamondLeggings = _block(
        "diamond_leggings", Dimension.Overworld, True, False)
    NetheriteLeggings = _block(
        "netherite_leggings", Dimension.Nether, True, False)
    LeatherBoots = _block("leather_boots", Dimension.Overworld, True, False)
    ChainmailBoots = _block(
        "chainmail_boots", Dimension.Overworld, True, False)
    IronBoots = _block("iron_boots", Dimension.Overworld, True, False)
    GoldenBoots = _block("golden_boots", Dimension.Overworld, True, False)
    DiamondBoots = _block("diamond_boots", Dimension.Overworld, True, False)
    NetheriteBoots = _block("netherite_boots", Dimension.Nether, True, False)
    WoodenSword = _block("wooden_sword", Dimension.Overworld, True, False)
    StoneSword = _block("stone_sword", Dimension.Overworld, True, False)
    IronSword = _block("iron_sword", Dimension.Overworld, True, False)
    GoldenSword = _block("golden_sword", Dimension.Overworld, True, False)
    DiamondSword = _block("diamond_sword", Dimension.Overworld, True, False)
    NetheriteSword = _block("netherite_sword", Dimension.Nether, True, False)
    WoodenAxe = _block("wooden_axe", Dimension.Overworld, True, False)
    StoneAxe = _block("stone_axe", Dimension.Overworld, True, False)
    IronAxe = _block("iron_axe", Dimension.Overworld, True, False)
    GoldenAxe = _block("golden_axe", Dimension.Overworld, True, False)
    DiamondAxe = _block("diamond_axe", Dimension.Overworld, True, False)
    NetheriteAxe = _block("netherite_axe", Dimension.Nether, True, False)
    WoodenPickaxe = _block("wooden_pickaxe", Dimension.Overworld, True, False)
    StonePickaxe = _block("stone_pickaxe", Dimension.Overworld, True, False)
    IronPickaxe = _block("iron_pickaxe", Dimension.Overworld, True, False)
    GoldenPickaxe = _block("golden_pickaxe", Dimension.Overworld, True, False)
    DiamondPickaxe = _block(
        "diamond_pickaxe", Dimension.Overworld, True, False)
    NetheritePickaxe = _block(
        "netherite_pickaxe", Dimension.Nether, True, False)
    WoodenShovel = _block("wooden_shovel", Dimension.Overworld, True, False)
    StoneShovel = _block("stone_shovel", Dimension.Overworld, True, False)
    IronShovel = _block("iron_shovel", Dimension.Overworld, True, False)
    GoldenShovel = _block("golden_shovel", Dimension.Overworld, True, False)
    DiamondShovel = _block("diamond_shovel", Dimension.Overworld, True, False)
    NetheriteShovel = _block("netherite_shovel", Dimension.Nether, True, False)
    WoodenHoe = _block("wooden_hoe", Dimension.Overworld, True, False)
    StoneHoe = _block("stone_hoe", Dimension.Overworld, True, False)
    IronHoe = _block("iron_hoe", Dimension.Overworld, True, False)
    GoldenHoe = _block("golden_hoe", Dimension.Overworld, True, False)
    DiamondHoe = _block("diamond_hoe", Dimension.Overworld, True, False)
    NetheriteHoe = _block("netherite_hoe", Dimension.Nether, True, False)
    Bow = _block("bow", Dimension.Overworld, True, False)
    Crossbow = _block("crossbow", Dimension.Overworld, True, False)
    Arrow = _block("arrow", Dimension.Overworld, True, False,
                   _state("variant", ["arrow", "night_vision_arrow_0_22", "night_vision_arrow_1", "invisibility_arrow_0_22", "invisibility_arrow_1", "leaping_arrow_0_22", "leaping_arrow_1", "leaping_2_arrow_1", "fire_resistance_arrow_0_22", "fire_resistance_arrow_1", "speed_arrow_0_22", "speed_arrow_1", "speed_2_arrow_1", "slowness_arrow_0_22", "slowness_arrow_1", "water_breathing_arrow_0_22", "water_breathing_arrow_1", "healing_arrow_1", "healing_arrow_2", "harming_arrow_1", "harming_arrow_2", "poison_arrow_0_05", "poison_arrow_0_15", "poison_2_arrow_0_02", "regeneration_arrow_0_05", "regeneration_arrow_0_15", "regeneration_2_arrow_0_02", "strength_arrow_0_22", "strength_arrow_1", "strength_2_arrow_0_11", "weakness_arrow_0_11", "weakness_arrow_0_30", "decay_arrow_0_05", "turtle_master_arrow_0_02", "turtle_master_arrow_0_05", "turtle_master_2_arrow_0_02", "slow_falling_arrow_0_11", "slow_falling_arrow_0_30", "slowness_arrow_0_02", ]))
    Shield = _block("shield", Dimension.Overworld, True, False)
    CookedChicken = _block("cooked_chicken", Dimension.Overworld, True, False)
    CookedPorkchop = _block(
        "cooked_porkchop", Dimension.Overworld, True, False)
    CookedBeef = _block("cooked_beef", Dimension.Overworld, True, False)
    CookedMutton = _block("cooked_mutton", Dimension.Overworld, True, False)
    CookedRabbit = _block("cooked_rabbit", Dimension.Overworld, True, False)
    CookedCod = _block("cooked_cod", Dimension.Overworld, True, False)
    CookedSalmon = _block("cooked_salmon", Dimension.Overworld, True, False)
    Bread = _block("bread", Dimension.Overworld, True, False)
    MushroomStew = _block("mushroom_stew", Dimension.Overworld, True, False)
    BeetrootSoup = _block("beetroot_soup", Dimension.Overworld, True, False)
    RabbitStew = _block("rabbit_stew", Dimension.Overworld, True, False)
    BakedPotato = _block("baked_potato", Dimension.Overworld, True, False)
    Cookie = _block("cookie", Dimension.Overworld, True, False)
    PumpkinPie = _block("pumpkin_pie", Dimension.Overworld, True, False)
    Cake = _block("cake", Dimension.Overworld, True, False)
    DriedKelp = _block("dried_kelp", Dimension.Overworld, True, False)
    FishingRod = _block("fishing_rod", Dimension.Overworld, True, False)
    CarrotOnAStick = _block("carrot_on_a_stick",
                            Dimension.Overworld, True, False)
    WarpedFungusOnAStick = _block(
        "warped_fungus_on_a_stick", Dimension.Nether, True, False)
    Snowball = _block("snowball", Dimension.Overworld, True, False)
    Shears = _block("shears", Dimension.Overworld, True, False)
    FlintAndSteel = _block("flint_and_steel", Dimension.Overworld, True, False)
    Lead = _block("lead", Dimension.Overworld, True, False)
    Clock = _block("clock", Dimension.Overworld, True, False)
    Compass = _block("compass", Dimension.Overworld, True, False)
    RecoveryCompass = _block(
        "recovery_compass", Dimension.Overworld, True, False)
    EmptyMap = _block("empty_map", Dimension.Overworld, True, False,
                      _state("variant", ["map", "locator_map", ]))
    Saddle = _block("saddle", Dimension.Overworld, True, False)
    GoatHorn = _block("goat_horn", Dimension.Overworld, True, False,
                      _state("variant", ["goat_horn_ponder", "goat_horn_sing", "goat_horn_seek", "goat_horn_feel", "goat_horn_admire", "goat_horn_call", "goat_horn_yearn", "goat_horn_resist", ]))
    LeatherHorseArmor = _block(
        "leather_horse_armor", Dimension.Overworld, True, False)
    IronHorseArmor = _block(
        "iron_horse_armor", Dimension.Overworld, True, False)
    GoldenHorseArmor = _block("golden_horse_armor",
                              Dimension.Overworld, True, False)
    DiamondHorseArmor = _block(
        "diamond_horse_armor", Dimension.Overworld, True, False)
    Trident = _block("trident", Dimension.Overworld, True, False)
    TurtleHelmet = _block("turtle_helmet", Dimension.Overworld, True, False)
    Elytra = _block("elytra", Dimension.Overworld, True, False)
    TotemOfUndying = _block(
        "totem_of_undying", Dimension.Overworld, True, False)
    GlassBottle = _block("glass_bottle", Dimension.Overworld, True, False)
    ExperienceBottle = _block(
        "experience_bottle", Dimension.Overworld, True, False)
    Potion = _block("potion", Dimension.Overworld, True, False,
                    _state("variant", ["water_bottle", "mundane_potion", "long_mundane_potion", "thick_potion", "awkward_potion", "night_vision_potion_3", "night_vision_potion_8", "invisibility_potion_3", "invisibility_potion_8", "leaping_potion_3", "leaping_potion_8", "leaping_potion_1_3", "fire_resistance_potion_3", "fire_resistance_potion_8", "swiftness_potion_3", "swiftness_potion_8", "swiftness_potion_1_3", "slowness_potion_1_3", "slowness_potion_4", "water_breathing_potion_3", "water_breathing_potion_8", "healing_potion_1", "healing_potion_2", "harming_potion_1", "harming_potion_2", "poison_potion_0_45", "poison_potion_2", "poison_potion_0_22", "regeneration_potion_0_45", "regeneration_potion_2", "regeneration_potion_0_22", "strength_potion_3", "strength_potion_8", "strength_potion_1_3", "weakness_potion_1_3", "weakness_potion_4", "decay_potion", "turtle_master_potion_0_2", "turtle_master_potion_0_4", "turtle_master_2_potion_0_2", "slow_falling_potion_1_3", "slow_falling_potion_4", "slowness_potion_0_2", ]))
    SplashPotion = _block("splash_potion", Dimension.Overworld, True, False,
                          _state("variant", ["splash_water_bottle", "splash_mundane_potion", "splash_long_mundane_potion", "splash_thick_potion", "splash_awkward_potion", "splash_night_vision_potion_3", "splash_night_vision_potion_8", "splash_invisibility_potion_3", "splash_invisibility_potion_8", "splash_leaping_potion_3", "splash_leaping_potion_8", "splash_leaping_potion_1_3", "splash_fire_resistance_potion_3", "splash_fire_resistance_potion_8", "splash_swiftness_potion_3", "splash_swiftness_potion_8", "splash_swiftness_potion_1_3", "splash_slowness_potion_1_3", "splash_slowness_potion_4", "splash_water_breathing_potion_3", "splash_water_breathing_potion_8", "splash_healing_potion_1", "splash_healing_potion_2", "splash_harming_potion_1", "splash_harming_potion_2", "splash_poison_potion_0_45", "splash_poison_potion_2", "splash_poison_potion_0_22", "splash_regeneration_potion_0_45", "splash_regeneration_potion_2", "splash_regeneration_potion_0_22", "splash_strength_potion_3", "splash_strength_potion_8", "splash_strength_potion_1_3", "splash_weakness_potion_1_3", "splash_weakness_potion_4", "splash_decay_potion", "splash_turtle_master_potion_0_2", "splash_turtle_master_potion_0_4", "splash_turtle_master_2_potion_0_2", "splash_slow_falling_potion_1_3", "splash_slow_falling_potion_4", "splash_slowness_potion_0_2", ]))
    LingeringPotion = _block("lingering_potion", Dimension.Overworld, True, False,
                             _state("variant", ["lingering_water_bottle", "lingering_mundane_potion", "lingering_long_mundane_potion", "lingering_thick_potion", "lingering_awkward_potion", "lingering_night_vision_potion_3", "lingering_night_vision_potion_8", "lingering_invisibility_potion_3", "lingering_invisibility_potion_8", "lingering_leaping_potion_3", "lingering_leaping_potion_8", "lingering_leaping_potion_1_3", "lingering_fire_resistance_potion_3", "lingering_fire_resistance_potion_8", "lingering_swiftness_potion_3", "lingering_swiftness_potion_8", "lingering_swiftness_potion_1_3", "lingering_slowness_potion_1_3", "lingering_slowness_potion_4", "lingering_water_breathing_potion_3", "lingering_water_breathing_potion_8", "lingering_healing_potion_1", "lingering_healing_potion_2", "lingering_harming_potion_1", "lingering_harming_potion_2", "lingering_poison_potion_0_45", "lingering_poison_potion_2", "lingering_poison_potion_0_22", "lingering_regeneration_potion_0_45", "lingering_regeneration_potion_2", "lingering_regeneration_potion_0_22", "lingering_strength_potion_3", "lingering_strength_potion_8", "lingering_strength_potion_1_3", "lingering_weakness_potion_1_3", "lingering_weakness_potion_4", "lingering_decay_potion", "lingering_turtle_master_potion_0_2", "lingering_turtle_master_potion_0_4", "lingering_turtle_master_2_potion_0_2", "lingering_slow_falling_potion_1_3", "lingering_slow_falling_potion_4", "lingering_slowness_potion_0_2", ]))
    Spyglass = _block("spyglass", Dimension.Overworld, True, False)
    Stick = _block("stick", Dimension.Overworld, True, False)
    Bed = _block("bed", Dimension.Overworld, True, False,
                 _state("variant", ["white_bed", "light_gray_bed", "gray_bed", "black_bed", "brown_bed", "red_bed", "orange_bed", "yellow_bed", "lime_bed", "green_bed", "cyan_bed", "light_blue_bed", "blue_bed", "purple_bed", "magenta_bed", "pink_bed", ]))
    Torch = _block("torch", Dimension.Overworld, True, False)
    SoulTorch = _block("soul_torch", Dimension.Nether, True, False)
    SeaPickle = _block("sea_pickle", Dimension.Overworld, True, False)
    Lantern = _block("lantern", Dimension.Overworld, True, False)
    SoulLantern = _block("soul_lantern", Dimension.Nether, True, False)
    Candle = _block("candle", Dimension.Overworld, True, False)
    WhiteCandle = _block("white_candle", Dimension.Overworld, True, False)
    OrangeCandle = _block("orange_candle", Dimension.Overworld, True, False)
    MagentaCandle = _block("magenta_candle", Dimension.Overworld, True, False)
    LightBlueCandle = _block(
        "light_blue_candle", Dimension.Overworld, True, False)
    YellowCandle = _block("yellow_candle", Dimension.Overworld, True, False)
    LimeCandle = _block("lime_candle", Dimension.Overworld, True, False)
    PinkCandle = _block("pink_candle", Dimension.Overworld, True, False)
    GrayCandle = _block("gray_candle", Dimension.Overworld, True, False)
    LightGrayCandle = _block(
        "light_gray_candle", Dimension.Overworld, True, False)
    CyanCandle = _block("cyan_candle", Dimension.Overworld, True, False)
    PurpleCandle = _block("purple_candle", Dimension.Overworld, True, False)
    BlueCandle = _block("blue_candle", Dimension.Overworld, True, False)
    BrownCandle = _block("brown_candle", Dimension.Overworld, True, False)
    GreenCandle = _block("green_candle", Dimension.Overworld, True, False)
    RedCandle = _block("red_candle", Dimension.Overworld, True, False)
    BlackCandle = _block("black_candle", Dimension.Overworld, True, False)
    CraftingTable = _block("crafting_table", Dimension.Overworld, True, False)
    CartographyTable = _block(
        "cartography_table", Dimension.Overworld, True, False)
    FletchingTable = _block(
        "fletching_table", Dimension.Overworld, True, False)
    SmithingTable = _block("smithing_table", Dimension.Overworld, True, False)
    Beehive = _block("beehive", Dimension.Overworld, True, False)
    Campfire = _block("campfire", Dimension.Overworld, True, False)
    SoulCampfire = _block("soul_campfire", Dimension.Nether, True, False)
    Furnace = _block("furnace", Dimension.Overworld, True, False)
    BlastFurnace = _block("blast_furnace", Dimension.Overworld, True, False)
    Smoker = _block("smoker", Dimension.Overworld, True, False)
    RespawnAnchor = _block("respawn_anchor", Dimension.Nether, True, False)
    BrewingStand = _block("brewing_stand", Dimension.Overworld, True, False)
    Anvil = _block("anvil", Dimension.Overworld, True, False,
                   _state("variant", ["anvil", "slighlty_damaged_anvil", "very_damaged_anvil", ]))
    Grindstone = _block("grindstone", Dimension.Overworld, True, False)
    EnchantingTable = _block(
        "enchanting_table", Dimension.Overworld, True, False)
    Bookshelf = _block("bookshelf", Dimension.Overworld, True, False)
    Lectern = _block("lectern", Dimension.Overworld, True, False)
    Cauldron = _block("cauldron", Dimension.Overworld, True, False)
    Composter = _block("composter", Dimension.Overworld, True, False)
    Chest = _block("chest", Dimension.Overworld, True, False)
    TrappedChest = _block("trapped_chest", Dimension.Overworld, True, False)
    EnderChest = _block("ender_chest",
                        Dimension.End,
                        True,
                        False, )
    Barrel = _block("barrel", Dimension.Overworld, True, False)
    UndyedShulkerBox = _block("undyed_shulker_box",
                              Dimension.Overworld, True, False)
    ShulkerBox = _block("shulker_box", Dimension.Overworld, True, False,
                        _state("variant", ["white_shulker_box", "gray_shulker_box", "light_gray_shulker_box", "black_shulker_box", "brown_shulker_box", "red_shulker_box", "orange_shulker_box", "yellow_shulker_box", "lime_shulker_box", "green_shulker_box", "cyan_shulker_box", "light_blue_shulker_box", "blue_shulker_box", "purple_shulker_box", "magenta_shulker_box", "pink_shulker_box", ]))
    ArmorStand = _block("armor_stand", Dimension.Overworld, True, False)
    Noteblock = _block("noteblock", Dimension.Overworld, True, False)
    Jukebox = _block("jukebox", Dimension.Overworld, True, False)
    MusicDisc13 = _block("music_disc_13", Dimension.Overworld, True, False)
    MusicDiscCat = _block("music_disc_cat", Dimension.Overworld, True, False)
    MusicDiscBlocks = _block(
        "music_disc_blocks", Dimension.Overworld, True, False)
    MusicDiscChirp = _block(
        "music_disc_chirp", Dimension.Overworld, True, False)
    MusicDiscFar = _block("music_disc_far", Dimension.Overworld, True, False)
    MusicDiscMall = _block("music_disc_mall", Dimension.Overworld, True, False)
    MusicDiscMellohi = _block("music_disc_mellohi",
                              Dimension.Overworld, True, False)
    MusicDiscStal = _block("music_disc_stal", Dimension.Overworld, True, False)
    MusicDiscStrad = _block(
        "music_disc_strad", Dimension.Overworld, True, False)
    MusicDiscWard = _block("music_disc_ward", Dimension.Overworld, True, False)
    MusicDisc11 = _block("music_disc_11", Dimension.Overworld, True, False)
    MusicDiscWait = _block("music_disc_wait", Dimension.Overworld, True, False)
    MusicDiscOtherside = _block(
        "music_disc_otherside", Dimension.Overworld, True, False)
    MusicDisc5 = _block("music_disc_5", Dimension.Overworld, True, False)
    MusicDiscPigstep = _block("music_disc_pigstep",
                              Dimension.Overworld, True, False)
    DiscFragment5 = _block("disc_fragment_5", Dimension.Overworld, True, False)
    GlowstoneDust = _block("glowstone_dust", Dimension.Nether, True, False)
    Glowstone = _block("glowstone", Dimension.Nether, True, False)
    RedstoneLamp = _block("redstone_lamp", Dimension.Overworld, True, False)
    SeaLantern = _block("sea_lantern", Dimension.Overworld, True, False)
    OakSign = _block("oak_sign", Dimension.Overworld, True, False)
    SpruceSign = _block("spruce_sign", Dimension.Overworld, True, False)
    BirchSign = _block("birch_sign", Dimension.Overworld, True, False)
    JungleSign = _block("jungle_sign", Dimension.Overworld, True, False)
    AcaciaSign = _block("acacia_sign", Dimension.Overworld, True, False)
    DarkOakSign = _block("dark_oak_sign", Dimension.Overworld, True, False)
    MangroveSign = _block("mangrove_sign", Dimension.Overworld, True, False)
    CrimsonSign = _block("crimson_sign", Dimension.Nether, True, False)
    WarpedSign = _block("warped_sign", Dimension.Nether, True, False)
    Painting = _block("painting", Dimension.Overworld, True, False)
    Frame = _block("frame", Dimension.Overworld, True, False)
    GlowFrame = _block("glow_frame", Dimension.Overworld, True, False)
    HoneyBottle = _block("honey_bottle", Dimension.Overworld, True, False)
    FlowerPot = _block("flower_pot", Dimension.Overworld, True, False)
    Bowl = _block("bowl", Dimension.Overworld, True, False)
    Bucket = _block("bucket", Dimension.Overworld, True, False)
    MilkBucket = _block("milk_bucket", Dimension.Overworld, True, False)
    WaterBucket = _block("water_bucket", Dimension.Overworld, True, False)
    LavaBucket = _block("lava_bucket", Dimension.Overworld, True, False)
    CodBucket = _block("cod_bucket", Dimension.Overworld, True, False)
    SalmonBucket = _block("salmon_bucket", Dimension.Overworld, True, False)
    TropicalFishBucket = _block(
        "tropical_fish_bucket", Dimension.Overworld, True, False)
    PufferfishBucket = _block(
        "pufferfish_bucket", Dimension.Overworld, True, False)
    PowderSnowBucket = _block("powder_snow_bucket",
                              Dimension.Overworld, True, False)
    AxolotlBucket = _block("axolotl_bucket", Dimension.Overworld, True, False)
    TadpoleBucket = _block("tadpole_bucket", Dimension.Overworld, True, False)
    Skull = _block("skull", Dimension.Overworld, True, False,
                   _state("variant", ["player_head", "zombie_head", "creeper_head", "dragon_head", "skeleton_skull", "wither_skeleton_skull", ]))
    Beacon = _block("beacon", Dimension.Overworld, True, False)
    Bell = _block("bell", Dimension.Overworld, True, False)
    Conduit = _block("conduit", Dimension.Overworld, True, False)
    StonecutterBlock = _block(
        "stonecutter_block", Dimension.Overworld, True, False)
    EndPortalFrame = _block("end_portal_frame",
                            Dimension.End,
                            True,
                            False, )
    Coal = _block("coal", Dimension.Overworld, True, False)
    Charcoal = _block("charcoal", Dimension.Overworld, True, False)
    Diamond = _block("diamond", Dimension.Overworld, True, False)
    IronNugget = _block("iron_nugget", Dimension.Overworld, True, False)
    RawIron = _block("raw_iron", Dimension.Overworld, True, False)
    RawGold = _block("raw_gold", Dimension.Overworld, True, False)
    RawCopper = _block("raw_copper", Dimension.Overworld, True, False)
    CopperIngot = _block("copper_ingot", Dimension.Overworld, True, False)
    IronIngot = _block("iron_ingot", Dimension.Overworld, True, False)
    NetheriteScrap = _block("netherite_scrap", Dimension.Nether, True, False)
    NetheriteIngot = _block("netherite_ingot", Dimension.Nether, True, False)
    GoldNugget = _block("gold_nugget", Dimension.Overworld, True, False)
    GoldIngot = _block("gold_ingot", Dimension.Overworld, True, False)
    Emerald = _block("emerald", Dimension.Overworld, True, False)
    Quartz = _block("quartz", Dimension.Nether, True, False)
    ClayBall = _block("clay_ball", Dimension.Overworld, True, False)
    Brick = _block("brick", Dimension.Overworld, True, False)
    Netherbrick = _block("netherbrick", Dimension.Nether, True, False)
    PrismarineShard = _block(
        "prismarine_shard", Dimension.Overworld, True, False)
    AmethystShard = _block("amethyst_shard", Dimension.Overworld, True, False)
    PrismarineCrystals = _block(
        "prismarine_crystals", Dimension.Overworld, True, False)
    NautilusShell = _block("nautilus_shell", Dimension.Overworld, True, False)
    HeartOfTheSea = _block(
        "heart_of_the_sea", Dimension.Overworld, True, False)
    Scute = _block("scute", Dimension.Overworld, True, False)
    PhantomMembrane = _block(
        "phantom_membrane", Dimension.Overworld, True, False)
    String = _block("string", Dimension.Overworld, True, False)
    Feather = _block("feather", Dimension.Overworld, True, False)
    Flint = _block("flint", Dimension.Overworld, True, False)
    Gunpowder = _block("gunpowder", Dimension.Overworld, True, False)
    Leather = _block("leather", Dimension.Overworld, True, False)
    RabbitHide = _block("rabbit_hide", Dimension.Overworld, True, False)
    RabbitFoot = _block("rabbit_foot", Dimension.Overworld, True, False)
    FireCharge = _block("fire_charge", Dimension.Overworld, True, False)
    BlazeRod = _block("blaze_rod", Dimension.Overworld, True, False)
    BlazePowder = _block("blaze_powder", Dimension.Overworld, True, False)
    MagmaCream = _block("magma_cream", Dimension.Nether, True, False)
    FermentedSpiderEye = _block(
        "fermented_spider_eye", Dimension.Overworld, True, False)
    EchoShard = _block("echo_shard", Dimension.Overworld, True, False)
    DragonBreath = _block("dragon_breath",
                          Dimension.End,
                          True,
                          False, )
    ShulkerShell = _block("shulker_shell", Dimension.Overworld, True, False)
    GhastTear = _block("ghast_tear", Dimension.Overworld, True, False)
    SlimeBall = _block("slime_ball", Dimension.Overworld, True, False)
    EnderPearl = _block("ender_pearl",
                        Dimension.End,
                        True,
                        False, )
    EnderEye = _block("ender_eye",
                      Dimension.End,
                      True,
                      False, )
    NetherStar = _block("nether_star", Dimension.Nether, True, False)
    EndRod = _block("end_rod",
                    Dimension.End,
                    True,
                    False, )
    LightningRod = _block("lightning_rod", Dimension.Overworld, True, False)
    EndCrystal = _block("end_crystal",
                        Dimension.End,
                        True,
                        False, )
    Paper = _block("paper", Dimension.Overworld, True, False)
    Book = _block("book", Dimension.Overworld, True, False)
    WritableBook = _block("writable_book", Dimension.Overworld, True, False)
    WrittenBook = _block("written_book", Dimension.Overworld, True, False)
    EnchantedBook = _block("enchanted_book", Dimension.Overworld, True, False)
    OakBoat = _block("oak_boat", Dimension.Overworld, True, False)
    SpruceBoat = _block("spruce_boat", Dimension.Overworld, True, False)
    BirchBoat = _block("birch_boat", Dimension.Overworld, True, False)
    JungleBoat = _block("jungle_boat", Dimension.Overworld, True, False)
    AcaciaBoat = _block("acacia_boat", Dimension.Overworld, True, False)
    DarkOakBoat = _block("dark_oak_boat", Dimension.Overworld, True, False)
    MangroveBoat = _block("mangrove_boat", Dimension.Overworld, True, False)
    OakChestBoat = _block("oak_chest_boat", Dimension.Overworld, True, False)
    SpruceChestBoat = _block(
        "spruce_chest_boat", Dimension.Overworld, True, False)
    BirchChestBoat = _block(
        "birch_chest_boat", Dimension.Overworld, True, False)
    JungleChestBoat = _block(
        "jungle_chest_boat", Dimension.Overworld, True, False)
    AcaciaChestBoat = _block(
        "acacia_chest_boat", Dimension.Overworld, True, False)
    DarkOakChestBoat = _block("dark_oak_chest_boat",
                              Dimension.Overworld, True, False)
    MangroveChestBoat = _block(
        "mangrove_chest_boat", Dimension.Overworld, True, False)
    Rail = _block("rail", Dimension.Overworld, True, False)
    GoldenRail = _block("golden_rail", Dimension.Overworld, True, False)
    DetectorRail = _block("detector_rail", Dimension.Overworld, True, False)
    ActivatorRail = _block("activator_rail", Dimension.Overworld, True, False)
    Minecart = _block("minecart", Dimension.Overworld, True, False)
    ChestMinecart = _block("chest_minecart", Dimension.Overworld, True, False)
    HopperMinecart = _block(
        "hopper_minecart", Dimension.Overworld, True, False)
    TntMinecart = _block("tnt_minecart", Dimension.Overworld, True, False)
    RedstoneBlock = _block("redstone_block", Dimension.Overworld, True, False)
    RedstoneTorch = _block("redstone_torch", Dimension.Overworld, True, False)
    Lever = _block("lever", Dimension.Overworld, True, False)
    WoodenButton = _block("wooden_button", Dimension.Overworld, True, False)
    SpruceButton = _block("spruce_button", Dimension.Overworld, True, False)
    BirchButton = _block("birch_button", Dimension.Overworld, True, False)
    JungleButton = _block("jungle_button", Dimension.Overworld, True, False)
    AcaciaButton = _block("acacia_button", Dimension.Overworld, True, False)
    DarkOakButton = _block("dark_oak_button", Dimension.Overworld, True, False)
    MangroveButton = _block(
        "mangrove_button", Dimension.Overworld, True, False)
    StoneButton = _block("stone_button", Dimension.Overworld, True, False)
    CrimsonButton = _block("crimson_button", Dimension.Nether, True, False)
    WarpedButton = _block("warped_button", Dimension.Nether, True, False)
    PolishedBlackstoneButton = _block(
        "polished_blackstone_button", Dimension.Nether, True, False)
    TripwireHook = _block("tripwire_hook", Dimension.Overworld, True, False)
    WoodenPressurePlate = _block(
        "wooden_pressure_plate", Dimension.Overworld, True, False)
    SprucePressurePlate = _block(
        "spruce_pressure_plate", Dimension.Overworld, True, False)
    BirchPressurePlate = _block(
        "birch_pressure_plate", Dimension.Overworld, True, False)
    JunglePressurePlate = _block(
        "jungle_pressure_plate", Dimension.Overworld, True, False)
    AcaciaPressurePlate = _block(
        "acacia_pressure_plate", Dimension.Overworld, True, False)
    DarkOakPressurePlate = _block(
        "dark_oak_pressure_plate", Dimension.Overworld, True, False)
    MangrovePressurePlate = _block(
        "mangrove_pressure_plate", Dimension.Overworld, True, False)
    CrimsonPressurePlate = _block(
        "crimson_pressure_plate", Dimension.Nether, True, False)
    WarpedPressurePlate = _block(
        "warped_pressure_plate", Dimension.Nether, True, False)
    StonePressurePlate = _block(
        "stone_pressure_plate", Dimension.Overworld, True, False)
    LightWeightedPressurePlate = _block(
        "light_weighted_pressure_plate", Dimension.Overworld, True, False)
    HeavyWeightedPressurePlate = _block(
        "heavy_weighted_pressure_plate", Dimension.Overworld, True, False)
    PolishedBlackstonePressurePlate = _block(
        "polished_blackstone_pressure_plate", Dimension.Nether, True, False)
    Observer = _block("observer", Dimension.Overworld, True, False)
    DaylightDetector = _block(
        "daylight_detector", Dimension.Overworld, True, False)
    Repeater = _block("repeater", Dimension.Overworld, True, False)
    Comparator = _block("comparator", Dimension.Overworld, True, False)
    Hopper = _block("hopper", Dimension.Overworld, True, False)
    Dropper = _block("dropper", Dimension.Overworld, True, False)
    Dispenser = _block("dispenser", Dimension.Overworld, True, False)
    Piston = _block("piston", Dimension.Overworld, True, False)
    StickyPiston = _block("sticky_piston", Dimension.Overworld, True, False)
    Tnt = _block("tnt", Dimension.Overworld, True, False)
    NameTag = _block("name_tag", Dimension.Overworld, True, False)
    Loom = _block("loom", Dimension.Overworld, True, False)
    Banner = _block("banner", Dimension.Overworld, True, False,
                    _state("variant", ["black_banner", "gray_banner", "light_gray_banner", "white_banner", "light_blue_banner", "orange_banner", "red_banner", "blue_banner", "purple_banner", "magenta_banner", "pink_banner", "brown_banner", "yellow_banner", "lime_banner", "green_banner", "cyan_banner", "illager_banner", ]))
    BordureIndentedBannerPattern = _block(
        "bordure_indented_banner_pattern", Dimension.Overworld, True, False)
    CreeperBannerPattern = _block(
        "creeper_banner_pattern", Dimension.Overworld, True, False)
    FieldMasonedBannerPattern = _block(
        "field_masoned_banner_pattern", Dimension.Overworld, True, False)
    FlowerBannerPattern = _block(
        "flower_banner_pattern", Dimension.Overworld, True, False)
    BannerPattern = _block("banner_pattern", Dimension.Overworld, True, False)
    MojangBannerPattern = _block(
        "mojang_banner_pattern", Dimension.Overworld, True, False)
    PiglinBannerPattern = _block(
        "piglin_banner_pattern", Dimension.Overworld, True, False)
    SkullBannerPattern = _block(
        "skull_banner_pattern", Dimension.Overworld, True, False)
    FireworkRocket = _block(
        "firework_rocket", Dimension.Overworld, True, False)
    FireworkStar = _block("firework_star", Dimension.Overworld, True, False)
    Chain = _block("chain", Dimension.Nether, True, False)
    Target = _block("target", Dimension.Overworld, True, False)
    Air = _block("air", Dimension.Overworld, True, True)
    Allow = _block("allow", Dimension.Overworld, True, True)
    Barrier = _block("barrier", Dimension.Overworld, True, True)
    CommandBlock = _block("command_block", Dimension.Overworld, True, True)
    ChainCommandBlock = _block(
        "chain_command_block", Dimension.Overworld, True, True)
    RepeatingCommandBlock = _block(
        "repeating_command_block", Dimension.Overworld, True, True)
    CommandBlockMinecart = _block(
        "command_block_minecart", Dimension.Overworld, True, True)
    StructureBlock = _block("structure_block", Dimension.Overworld, True, True)
    StructureVoid = _block("structure_void", Dimension.Overworld, True, True)
    Jigsaw = _block("jigsaw", Dimension.Overworld, True, True)
    LightBlock = _block("light_block", Dimension.Overworld, True, True)
    SuspiciousStew = _block("suspicious_stew", Dimension.Overworld, True, True)
    FilledMap = _block("filled_map", Dimension.Overworld, True, True)
    FrostedIce = _block("frosted_ice", Dimension.Overworld, True, True)
    Portal = _block("portal", Dimension.Nether, True, True)
    EndPortal = _block("end_portal",
                       Dimension.End,
                       True,
                       True, )
    EndGateway = _block("end_gateway",
                        Dimension.End,
                        True,
                        True, )

    Blocks = [CherryBoat, CherryButton, CherryChestBoat, CherryDoor, CherryFence, CherryFenceGate, CherryHangingSign, CherryLeaves, CherryLog, CherryPlanks, CherryPressurePlate, CherrySapling, CherrySign, CherrySlab, CherryStairs, 
              CherryTrapdoor, CherryWood, StrippedCherryLog, StrippedCherryWood, PinkPetals, Brush, DecoratedPot, ArmsUpPotteryShard, SkullPotteryShard, PrizePotteryShard, ArcherPotteryShard, SuspiciousSand, Tourchflower, 
              TourchflowerSeeds, BambooBlock, StrippedBambooBlock, BambooPlanks, BambooMosaic, BambooFence, BambooFenceGate, BambooStairs, BambooDoor, BambooTrapdoor, BambooSlab, BambooMosaicSlab, BambooMosaicStairs, BambooBoat, 
              BambooChestBoat, BambooButton, BambooPressurePlate, BambooSign, CamelSpawnEgg, ChiseledBookshelf, BambooHangingSign, MangroveHangingSign, WarpedHangingSign, CrimsonHangingSign, DarkOakHangingSign, AcaciaHangingSign, 
              JungleHangingSign, BirchHangingSign, SpruceHangingSign, OakHangingSign, Planks, MangrovePlanks, CrimsonPlanks, WarpedPlanks, CobblestoneWall, BlackstoneWall, PolishedBlackstoneWall, PolishedBlackstoneBrickWall, 
              CobbledDeepslateWall, DeepslateTileWall, PolishedDeepslateWall, DeepslateBrickWall, MudBrickWall, Fence, MangroveFence, NetherBrickFence, CrimsonFence, WarpedFence, FenceGate, SpruceFenceGate, BirchFenceGate, 
              JungleFenceGate, AcaciaFenceGate, DarkOakFenceGate, MangroveFenceGate, CrimsonFenceGate, WarpedFenceGate, NormalStoneStairs, StoneStairs, MossyCobblestoneStairs, OakStairs, SpruceStairs, BirchStairs, JungleStairs, 
              AcaciaStairs, DarkOakStairs, MangroveStairs, StoneBrickStairs, MossyStoneBrickStairs, SandstoneStairs, SmoothSandstoneStairs, RedSandstoneStairs, SmoothRedSandstoneStairs, GraniteStairs, PolishedGraniteStairs, 
              DioriteStairs, PolishedDioriteStairs, AndesiteStairs, PolishedAndesiteStairs, BrickStairs, NetherBrickStairs, RedNetherBrickStairs, EndBrickStairs, QuartzStairs, SmoothQuartzStairs, PurpurStairs, PrismarineStairs, 
              DarkPrismarineStairs, PrismarineBricksStairs, CrimsonStairs, WarpedStairs, BlackstoneStairs, PolishedBlackstoneStairs, PolishedBlackstoneBrickStairs, CutCopperStairs, ExposedCutCopperStairs, WeatheredCutCopperStairs, 
              OxidizedCutCopperStairs, WaxedCutCopperStairs, WaxedExposedCutCopperStairs, WaxedWeatheredCutCopperStairs, WaxedOxidizedCutCopperStairs, CobbledDeepslateStairs, DeepslateTileStairs, PolishedDeepslateStairs, 
              DeepslateBrickStairs, MudBrickStairs, WoodenDoor, SpruceDoor, BirchDoor, JungleDoor, AcaciaDoor, DarkOakDoor, MangroveDoor, IronDoor, CrimsonDoor, WarpedDoor, Trapdoor, SpruceTrapdoor, BirchTrapdoor, JungleTrapdoor, 
              AcaciaTrapdoor, DarkOakTrapdoor, MangroveTrapdoor, IronTrapdoor, CrimsonTrapdoor, WarpedTrapdoor, IronBars, Glass, StainedGlass, TintedGlass, GlassPane, StainedGlassPane, Ladder, Scaffolding, StoneSlab4, StoneSlab, 
              StoneSlab2, WoodenSlab, MangroveSlab, StoneSlab3, CrimsonSlab, WarpedSlab, BlackstoneSlab, PolishedBlackstoneSlab, PolishedBlackstoneBrickSlab, CutCopperSlab, ExposedCutCopperSlab, WeatheredCutCopperSlab, 
              OxidizedCutCopperSlab, WaxedCutCopperSlab, WaxedExposedCutCopperSlab, WaxedWeatheredCutCopperSlab, WaxedOxidizedCutCopperSlab, CobbledDeepslateSlab, PolishedDeepslateSlab, DeepslateTileSlab, DeepslateBrickSlab, 
              MudBrickSlab, BrickBlock, ChiseledNetherBricks, CrackedNetherBricks, QuartzBricks, Stonebrick, EndBricks, Prismarine, PolishedBlackstoneBricks, CrackedPolishedBlackstoneBricks, GildedBlackstone, ChiseledPolishedBlackstone, 
              DeepslateTiles, CrackedDeepslateTiles, DeepslateBricks, CrackedDeepslateBricks, ChiseledDeepslate, Cobblestone, MossyCobblestone, CobbledDeepslate, SmoothStone, Sandstone, RedSandstone, CoalBlock, DriedKelpBlock, 
              GoldBlock, IronBlock, CopperBlock, ExposedCopper, WeatheredCopper, OxidizedCopper, WaxedCopper, WaxedExposedCopper, WaxedWeatheredCopper, WaxedOxidizedCopper, CutCopper, ExposedCutCopper, WeatheredCutCopper, 
              OxidizedCutCopper, WaxedCutCopper, WaxedExposedCutCopper, WaxedWeatheredCutCopper, WaxedOxidizedCutCopper, EmeraldBlock, DiamondBlock, LapisBlock, RawIronBlock, RawCopperBlock, RawGoldBlock, QuartzBlock, Slime, 
              HoneyBlock, HoneycombBlock, HayBlock, BoneBlock, NetherBrick, RedNetherBrick, NetheriteBlock, Lodestone, Wool, Carpet, ConcretePowder, Concrete, Clay, HardenedClay, StainedHardenedClay, WhiteGlazedTerracotta, 
              SilverGlazedTerracotta, GrayGlazedTerracotta, BlackGlazedTerracotta, BrownGlazedTerracotta, RedGlazedTerracotta, OrangeGlazedTerracotta, YellowGlazedTerracotta, LimeGlazedTerracotta, GreenGlazedTerracotta, 
              CyanGlazedTerracotta, LightBlueGlazedTerracotta, BlueGlazedTerracotta, PurpleGlazedTerracotta, MagentaGlazedTerracotta, PinkGlazedTerracotta, PurpurBlock, PackedMud, MudBricks, NetherWartBlock, WarpedWartBlock, 
              Shroomlight, CrimsonNylium, WarpedNylium, Basalt, PolishedBasalt, SmoothBasalt, SoulSoil, Dirt, Farmland, Grass, GrassPath, Podzol, Mycelium, Mud, Stone, IronOre, GoldOre, DiamondOre, LapisOre, RedstoneOre, CoalOre, 
              CopperOre, EmeraldOre, QuartzOre, NetherGoldOre, AncientDebris, DeepslateIronOre, DeepslateGoldOre, DeepslateDiamondOre, DeepslateLapisOre, DeepslateRedstoneOre, DeepslateEmeraldOre, DeepslateCoalOre, DeepslateCopperOre, 
              Gravel, Blackstone, Deepslate, PolishedBlackstone, PolishedDeepslate, Sand, Cactus, Log, StrippedOakLog, StrippedSpruceLog, StrippedBirchLog, StrippedJungleLog, Log2, StrippedAcaciaLog, StrippedDarkOakLog, MangroveLog, 
              StrippedMangroveLog, CrimsonStem, StrippedCrimsonStem, WarpedStem, StrippedWarpedStem, Wood, MangroveWood, StrippedMangroveWood, CrimsonHyphae, StrippedCrimsonHyphae, WarpedHyphae, StrippedWarpedHyphae, Leaves, Leaves2, 
              MangroveLeaves, AzaleaLeaves, AzaleaLeavesFlowered, Sapling, MangrovePropagule, BeeNest, WheatSeeds, PumpkinSeeds, MelonSeeds, BeetrootSeeds, Wheat, Beetroot, Potato, PoisonousPotato, Carrot, GoldenCarrot, Apple, 
              GoldenApple, EnchantedGoldenApple, MelonBlock, MelonSlice, GlisteringMelonSlice, SweetBerries, GlowBerries, Pumpkin, CarvedPumpkin, LitPumpkin, Honeycomb, Tallgrass, DoublePlant, NetherSprouts, Coral, CoralFan, 
              CoralFanDead, Kelp, Seagrass, CrimsonRoots, WarpedRoots, YellowFlower, RedFlower, WitherRose, WhiteDye, LightGrayDye, GrayDye, BrownDye, BlackDye, RedDye, OrangeDye, YellowDye, LimeDye, GreenDye, CyanDye, LightBlueDye, 
              BlueDye, PurpleDye, MagentaDye, PinkDye, InkSac, GlowInkSac, CocoaBeans, LapisLazuli, BoneMeal, Vine, WeepingVines, TwistingVines, Waterlily, Deadbush, Bamboo, Snow, Ice, PackedIce, BlueIce, SnowLayer, PointedDripstone, 
              DripstoneBlock, MossCarpet, MossBlock, DirtWithRoots, HangingRoots, MangroveRoots, MuddyMangroveRoots, BigDripleaf, SmallDripleafBlock, SporeBlossom, Azalea, FloweringAzalea,
              GlowLichen, AmethystBlock, BuddingAmethyst, AmethystCluster, LargeAmethystBud, MediumAmethystBud, SmallAmethystBud, Tuff, Calcite, Chicken, Porkchop, Beef, Mutton, Rabbit, Cod, Salmon, TropicalFish, Pufferfish, 
              BrownMushroom, RedMushroom, CrimsonFungus, WarpedFungus, BrownMushroomBlock, RedMushroomBlock, Egg, SugarCane, Sugar, RottenFlesh, Bone, Web, SpiderEye, MobSpawner, MonsterEgg, InfestedDeepslate, DragonEgg, TurtleEgg, 
              FrogSpawn, PearlescentFroglight, VerdantFroglight, OchreFroglight, ChickenSpawnEgg, BeeSpawnEgg, CowSpawnEgg, PigSpawnEgg, SheepSpawnEgg, WolfSpawnEgg, PolarBearSpawnEgg, OcelotSpawnEgg, CatSpawnEgg, MooshroomSpawnEgg, 
              BatSpawnEgg, ParrotSpawnEgg, RabbitSpawnEgg, LlamaSpawnEgg, HorseSpawnEgg, DonkeySpawnEgg, MuleSpawnEgg, SkeletonHorseSpawnEgg, ZombieHorseSpawnEgg, TropicalFishSpawnEgg, CodSpawnEgg, PufferfishSpawnEgg, SalmonSpawnEgg, 
              DolphinSpawnEgg, TurtleSpawnEgg, PandaSpawnEgg, FoxSpawnEgg, CreeperSpawnEgg, EndermanSpawnEgg, SilverfishSpawnEgg, SkeletonSpawnEgg, WitherSkeletonSpawnEgg, StraySpawnEgg, SlimeSpawnEgg, SpiderSpawnEgg, ZombieSpawnEgg, 
              ZombiePigmanSpawnEgg, HuskSpawnEgg, DrownedSpawnEgg, SquidSpawnEgg, GlowSquidSpawnEgg, CaveSpiderSpawnEgg, WitchSpawnEgg, GuardianSpawnEgg, ElderGuardianSpawnEgg, EndermiteSpawnEgg, MagmaCubeSpawnEgg, StriderSpawnEgg, 
              HoglinSpawnEgg, PiglinSpawnEgg, ZoglinSpawnEgg, PiglinBruteSpawnEgg, GoatSpawnEgg, AxolotlSpawnEgg, WardenSpawnEgg, AllaySpawnEgg, FrogSpawnEgg, TadpoleSpawnEgg, GhastSpawnEgg, BlazeSpawnEgg, ShulkerSpawnEgg, 
              VindicatorSpawnEgg, EvokerSpawnEgg, VexSpawnEgg, VillagerSpawnEgg, WanderingTraderSpawnEgg, ZombieVillagerSpawnEgg, PhantomSpawnEgg, PillagerSpawnEgg, RavagerSpawnEgg, Obsidian, CryingObsidian, Bedrock, SoulSand, 
              Netherrack, Magma, NetherWart, EndStone, ChorusFlower, ChorusPlant, ChorusFruit, PoppedChorusFruit, Sponge, CoralBlock, Sculk, SculkVein, SculkCatalyst, SculkShrieker, SculkSensor, ReinforcedDeepslate, LeatherHelmet, 
              ChainmailHelmet, IronHelmet, GoldenHelmet, DiamondHelmet, NetheriteHelmet, LeatherChestplate, ChainmailChestplate, IronChestplate, GoldenChestplate, DiamondChestplate, NetheriteChestplate, LeatherLeggings, 
              ChainmailLeggings, IronLeggings, GoldenLeggings, DiamondLeggings, NetheriteLeggings, LeatherBoots, ChainmailBoots, IronBoots, GoldenBoots, DiamondBoots, NetheriteBoots, WoodenSword, StoneSword, IronSword, GoldenSword, 
              DiamondSword, NetheriteSword, WoodenAxe, StoneAxe, IronAxe, GoldenAxe, DiamondAxe, NetheriteAxe, WoodenPickaxe, StonePickaxe, IronPickaxe, GoldenPickaxe, DiamondPickaxe, NetheritePickaxe, WoodenShovel, StoneShovel, 
              IronShovel, GoldenShovel, DiamondShovel, NetheriteShovel, WoodenHoe, StoneHoe, IronHoe, GoldenHoe, DiamondHoe, NetheriteHoe, Bow, Crossbow, Arrow, Shield, CookedChicken, CookedPorkchop, CookedBeef, CookedMutton, 
              CookedRabbit, CookedCod, CookedSalmon, Bread, MushroomStew, BeetrootSoup, RabbitStew, BakedPotato, Cookie, PumpkinPie, Cake, DriedKelp, FishingRod, CarrotOnAStick, WarpedFungusOnAStick, Snowball, Shears, FlintAndSteel, 
              Lead, Clock, Compass, RecoveryCompass, EmptyMap, Saddle, GoatHorn, LeatherHorseArmor, IronHorseArmor, GoldenHorseArmor, DiamondHorseArmor, Trident, TurtleHelmet, Elytra, TotemOfUndying, GlassBottle, ExperienceBottle, 
              Potion, SplashPotion, LingeringPotion, Spyglass, Stick, Bed, Torch, SoulTorch, SeaPickle, Lantern, SoulLantern, Candle, WhiteCandle, OrangeCandle, MagentaCandle, LightBlueCandle, YellowCandle, LimeCandle, PinkCandle, 
              GrayCandle, LightGrayCandle, CyanCandle, PurpleCandle, BlueCandle, BrownCandle, GreenCandle, RedCandle, BlackCandle, CraftingTable, CartographyTable, FletchingTable, SmithingTable, Beehive, Campfire, SoulCampfire, 
              Furnace, BlastFurnace, Smoker, RespawnAnchor, BrewingStand, Anvil, Grindstone, EnchantingTable, Bookshelf, Lectern, Cauldron, Composter, Chest, TrappedChest, EnderChest, Barrel, UndyedShulkerBox, ShulkerBox, ArmorStand, 
              Noteblock, Jukebox, MusicDisc13, MusicDiscCat, MusicDiscBlocks, MusicDiscChirp, MusicDiscFar, MusicDiscMall, MusicDiscMellohi, MusicDiscStal, MusicDiscStrad, MusicDiscWard, MusicDisc11, MusicDiscWait, MusicDiscOtherside, 
              MusicDisc5, MusicDiscPigstep, DiscFragment5, GlowstoneDust, Glowstone, RedstoneLamp, SeaLantern, OakSign, SpruceSign, BirchSign, JungleSign, AcaciaSign, DarkOakSign, MangroveSign, CrimsonSign, WarpedSign, Painting, Frame, 
              GlowFrame, HoneyBottle, FlowerPot, Bowl, Bucket, MilkBucket, WaterBucket, LavaBucket, CodBucket, SalmonBucket, TropicalFishBucket, PufferfishBucket, PowderSnowBucket, AxolotlBucket, TadpoleBucket, Skull, Beacon, Bell, 
              Conduit, StonecutterBlock, EndPortalFrame, Coal, Charcoal, Diamond, IronNugget, RawIron, RawGold, RawCopper, CopperIngot, IronIngot, NetheriteScrap, NetheriteIngot, GoldNugget, GoldIngot, Emerald, Quartz, ClayBall, Brick, 
              Netherbrick, PrismarineShard, AmethystShard, PrismarineCrystals, NautilusShell, HeartOfTheSea, Scute, PhantomMembrane, String, Feather, Flint, Gunpowder, Leather, RabbitHide, RabbitFoot, FireCharge, BlazeRod, BlazePowder, 
              MagmaCream, FermentedSpiderEye, EchoShard, DragonBreath, ShulkerShell, GhastTear, SlimeBall, EnderPearl, EnderEye, NetherStar, EndRod, LightningRod, EndCrystal, Paper, Book, WritableBook, EnchantedBook, OakBoat, 
              SpruceBoat, BirchBoat, JungleBoat, AcaciaBoat, DarkOakBoat, MangroveBoat, OakChestBoat, SpruceChestBoat, BirchChestBoat, JungleChestBoat, AcaciaChestBoat, DarkOakChestBoat, MangroveChestBoat, Rail, GoldenRail, 
              DetectorRail, ActivatorRail, Minecart, ChestMinecart, HopperMinecart, TntMinecart, RedstoneBlock, RedstoneTorch, Lever, WoodenButton, SpruceButton, BirchButton, JungleButton, AcaciaButton, DarkOakButton, MangroveButton, 
              StoneButton, CrimsonButton, WarpedButton, PolishedBlackstoneButton, TripwireHook, WoodenPressurePlate, SprucePressurePlate, BirchPressurePlate, JunglePressurePlate, AcaciaPressurePlate, DarkOakPressurePlate, 
              MangrovePressurePlate, CrimsonPressurePlate, WarpedPressurePlate, StonePressurePlate, LightWeightedPressurePlate, HeavyWeightedPressurePlate, PolishedBlackstonePressurePlate, Observer, DaylightDetector, Repeater, 
              Comparator, Hopper, Dropper, Dispenser, Piston, StickyPiston, Tnt, NameTag, Loom, Banner, BordureIndentedBannerPattern, CreeperBannerPattern, FieldMasonedBannerPattern, FlowerBannerPattern, BannerPattern, 
              MojangBannerPattern, PiglinBannerPattern, SkullBannerPattern, FireworkRocket, FireworkStar, Chain, Target, Air, Allow, Barrier, CommandBlock, ChainCommandBlock, RepeatingCommandBlock, CommandBlockMinecart, StructureBlock, 
              StructureVoid, Jigsaw, LightBlock, SuspiciousStew, FilledMap, FrostedIce, Portal, EndPortal, EndGateway]

class Entities:
    ArmorStand = "armor_stand"
    Arrow = "arrow"
    Axolotl = "axolotl"
    Bat = "bat"
    Bee = "bee"
    Blaze = "blaze"
    Cat = "cat"
    CaveSpider = "cave_spider"
    Chicken = "chicken"
    Cow = "cow"
    Creeper = "creeper"
    Dolphin = "dolphin"
    Donkey = "donkey"
    Drowned = "drowned"
    ElderGuardian = "elder_guardian"
    EnderDragon = "ender_dragon"
    Enderman = "enderman"
    Endermite = "endermite"
    EvocationIllager = "evocation_illager"
    Fish = "fish"
    FishingHook = "fishing_hook"
    Fireball = "fireball"
    Fox = "fox"
    Ghast = "ghast"
    GlowSquid = "glow_squid"
    Goat = "goat"
    Guardian = "guardian"
    Hoglin = "hoglin"
    Horse = "horse"
    Husk = "husk"
    IronGolem = "iron_golem"
    Llama = "llama"
    LlamaSpit = "llama_spit"
    MagmaCube = "magma_cube"
    Mooshroom = "mooshroom"
    Mule = "mule"
    Npc = "npc"
    Ocelot = "ocelot"
    Panda = "panda"
    Parrot = "parrot"
    Phantom = "phantom"
    Pig = "pig"
    PiglinBrute = "piglin_brute"
    Piglin = "piglin"
    Pillager = "pillager"
    Player = "player"
    PolarBear = "polar_bear"
    Pufferfish = "pufferfish"
    Rabbit = "rabbit"
    Ravager = "ravager"
    Salmon = "salmon"
    Sheep = "sheep"
    Shulker = "shulker"
    Silverfish = "silverfish"
    SkeletonHorse = "skeleton_horse"
    Skeleton = "skeleton"
    Slime = "slime"
    SnowGolem = "snow_golem"
    Spider = "spider"
    Squid = "squid"
    Stray = "stray"
    Strider = "strider"
    Tropicalfish = "tropicalfish"
    ThrownTrident = "thrown_trident"
    Turtle = "turtle"
    Vex = "vex"
    Villager = "villager_v2"
    Vindicator = "vindicator"
    WanderingTrader = "wandering_trader"
    Witch = "witch"
    WitherSkull = "wither_skull"
    WitherSkullDangeroud = "wither_skull_dangerous"
    WitherSkeleton = "wither_skeleton"
    Wither = "wither"
    Wolf = "wolf"
    Zoglin = "zoglin"
    ZombieHorse = "zombie_horse"
    ZombiePigman = "zombie_pigman"
    ZombieVillager = "zombie_villager_v2"
    Zombie = "zombie"
    Boat = "boat"
    Snowball = "snowball"
    LightningBolt = 'lightning_bolt'
    # 1.19.0
    # Updated on 11-07-2022
    Warden = "warden"
    # 1.19.50.21
    # Updated on 21-10-2022
    Camel = "camel"
    # 1.19.70.23
    # Updated on 28-02-2023
    Sniffer = "sniffer"