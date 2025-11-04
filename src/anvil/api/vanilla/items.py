from enum import StrEnum
from typing import Literal

from anvil.lib.schemas import MinecraftItemDescriptor

item_factory = lambda identifier: MinecraftItemDescriptor(identifier)


class MinecraftItemTags(StrEnum):
    Arrow = "minecraft:arrow"
    Banner = "minecraft:banner"
    Boat = "minecraft:boat"
    Boats = "minecraft:boats"
    BookshelfBooks = "minecraft:bookshelf_books"
    ChainmailTier = "minecraft:chainmail_tier"
    Coals = "minecraft:coals"
    CrimsonStems = "minecraft:crimson_stems"
    DecoratedPotSherds = "minecraft:decorated_pot_sherds"
    DiamondTier = "minecraft:diamond_tier"
    Digger = "minecraft:digger"
    Door = "minecraft:door"
    GoldenTier = "minecraft:golden_tier"
    HangingActor = "minecraft:hanging_actor"
    HangingSign = "minecraft:hanging_sign"
    HorseArmor = "minecraft:horse_armor"
    IronTier = "minecraft:iron_tier"
    IsArmor = "minecraft:is_armor"
    IsAxe = "minecraft:is_axe"
    IsCooked = "minecraft:is_cooked"
    IsFish = "minecraft:is_fish"
    IsFood = "minecraft:is_food"
    IsHoe = "minecraft:is_hoe"
    IsMeat = "minecraft:is_meat"
    IsMinecart = "minecraft:is_minecart"
    IsPickaxe = "minecraft:is_pickaxe"
    IsShovel = "minecraft:is_shovel"
    IsSword = "minecraft:is_sword"
    IsTool = "minecraft:is_tool"
    IsTrident = "minecraft:is_trident"
    LeatherTier = "minecraft:leather_tier"
    LecternBooks = "minecraft:lectern_books"
    Logs = "minecraft:logs"
    LogsThatBurn = "minecraft:logs_that_burn"
    MangroveLogs = "minecraft:mangrove_logs"
    MusicDisc = "minecraft:music_disc"
    NetheriteTier = "minecraft:netherite_tier"
    Planks = "minecraft:planks"
    Sand = "minecraft:sand"
    Sign = "minecraft:sign"
    SoulFireBaseBlocks = "minecraft:soul_fire_base_blocks"
    SpawnEgg = "minecraft:spawn_egg"
    StoneBricks = "minecraft:stone_bricks"
    StoneCraftingMaterials = "minecraft:stone_crafting_materials"
    StoneTier = "minecraft:stone_tier"
    StoneToolMaterials = "minecraft:stone_tool_materials"
    TransformMaterials = "minecraft:transform_materials"
    TransformTemplates = "minecraft:transform_templates"
    TransformableItems = "minecraft:transformable_items"
    TrimTemplates = "minecraft:trim_templates"
    TrimmableArmors = "minecraft:trimmable_armors"
    VibrationDamper = "minecraft:vibration_damper"
    WarpedStems = "minecraft:warped_stems"
    WoodenSlabs = "minecraft:wooden_slabs"
    WoodenTier = "minecraft:wooden_tier"
    Wool = "minecraft:wool"


class MinecraftItemTypes:
    def AcaciaBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_boat")

    def AcaciaButton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_button")

    def AcaciaChestBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_chest_boat")

    def AcaciaDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_door")

    def AcaciaFence() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_fence")

    def AcaciaFenceGate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_fence_gate")

    def AcaciaHangingSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_hanging_sign")

    def AcaciaLeaves() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_leaves")

    def AcaciaLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_log")

    def AcaciaPlanks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_planks")

    def AcaciaPressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_pressure_plate")

    def AcaciaSapling() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_sapling")

    def AcaciaSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_sign")

    def AcaciaSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_slab")

    def AcaciaStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_stairs")

    def AcaciaTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_trapdoor")

    def AcaciaWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:acacia_wood")

    def ActivatorRail() -> MinecraftItemDescriptor:
        return item_factory("minecraft:activator_rail")

    def AllaySpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:allay_spawn_egg")

    def Allium() -> MinecraftItemDescriptor:
        return item_factory("minecraft:allium")

    def Allow() -> MinecraftItemDescriptor:
        return item_factory("minecraft:allow")

    def AmethystBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:amethyst_block")

    def AmethystCluster() -> MinecraftItemDescriptor:
        return item_factory("minecraft:amethyst_cluster")

    def AmethystShard() -> MinecraftItemDescriptor:
        return item_factory("minecraft:amethyst_shard")

    def AncientDebris() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ancient_debris")

    def Andesite() -> MinecraftItemDescriptor:
        return item_factory("minecraft:andesite")

    def AndesiteSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:andesite_slab")

    def AndesiteStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:andesite_stairs")

    def AndesiteWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:andesite_wall")

    def AnglerPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:angler_pottery_sherd")

    def Anvil() -> MinecraftItemDescriptor:
        return item_factory("minecraft:anvil")

    def Apple() -> MinecraftItemDescriptor:
        return item_factory("minecraft:apple")

    def ArcherPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:archer_pottery_sherd")

    def ArmadilloScute() -> MinecraftItemDescriptor:
        return item_factory("minecraft:armadillo_scute")

    def ArmadilloSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:armadillo_spawn_egg")

    def ArmorStand() -> MinecraftItemDescriptor:
        return item_factory("minecraft:armor_stand")

    def ArmsUpPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:arms_up_pottery_sherd")

    def Arrow() -> MinecraftItemDescriptor:
        return item_factory("minecraft:arrow")

    def AxolotlBucket() -> MinecraftItemDescriptor:
        return item_factory("minecraft:axolotl_bucket")

    def AxolotlSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:axolotl_spawn_egg")

    def Azalea() -> MinecraftItemDescriptor:
        return item_factory("minecraft:azalea")

    def AzaleaLeaves() -> MinecraftItemDescriptor:
        return item_factory("minecraft:azalea_leaves")

    def AzaleaLeavesFlowered() -> MinecraftItemDescriptor:
        return item_factory("minecraft:azalea_leaves_flowered")

    def AzureBluet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:azure_bluet")

    def BakedPotato() -> MinecraftItemDescriptor:
        return item_factory("minecraft:baked_potato")

    def Bamboo() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo")

    def BambooBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_block")

    def BambooButton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_button")

    def BambooChestRaft() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_chest_raft")

    def BambooDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_door")

    def BambooFence() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_fence")

    def BambooFenceGate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_fence_gate")

    def BambooHangingSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_hanging_sign")

    def BambooMosaic() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_mosaic")

    def BambooMosaicSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_mosaic_slab")

    def BambooMosaicStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_mosaic_stairs")

    def BambooPlanks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_planks")

    def BambooPressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_pressure_plate")

    def BambooRaft() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_raft")

    def BambooSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_sign")

    def BambooSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_slab")

    def BambooStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_stairs")

    def BambooTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bamboo_trapdoor")

    def Banner() -> MinecraftItemDescriptor:
        return item_factory("minecraft:banner")

    def Barrel() -> MinecraftItemDescriptor:
        return item_factory("minecraft:barrel")

    def Barrier() -> MinecraftItemDescriptor:
        return item_factory("minecraft:barrier")

    def Basalt() -> MinecraftItemDescriptor:
        return item_factory("minecraft:basalt")

    def BatSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bat_spawn_egg")

    def Beacon() -> MinecraftItemDescriptor:
        return item_factory("minecraft:beacon")

    def Bed() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bed")

    def Bedrock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bedrock")

    def BeeNest() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bee_nest")

    def BeeSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bee_spawn_egg")

    def Beef() -> MinecraftItemDescriptor:
        return item_factory("minecraft:beef")

    def Beehive() -> MinecraftItemDescriptor:
        return item_factory("minecraft:beehive")

    def Beetroot() -> MinecraftItemDescriptor:
        return item_factory("minecraft:beetroot")

    def BeetrootSeeds() -> MinecraftItemDescriptor:
        return item_factory("minecraft:beetroot_seeds")

    def BeetrootSoup() -> MinecraftItemDescriptor:
        return item_factory("minecraft:beetroot_soup")

    def Bell() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bell")

    def BigDripleaf() -> MinecraftItemDescriptor:
        return item_factory("minecraft:big_dripleaf")

    def BirchBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_boat")

    def BirchButton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_button")

    def BirchChestBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_chest_boat")

    def BirchDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_door")

    def BirchFence() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_fence")

    def BirchFenceGate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_fence_gate")

    def BirchHangingSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_hanging_sign")

    def BirchLeaves() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_leaves")

    def BirchLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_log")

    def BirchPlanks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_planks")

    def BirchPressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_pressure_plate")

    def BirchSapling() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_sapling")

    def BirchSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_sign")

    def BirchSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_slab")

    def BirchStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_stairs")

    def BirchTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_trapdoor")

    def BirchWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:birch_wood")

    def BlackBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:black_bundle")

    def BlackCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:black_candle")

    def BlackCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:black_carpet")

    def BlackConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:black_concrete")

    def BlackConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:black_concrete_powder")

    def BlackDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:black_dye")

    def BlackGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:black_glazed_terracotta")

    def BlackHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:black_harness")

    def BlackShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:black_shulker_box")

    def BlackStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:black_stained_glass")

    def BlackStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:black_stained_glass_pane")

    def BlackTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:black_terracotta")

    def BlackWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:black_wool")

    def Blackstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blackstone")

    def BlackstoneSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blackstone_slab")

    def BlackstoneStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blackstone_stairs")

    def BlackstoneWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blackstone_wall")

    def BladePotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blade_pottery_sherd")

    def BlastFurnace() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blast_furnace")

    def BlazePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blaze_powder")

    def BlazeRod() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blaze_rod")

    def BlazeSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blaze_spawn_egg")

    def BlueBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_bundle")

    def BlueCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_candle")

    def BlueCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_carpet")

    def BlueConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_concrete")

    def BlueConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_concrete_powder")

    def BlueDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_dye")

    def BlueEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_egg")

    def BlueGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_glazed_terracotta")

    def BlueHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_harness")

    def BlueIce() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_ice")

    def BlueOrchid() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_orchid")

    def BlueShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_shulker_box")

    def BlueStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_stained_glass")

    def BlueStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_stained_glass_pane")

    def BlueTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_terracotta")

    def BlueWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:blue_wool")

    def BoggedSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bogged_spawn_egg")

    def BoltArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bolt_armor_trim_smithing_template")

    def Bone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bone")

    def BoneBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bone_block")

    def BoneMeal() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bone_meal")

    def Book() -> MinecraftItemDescriptor:
        return item_factory("minecraft:book")

    def Bookshelf() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bookshelf")

    def BorderBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:border_block")

    def BordureIndentedBannerPattern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bordure_indented_banner_pattern")

    def Bow() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bow")

    def Bowl() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bowl")

    def BrainCoral() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brain_coral")

    def BrainCoralBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brain_coral_block")

    def BrainCoralFan() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brain_coral_fan")

    def Bread() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bread")

    def BreezeRod() -> MinecraftItemDescriptor:
        return item_factory("minecraft:breeze_rod")

    def BreezeSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:breeze_spawn_egg")

    def BrewerPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brewer_pottery_sherd")

    def BrewingStand() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brewing_stand")

    def Brick() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brick")

    def BrickBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brick_block")

    def BrickSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brick_slab")

    def BrickStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brick_stairs")

    def BrickWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brick_wall")

    def BrownBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_bundle")

    def BrownCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_candle")

    def BrownCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_carpet")

    def BrownConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_concrete")

    def BrownConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_concrete_powder")

    def BrownDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_dye")

    def BrownEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_egg")

    def BrownGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_glazed_terracotta")

    def BrownHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_harness")

    def BrownMushroom() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_mushroom")

    def BrownMushroomBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_mushroom_block")

    def BrownShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_shulker_box")

    def BrownStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_stained_glass")

    def BrownStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_stained_glass_pane")

    def BrownTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_terracotta")

    def BrownWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brown_wool")

    def Brush() -> MinecraftItemDescriptor:
        return item_factory("minecraft:brush")

    def BubbleCoral() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bubble_coral")

    def BubbleCoralBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bubble_coral_block")

    def BubbleCoralFan() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bubble_coral_fan")

    def Bucket() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bucket")

    def BuddingAmethyst() -> MinecraftItemDescriptor:
        return item_factory("minecraft:budding_amethyst")

    def Bundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bundle")

    def BurnPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:burn_pottery_sherd")

    def Bush() -> MinecraftItemDescriptor:
        return item_factory("minecraft:bush")

    def Cactus() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cactus")

    def CactusFlower() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cactus_flower")

    def Cake() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cake")

    def Calcite() -> MinecraftItemDescriptor:
        return item_factory("minecraft:calcite")

    def CalibratedSculkSensor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:calibrated_sculk_sensor")

    def CamelSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:camel_spawn_egg")

    def Campfire() -> MinecraftItemDescriptor:
        return item_factory("minecraft:campfire")

    def Candle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:candle")

    def Carrot() -> MinecraftItemDescriptor:
        return item_factory("minecraft:carrot")

    def CarrotOnAStick() -> MinecraftItemDescriptor:
        return item_factory("minecraft:carrot_on_a_stick")

    def CartographyTable() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cartography_table")

    def CarvedPumpkin() -> MinecraftItemDescriptor:
        return item_factory("minecraft:carved_pumpkin")

    def CatSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cat_spawn_egg")

    def Cauldron() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cauldron")

    def CaveSpiderSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cave_spider_spawn_egg")

    def Chain() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chain")

    def ChainCommandBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chain_command_block")

    def ChainmailBoots() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chainmail_boots")

    def ChainmailChestplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chainmail_chestplate")

    def ChainmailHelmet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chainmail_helmet")

    def ChainmailLeggings() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chainmail_leggings")

    def Charcoal() -> MinecraftItemDescriptor:
        return item_factory("minecraft:charcoal")

    def CherryBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_boat")

    def CherryButton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_button")

    def CherryChestBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_chest_boat")

    def CherryDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_door")

    def CherryFence() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_fence")

    def CherryFenceGate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_fence_gate")

    def CherryHangingSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_hanging_sign")

    def CherryLeaves() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_leaves")

    def CherryLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_log")

    def CherryPlanks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_planks")

    def CherryPressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_pressure_plate")

    def CherrySapling() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_sapling")

    def CherrySign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_sign")

    def CherrySlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_slab")

    def CherryStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_stairs")

    def CherryTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_trapdoor")

    def CherryWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cherry_wood")

    def Chest() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chest")

    def ChestMinecart() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chest_minecart")

    def Chicken() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chicken")

    def ChickenSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chicken_spawn_egg")

    def ChippedAnvil() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chipped_anvil")

    def ChiseledBookshelf() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chiseled_bookshelf")

    def ChiseledCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chiseled_copper")

    def ChiseledDeepslate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chiseled_deepslate")

    def ChiseledNetherBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chiseled_nether_bricks")

    def ChiseledPolishedBlackstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chiseled_polished_blackstone")

    def ChiseledQuartzBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chiseled_quartz_block")

    def ChiseledRedSandstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chiseled_red_sandstone")

    def ChiseledResinBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chiseled_resin_bricks")

    def ChiseledSandstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chiseled_sandstone")

    def ChiseledStoneBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chiseled_stone_bricks")

    def ChiseledTuff() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chiseled_tuff")

    def ChiseledTuffBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chiseled_tuff_bricks")

    def ChorusFlower() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chorus_flower")

    def ChorusFruit() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chorus_fruit")

    def ChorusPlant() -> MinecraftItemDescriptor:
        return item_factory("minecraft:chorus_plant")

    def Clay() -> MinecraftItemDescriptor:
        return item_factory("minecraft:clay")

    def ClayBall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:clay_ball")

    def Clock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:clock")

    def ClosedEyeblossom() -> MinecraftItemDescriptor:
        return item_factory("minecraft:closed_eyeblossom")

    def Coal() -> MinecraftItemDescriptor:
        return item_factory("minecraft:coal")

    def CoalBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:coal_block")

    def CoalOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:coal_ore")

    def CoarseDirt() -> MinecraftItemDescriptor:
        return item_factory("minecraft:coarse_dirt")

    def CoastArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:coast_armor_trim_smithing_template")

    def CobbledDeepslate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cobbled_deepslate")

    def CobbledDeepslateSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cobbled_deepslate_slab")

    def CobbledDeepslateStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cobbled_deepslate_stairs")

    def CobbledDeepslateWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cobbled_deepslate_wall")

    def Cobblestone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cobblestone")

    def CobblestoneSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cobblestone_slab")

    def CobblestoneWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cobblestone_wall")

    def CocoaBeans() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cocoa_beans")

    def Cod() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cod")

    def CodBucket() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cod_bucket")

    def CodSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cod_spawn_egg")

    def CommandBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:command_block")

    def CommandBlockMinecart() -> MinecraftItemDescriptor:
        return item_factory("minecraft:command_block_minecart")

    def Comparator() -> MinecraftItemDescriptor:
        return item_factory("minecraft:comparator")

    def Compass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:compass")

    def Composter() -> MinecraftItemDescriptor:
        return item_factory("minecraft:composter")

    def Conduit() -> MinecraftItemDescriptor:
        return item_factory("minecraft:conduit")

    def CookedBeef() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cooked_beef")

    def CookedChicken() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cooked_chicken")

    def CookedCod() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cooked_cod")

    def CookedMutton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cooked_mutton")

    def CookedPorkchop() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cooked_porkchop")

    def CookedRabbit() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cooked_rabbit")

    def CookedSalmon() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cooked_salmon")

    def Cookie() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cookie")

    def CopperAxe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_axe")

    def CopperBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_block")

    def CopperBoots() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_boots")

    def CopperBulb() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_bulb")

    def CopperChest() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_chest")

    def CopperChestplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_chestplate")

    def CopperDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_door")

    def CopperGolemSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_golem_spawn_egg")

    def CopperGrate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_grate")

    def CopperHelmet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_helmet")

    def CopperHoe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_hoe")

    def CopperIngot() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_ingot")

    def CopperLeggings() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_leggings")

    def CopperNugget() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_nugget")

    def CopperOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_ore")

    def CopperPickaxe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_pickaxe")

    def CopperShovel() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_shovel")

    def CopperSword() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_sword")

    def CopperTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:copper_trapdoor")

    def Cornflower() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cornflower")

    def CowSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cow_spawn_egg")

    def CrackedDeepslateBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cracked_deepslate_bricks")

    def CrackedDeepslateTiles() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cracked_deepslate_tiles")

    def CrackedNetherBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cracked_nether_bricks")

    def CrackedPolishedBlackstoneBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cracked_polished_blackstone_bricks")

    def CrackedStoneBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cracked_stone_bricks")

    def Crafter() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crafter")

    def CraftingTable() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crafting_table")

    def CreakingHeart() -> MinecraftItemDescriptor:
        return item_factory("minecraft:creaking_heart")

    def CreakingSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:creaking_spawn_egg")

    def CreeperBannerPattern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:creeper_banner_pattern")

    def CreeperHead() -> MinecraftItemDescriptor:
        return item_factory("minecraft:creeper_head")

    def CreeperSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:creeper_spawn_egg")

    def CrimsonButton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_button")

    def CrimsonDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_door")

    def CrimsonFence() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_fence")

    def CrimsonFenceGate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_fence_gate")

    def CrimsonFungus() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_fungus")

    def CrimsonHangingSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_hanging_sign")

    def CrimsonHyphae() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_hyphae")

    def CrimsonNylium() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_nylium")

    def CrimsonPlanks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_planks")

    def CrimsonPressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_pressure_plate")

    def CrimsonRoots() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_roots")

    def CrimsonSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_sign")

    def CrimsonSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_slab")

    def CrimsonStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_stairs")

    def CrimsonStem() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_stem")

    def CrimsonTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crimson_trapdoor")

    def Crossbow() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crossbow")

    def CryingObsidian() -> MinecraftItemDescriptor:
        return item_factory("minecraft:crying_obsidian")

    def CutCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cut_copper")

    def CutCopperSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cut_copper_slab")

    def CutCopperStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cut_copper_stairs")

    def CutRedSandstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cut_red_sandstone")

    def CutRedSandstoneSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cut_red_sandstone_slab")

    def CutSandstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cut_sandstone")

    def CutSandstoneSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cut_sandstone_slab")

    def CyanBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cyan_bundle")

    def CyanCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cyan_candle")

    def CyanCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cyan_carpet")

    def CyanConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cyan_concrete")

    def CyanConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cyan_concrete_powder")

    def CyanDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cyan_dye")

    def CyanGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cyan_glazed_terracotta")

    def CyanHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cyan_harness")

    def CyanShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cyan_shulker_box")

    def CyanStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cyan_stained_glass")

    def CyanStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cyan_stained_glass_pane")

    def CyanTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cyan_terracotta")

    def CyanWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:cyan_wool")

    def DamagedAnvil() -> MinecraftItemDescriptor:
        return item_factory("minecraft:damaged_anvil")

    def Dandelion() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dandelion")

    def DangerPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:danger_pottery_sherd")

    def DarkOakBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_boat")

    def DarkOakButton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_button")

    def DarkOakChestBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_chest_boat")

    def DarkOakDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_door")

    def DarkOakFence() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_fence")

    def DarkOakFenceGate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_fence_gate")

    def DarkOakHangingSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_hanging_sign")

    def DarkOakLeaves() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_leaves")

    def DarkOakLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_log")

    def DarkOakPlanks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_planks")

    def DarkOakPressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_pressure_plate")

    def DarkOakSapling() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_sapling")

    def DarkOakSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_sign")

    def DarkOakSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_slab")

    def DarkOakStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_stairs")

    def DarkOakTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_trapdoor")

    def DarkOakWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_oak_wood")

    def DarkPrismarine() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_prismarine")

    def DarkPrismarineSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_prismarine_slab")

    def DarkPrismarineStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dark_prismarine_stairs")

    def DaylightDetector() -> MinecraftItemDescriptor:
        return item_factory("minecraft:daylight_detector")

    def DeadBrainCoral() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_brain_coral")

    def DeadBrainCoralBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_brain_coral_block")

    def DeadBrainCoralFan() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_brain_coral_fan")

    def DeadBubbleCoral() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_bubble_coral")

    def DeadBubbleCoralBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_bubble_coral_block")

    def DeadBubbleCoralFan() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_bubble_coral_fan")

    def DeadFireCoral() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_fire_coral")

    def DeadFireCoralBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_fire_coral_block")

    def DeadFireCoralFan() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_fire_coral_fan")

    def DeadHornCoral() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_horn_coral")

    def DeadHornCoralBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_horn_coral_block")

    def DeadHornCoralFan() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_horn_coral_fan")

    def DeadTubeCoral() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_tube_coral")

    def DeadTubeCoralBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_tube_coral_block")

    def DeadTubeCoralFan() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dead_tube_coral_fan")

    def Deadbush() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deadbush")

    def DecoratedPot() -> MinecraftItemDescriptor:
        return item_factory("minecraft:decorated_pot")

    def Deepslate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate")

    def DeepslateBrickSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_brick_slab")

    def DeepslateBrickStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_brick_stairs")

    def DeepslateBrickWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_brick_wall")

    def DeepslateBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_bricks")

    def DeepslateCoalOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_coal_ore")

    def DeepslateCopperOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_copper_ore")

    def DeepslateDiamondOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_diamond_ore")

    def DeepslateEmeraldOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_emerald_ore")

    def DeepslateGoldOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_gold_ore")

    def DeepslateIronOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_iron_ore")

    def DeepslateLapisOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_lapis_ore")

    def DeepslateRedstoneOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_redstone_ore")

    def DeepslateTileSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_tile_slab")

    def DeepslateTileStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_tile_stairs")

    def DeepslateTileWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_tile_wall")

    def DeepslateTiles() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deepslate_tiles")

    def Deny() -> MinecraftItemDescriptor:
        return item_factory("minecraft:deny")

    def DetectorRail() -> MinecraftItemDescriptor:
        return item_factory("minecraft:detector_rail")

    def Diamond() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diamond")

    def DiamondAxe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diamond_axe")

    def DiamondBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diamond_block")

    def DiamondBoots() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diamond_boots")

    def DiamondChestplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diamond_chestplate")

    def DiamondHelmet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diamond_helmet")

    def DiamondHoe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diamond_hoe")

    def DiamondHorseArmor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diamond_horse_armor")

    def DiamondLeggings() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diamond_leggings")

    def DiamondOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diamond_ore")

    def DiamondPickaxe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diamond_pickaxe")

    def DiamondShovel() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diamond_shovel")

    def DiamondSword() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diamond_sword")

    def Diorite() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diorite")

    def DioriteSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diorite_slab")

    def DioriteStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diorite_stairs")

    def DioriteWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:diorite_wall")

    def Dirt() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dirt")

    def DirtWithRoots() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dirt_with_roots")

    def DiscFragment5() -> MinecraftItemDescriptor:
        return item_factory("minecraft:disc_fragment_5")

    def Dispenser() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dispenser")

    def DolphinSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dolphin_spawn_egg")

    def DonkeySpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:donkey_spawn_egg")

    def DragonBreath() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dragon_breath")

    def DragonEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dragon_egg")

    def DragonHead() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dragon_head")

    def DriedGhast() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dried_ghast")

    def DriedKelp() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dried_kelp")

    def DriedKelpBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dried_kelp_block")

    def DripstoneBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dripstone_block")

    def Dropper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dropper")

    def DrownedSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:drowned_spawn_egg")

    def DuneArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:dune_armor_trim_smithing_template")

    def EchoShard() -> MinecraftItemDescriptor:
        return item_factory("minecraft:echo_shard")

    def Egg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:egg")

    def ElderGuardianSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:elder_guardian_spawn_egg")

    def Elytra() -> MinecraftItemDescriptor:
        return item_factory("minecraft:elytra")

    def Emerald() -> MinecraftItemDescriptor:
        return item_factory("minecraft:emerald")

    def EmeraldBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:emerald_block")

    def EmeraldOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:emerald_ore")

    def EmptyMap() -> MinecraftItemDescriptor:
        return item_factory("minecraft:empty_map")

    def EnchantedBook() -> MinecraftItemDescriptor:
        return item_factory("minecraft:enchanted_book")

    def EnchantedGoldenApple() -> MinecraftItemDescriptor:
        return item_factory("minecraft:enchanted_golden_apple")

    def EnchantingTable() -> MinecraftItemDescriptor:
        return item_factory("minecraft:enchanting_table")

    def EndBrickStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:end_brick_stairs")

    def EndBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:end_bricks")

    def EndCrystal() -> MinecraftItemDescriptor:
        return item_factory("minecraft:end_crystal")

    def EndPortalFrame() -> MinecraftItemDescriptor:
        return item_factory("minecraft:end_portal_frame")

    def EndRod() -> MinecraftItemDescriptor:
        return item_factory("minecraft:end_rod")

    def EndStone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:end_stone")

    def EndStoneBrickSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:end_stone_brick_slab")

    def EndStoneBrickWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:end_stone_brick_wall")

    def EnderChest() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ender_chest")

    def EnderDragonSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ender_dragon_spawn_egg")

    def EnderEye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ender_eye")

    def EnderPearl() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ender_pearl")

    def EndermanSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:enderman_spawn_egg")

    def EndermiteSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:endermite_spawn_egg")

    def EvokerSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:evoker_spawn_egg")

    def ExperienceBottle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:experience_bottle")

    def ExplorerPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:explorer_pottery_sherd")

    def ExposedChiseledCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:exposed_chiseled_copper")

    def ExposedCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:exposed_copper")

    def ExposedCopperBulb() -> MinecraftItemDescriptor:
        return item_factory("minecraft:exposed_copper_bulb")

    def ExposedCopperChest() -> MinecraftItemDescriptor:
        return item_factory("minecraft:exposed_copper_chest")

    def ExposedCopperDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:exposed_copper_door")

    def ExposedCopperGrate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:exposed_copper_grate")

    def ExposedCopperTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:exposed_copper_trapdoor")

    def ExposedCutCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:exposed_cut_copper")

    def ExposedCutCopperSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:exposed_cut_copper_slab")

    def ExposedCutCopperStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:exposed_cut_copper_stairs")

    def EyeArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:eye_armor_trim_smithing_template")

    def Farmland() -> MinecraftItemDescriptor:
        return item_factory("minecraft:farmland")

    def Feather() -> MinecraftItemDescriptor:
        return item_factory("minecraft:feather")

    def FenceGate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:fence_gate")

    def FermentedSpiderEye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:fermented_spider_eye")

    def Fern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:fern")

    def FieldMasonedBannerPattern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:field_masoned_banner_pattern")

    def FilledMap() -> MinecraftItemDescriptor:
        return item_factory("minecraft:filled_map")

    def FireCharge() -> MinecraftItemDescriptor:
        return item_factory("minecraft:fire_charge")

    def FireCoral() -> MinecraftItemDescriptor:
        return item_factory("minecraft:fire_coral")

    def FireCoralBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:fire_coral_block")

    def FireCoralFan() -> MinecraftItemDescriptor:
        return item_factory("minecraft:fire_coral_fan")

    def FireflyBush() -> MinecraftItemDescriptor:
        return item_factory("minecraft:firefly_bush")

    def FireworkRocket() -> MinecraftItemDescriptor:
        return item_factory("minecraft:firework_rocket")

    def FireworkStar() -> MinecraftItemDescriptor:
        return item_factory("minecraft:firework_star")

    def FishingRod() -> MinecraftItemDescriptor:
        return item_factory("minecraft:fishing_rod")

    def FletchingTable() -> MinecraftItemDescriptor:
        return item_factory("minecraft:fletching_table")

    def Flint() -> MinecraftItemDescriptor:
        return item_factory("minecraft:flint")

    def FlintAndSteel() -> MinecraftItemDescriptor:
        return item_factory("minecraft:flint_and_steel")

    def FlowArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:flow_armor_trim_smithing_template")

    def FlowBannerPattern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:flow_banner_pattern")

    def FlowPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:flow_pottery_sherd")

    def FlowerBannerPattern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:flower_banner_pattern")

    def FlowerPot() -> MinecraftItemDescriptor:
        return item_factory("minecraft:flower_pot")

    def FloweringAzalea() -> MinecraftItemDescriptor:
        return item_factory("minecraft:flowering_azalea")

    def FoxSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:fox_spawn_egg")

    def Frame() -> MinecraftItemDescriptor:
        return item_factory("minecraft:frame")

    def FriendPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:friend_pottery_sherd")

    def FrogSpawn() -> MinecraftItemDescriptor:
        return item_factory("minecraft:frog_spawn")

    def FrogSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:frog_spawn_egg")

    def FrostedIce() -> MinecraftItemDescriptor:
        return item_factory("minecraft:frosted_ice")

    def Furnace() -> MinecraftItemDescriptor:
        return item_factory("minecraft:furnace")

    def GhastSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ghast_spawn_egg")

    def GhastTear() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ghast_tear")

    def GildedBlackstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gilded_blackstone")

    def Glass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:glass")

    def GlassBottle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:glass_bottle")

    def GlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:glass_pane")

    def GlisteringMelonSlice() -> MinecraftItemDescriptor:
        return item_factory("minecraft:glistering_melon_slice")

    def GlobeBannerPattern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:globe_banner_pattern")

    def GlowBerries() -> MinecraftItemDescriptor:
        return item_factory("minecraft:glow_berries")

    def GlowFrame() -> MinecraftItemDescriptor:
        return item_factory("minecraft:glow_frame")

    def GlowInkSac() -> MinecraftItemDescriptor:
        return item_factory("minecraft:glow_ink_sac")

    def GlowLichen() -> MinecraftItemDescriptor:
        return item_factory("minecraft:glow_lichen")

    def GlowSquidSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:glow_squid_spawn_egg")

    def Glowstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:glowstone")

    def GlowstoneDust() -> MinecraftItemDescriptor:
        return item_factory("minecraft:glowstone_dust")

    def GoatHorn() -> MinecraftItemDescriptor:
        return item_factory("minecraft:goat_horn")

    def GoatSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:goat_spawn_egg")

    def GoldBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gold_block")

    def GoldIngot() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gold_ingot")

    def GoldNugget() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gold_nugget")

    def GoldOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gold_ore")

    def GoldenApple() -> MinecraftItemDescriptor:
        return item_factory("minecraft:golden_apple")

    def GoldenAxe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:golden_axe")

    def GoldenBoots() -> MinecraftItemDescriptor:
        return item_factory("minecraft:golden_boots")

    def GoldenCarrot() -> MinecraftItemDescriptor:
        return item_factory("minecraft:golden_carrot")

    def GoldenChestplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:golden_chestplate")

    def GoldenHelmet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:golden_helmet")

    def GoldenHoe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:golden_hoe")

    def GoldenHorseArmor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:golden_horse_armor")

    def GoldenLeggings() -> MinecraftItemDescriptor:
        return item_factory("minecraft:golden_leggings")

    def GoldenPickaxe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:golden_pickaxe")

    def GoldenRail() -> MinecraftItemDescriptor:
        return item_factory("minecraft:golden_rail")

    def GoldenShovel() -> MinecraftItemDescriptor:
        return item_factory("minecraft:golden_shovel")

    def GoldenSword() -> MinecraftItemDescriptor:
        return item_factory("minecraft:golden_sword")

    def Granite() -> MinecraftItemDescriptor:
        return item_factory("minecraft:granite")

    def GraniteSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:granite_slab")

    def GraniteStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:granite_stairs")

    def GraniteWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:granite_wall")

    def GrassBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:grass_block")

    def GrassPath() -> MinecraftItemDescriptor:
        return item_factory("minecraft:grass_path")

    def Gravel() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gravel")

    def GrayBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gray_bundle")

    def GrayCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gray_candle")

    def GrayCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gray_carpet")

    def GrayConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gray_concrete")

    def GrayConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gray_concrete_powder")

    def GrayDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gray_dye")

    def GrayGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gray_glazed_terracotta")

    def GrayHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gray_harness")

    def GrayShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gray_shulker_box")

    def GrayStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gray_stained_glass")

    def GrayStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gray_stained_glass_pane")

    def GrayTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gray_terracotta")

    def GrayWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gray_wool")

    def GreenBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:green_bundle")

    def GreenCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:green_candle")

    def GreenCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:green_carpet")

    def GreenConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:green_concrete")

    def GreenConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:green_concrete_powder")

    def GreenDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:green_dye")

    def GreenGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:green_glazed_terracotta")

    def GreenHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:green_harness")

    def GreenShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:green_shulker_box")

    def GreenStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:green_stained_glass")

    def GreenStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:green_stained_glass_pane")

    def GreenTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:green_terracotta")

    def GreenWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:green_wool")

    def Grindstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:grindstone")

    def GuardianSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:guardian_spawn_egg")

    def Gunpowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:gunpowder")

    def GusterBannerPattern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:guster_banner_pattern")

    def GusterPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:guster_pottery_sherd")

    def HangingRoots() -> MinecraftItemDescriptor:
        return item_factory("minecraft:hanging_roots")

    def HappyGhastSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:happy_ghast_spawn_egg")

    def HardenedClay() -> MinecraftItemDescriptor:
        return item_factory("minecraft:hardened_clay")

    def HayBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:hay_block")

    def HeartOfTheSea() -> MinecraftItemDescriptor:
        return item_factory("minecraft:heart_of_the_sea")

    def HeartPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:heart_pottery_sherd")

    def HeartbreakPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:heartbreak_pottery_sherd")

    def HeavyCore() -> MinecraftItemDescriptor:
        return item_factory("minecraft:heavy_core")

    def HeavyWeightedPressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:heavy_weighted_pressure_plate")

    def HoglinSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:hoglin_spawn_egg")

    def HoneyBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:honey_block")

    def HoneyBottle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:honey_bottle")

    def Honeycomb() -> MinecraftItemDescriptor:
        return item_factory("minecraft:honeycomb")

    def HoneycombBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:honeycomb_block")

    def Hopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:hopper")

    def HopperMinecart() -> MinecraftItemDescriptor:
        return item_factory("minecraft:hopper_minecart")

    def HornCoral() -> MinecraftItemDescriptor:
        return item_factory("minecraft:horn_coral")

    def HornCoralBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:horn_coral_block")

    def HornCoralFan() -> MinecraftItemDescriptor:
        return item_factory("minecraft:horn_coral_fan")

    def HorseSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:horse_spawn_egg")

    def HostArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:host_armor_trim_smithing_template")

    def HowlPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:howl_pottery_sherd")

    def HuskSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:husk_spawn_egg")

    def Ice() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ice")

    def InfestedChiseledStoneBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:infested_chiseled_stone_bricks")

    def InfestedCobblestone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:infested_cobblestone")

    def InfestedCrackedStoneBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:infested_cracked_stone_bricks")

    def InfestedDeepslate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:infested_deepslate")

    def InfestedMossyStoneBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:infested_mossy_stone_bricks")

    def InfestedStone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:infested_stone")

    def InfestedStoneBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:infested_stone_bricks")

    def InkSac() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ink_sac")

    def IronAxe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_axe")

    def IronBars() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_bars")

    def IronBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_block")

    def IronBoots() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_boots")

    def IronChestplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_chestplate")

    def IronDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_door")

    def IronGolemSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_golem_spawn_egg")

    def IronHelmet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_helmet")

    def IronHoe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_hoe")

    def IronHorseArmor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_horse_armor")

    def IronIngot() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_ingot")

    def IronLeggings() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_leggings")

    def IronNugget() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_nugget")

    def IronOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_ore")

    def IronPickaxe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_pickaxe")

    def IronShovel() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_shovel")

    def IronSword() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_sword")

    def IronTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:iron_trapdoor")

    def Jigsaw() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jigsaw")

    def Jukebox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jukebox")

    def JungleBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_boat")

    def JungleButton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_button")

    def JungleChestBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_chest_boat")

    def JungleDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_door")

    def JungleFence() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_fence")

    def JungleFenceGate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_fence_gate")

    def JungleHangingSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_hanging_sign")

    def JungleLeaves() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_leaves")

    def JungleLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_log")

    def JunglePlanks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_planks")

    def JunglePressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_pressure_plate")

    def JungleSapling() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_sapling")

    def JungleSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_sign")

    def JungleSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_slab")

    def JungleStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_stairs")

    def JungleTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_trapdoor")

    def JungleWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:jungle_wood")

    def Kelp() -> MinecraftItemDescriptor:
        return item_factory("minecraft:kelp")

    def Ladder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ladder")

    def Lantern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lantern")

    def LapisBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lapis_block")

    def LapisLazuli() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lapis_lazuli")

    def LapisOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lapis_ore")

    def LargeAmethystBud() -> MinecraftItemDescriptor:
        return item_factory("minecraft:large_amethyst_bud")

    def LargeFern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:large_fern")

    def LavaBucket() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lava_bucket")

    def Lead() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lead")

    def LeafLitter() -> MinecraftItemDescriptor:
        return item_factory("minecraft:leaf_litter")

    def Leather() -> MinecraftItemDescriptor:
        return item_factory("minecraft:leather")

    def LeatherBoots() -> MinecraftItemDescriptor:
        return item_factory("minecraft:leather_boots")

    def LeatherChestplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:leather_chestplate")

    def LeatherHelmet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:leather_helmet")

    def LeatherHorseArmor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:leather_horse_armor")

    def LeatherLeggings() -> MinecraftItemDescriptor:
        return item_factory("minecraft:leather_leggings")

    def Lectern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lectern")

    def Lever() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lever")

    def LightBlock0() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_0")

    def LightBlock1() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_1")

    def LightBlock10() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_10")

    def LightBlock11() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_11")

    def LightBlock12() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_12")

    def LightBlock13() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_13")

    def LightBlock14() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_14")

    def LightBlock15() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_15")

    def LightBlock2() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_2")

    def LightBlock3() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_3")

    def LightBlock4() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_4")

    def LightBlock5() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_5")

    def LightBlock6() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_6")

    def LightBlock7() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_7")

    def LightBlock8() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_8")

    def LightBlock9() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_block_9")

    def LightBlueBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_blue_bundle")

    def LightBlueCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_blue_candle")

    def LightBlueCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_blue_carpet")

    def LightBlueConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_blue_concrete")

    def LightBlueConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_blue_concrete_powder")

    def LightBlueDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_blue_dye")

    def LightBlueGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_blue_glazed_terracotta")

    def LightBlueHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_blue_harness")

    def LightBlueShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_blue_shulker_box")

    def LightBlueStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_blue_stained_glass")

    def LightBlueStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_blue_stained_glass_pane")

    def LightBlueTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_blue_terracotta")

    def LightBlueWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_blue_wool")

    def LightGrayBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_gray_bundle")

    def LightGrayCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_gray_candle")

    def LightGrayCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_gray_carpet")

    def LightGrayConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_gray_concrete")

    def LightGrayConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_gray_concrete_powder")

    def LightGrayDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_gray_dye")

    def LightGrayHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_gray_harness")

    def LightGrayShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_gray_shulker_box")

    def LightGrayStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_gray_stained_glass")

    def LightGrayStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_gray_stained_glass_pane")

    def LightGrayTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_gray_terracotta")

    def LightGrayWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_gray_wool")

    def LightWeightedPressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:light_weighted_pressure_plate")

    def LightningRod() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lightning_rod")

    def Lilac() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lilac")

    def LilyOfTheValley() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lily_of_the_valley")

    def LimeBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lime_bundle")

    def LimeCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lime_candle")

    def LimeCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lime_carpet")

    def LimeConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lime_concrete")

    def LimeConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lime_concrete_powder")

    def LimeDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lime_dye")

    def LimeGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lime_glazed_terracotta")

    def LimeHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lime_harness")

    def LimeShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lime_shulker_box")

    def LimeStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lime_stained_glass")

    def LimeStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lime_stained_glass_pane")

    def LimeTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lime_terracotta")

    def LimeWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lime_wool")

    def LingeringPotion() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lingering_potion")

    def LitPumpkin() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lit_pumpkin")

    def LlamaSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:llama_spawn_egg")

    def Lodestone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lodestone")

    def LodestoneCompass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:lodestone_compass")

    def Loom() -> MinecraftItemDescriptor:
        return item_factory("minecraft:loom")

    def Mace() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mace")

    def MagentaBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magenta_bundle")

    def MagentaCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magenta_candle")

    def MagentaCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magenta_carpet")

    def MagentaConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magenta_concrete")

    def MagentaConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magenta_concrete_powder")

    def MagentaDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magenta_dye")

    def MagentaGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magenta_glazed_terracotta")

    def MagentaHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magenta_harness")

    def MagentaShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magenta_shulker_box")

    def MagentaStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magenta_stained_glass")

    def MagentaStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magenta_stained_glass_pane")

    def MagentaTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magenta_terracotta")

    def MagentaWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magenta_wool")

    def Magma() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magma")

    def MagmaCream() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magma_cream")

    def MagmaCubeSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:magma_cube_spawn_egg")

    def MangroveBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_boat")

    def MangroveButton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_button")

    def MangroveChestBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_chest_boat")

    def MangroveDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_door")

    def MangroveFence() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_fence")

    def MangroveFenceGate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_fence_gate")

    def MangroveHangingSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_hanging_sign")

    def MangroveLeaves() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_leaves")

    def MangroveLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_log")

    def MangrovePlanks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_planks")

    def MangrovePressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_pressure_plate")

    def MangrovePropagule() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_propagule")

    def MangroveRoots() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_roots")

    def MangroveSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_sign")

    def MangroveSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_slab")

    def MangroveStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_stairs")

    def MangroveTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_trapdoor")

    def MangroveWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mangrove_wood")

    def MediumAmethystBud() -> MinecraftItemDescriptor:
        return item_factory("minecraft:medium_amethyst_bud")

    def MelonBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:melon_block")

    def MelonSeeds() -> MinecraftItemDescriptor:
        return item_factory("minecraft:melon_seeds")

    def MelonSlice() -> MinecraftItemDescriptor:
        return item_factory("minecraft:melon_slice")

    def MilkBucket() -> MinecraftItemDescriptor:
        return item_factory("minecraft:milk_bucket")

    def Minecart() -> MinecraftItemDescriptor:
        return item_factory("minecraft:minecart")

    def MinerPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:miner_pottery_sherd")

    def MobSpawner() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mob_spawner")

    def MojangBannerPattern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mojang_banner_pattern")

    def MooshroomSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mooshroom_spawn_egg")

    def MossBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:moss_block")

    def MossCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:moss_carpet")

    def MossyCobblestone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mossy_cobblestone")

    def MossyCobblestoneSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mossy_cobblestone_slab")

    def MossyCobblestoneStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mossy_cobblestone_stairs")

    def MossyCobblestoneWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mossy_cobblestone_wall")

    def MossyStoneBrickSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mossy_stone_brick_slab")

    def MossyStoneBrickStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mossy_stone_brick_stairs")

    def MossyStoneBrickWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mossy_stone_brick_wall")

    def MossyStoneBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mossy_stone_bricks")

    def MournerPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mourner_pottery_sherd")

    def Mud() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mud")

    def MudBrickSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mud_brick_slab")

    def MudBrickStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mud_brick_stairs")

    def MudBrickWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mud_brick_wall")

    def MudBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mud_bricks")

    def MuddyMangroveRoots() -> MinecraftItemDescriptor:
        return item_factory("minecraft:muddy_mangrove_roots")

    def MuleSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mule_spawn_egg")

    def MushroomStem() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mushroom_stem")

    def MushroomStew() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mushroom_stew")

    def MusicDisc11() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_11")

    def MusicDisc13() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_13")

    def MusicDisc5() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_5")

    def MusicDiscBlocks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_blocks")

    def MusicDiscCat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_cat")

    def MusicDiscChirp() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_chirp")

    def MusicDiscCreator() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_creator")

    def MusicDiscCreatorMusicBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_creator_music_box")

    def MusicDiscFar() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_far")

    def MusicDiscLavaChicken() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_lava_chicken")

    def MusicDiscMall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_mall")

    def MusicDiscMellohi() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_mellohi")

    def MusicDiscOtherside() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_otherside")

    def MusicDiscPigstep() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_pigstep")

    def MusicDiscPrecipice() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_precipice")

    def MusicDiscRelic() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_relic")

    def MusicDiscStal() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_stal")

    def MusicDiscStrad() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_strad")

    def MusicDiscTears() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_tears")

    def MusicDiscWait() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_wait")

    def MusicDiscWard() -> MinecraftItemDescriptor:
        return item_factory("minecraft:music_disc_ward")

    def Mutton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mutton")

    def Mycelium() -> MinecraftItemDescriptor:
        return item_factory("minecraft:mycelium")

    def NameTag() -> MinecraftItemDescriptor:
        return item_factory("minecraft:name_tag")

    def NautilusShell() -> MinecraftItemDescriptor:
        return item_factory("minecraft:nautilus_shell")

    def NetherBrick() -> MinecraftItemDescriptor:
        return item_factory("minecraft:nether_brick")

    def NetherBrickFence() -> MinecraftItemDescriptor:
        return item_factory("minecraft:nether_brick_fence")

    def NetherBrickSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:nether_brick_slab")

    def NetherBrickStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:nether_brick_stairs")

    def NetherBrickWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:nether_brick_wall")

    def NetherGoldOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:nether_gold_ore")

    def NetherSprouts() -> MinecraftItemDescriptor:
        return item_factory("minecraft:nether_sprouts")

    def NetherStar() -> MinecraftItemDescriptor:
        return item_factory("minecraft:nether_star")

    def NetherWart() -> MinecraftItemDescriptor:
        return item_factory("minecraft:nether_wart")

    def NetherWartBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:nether_wart_block")

    def Netherbrick() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherbrick")

    def NetheriteAxe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherite_axe")

    def NetheriteBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherite_block")

    def NetheriteBoots() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherite_boots")

    def NetheriteChestplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherite_chestplate")

    def NetheriteHelmet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherite_helmet")

    def NetheriteHoe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherite_hoe")

    def NetheriteIngot() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherite_ingot")

    def NetheriteLeggings() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherite_leggings")

    def NetheritePickaxe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherite_pickaxe")

    def NetheriteScrap() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherite_scrap")

    def NetheriteShovel() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherite_shovel")

    def NetheriteSword() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherite_sword")

    def NetheriteUpgradeSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherite_upgrade_smithing_template")

    def Netherrack() -> MinecraftItemDescriptor:
        return item_factory("minecraft:netherrack")

    def NormalStoneSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:normal_stone_slab")

    def NormalStoneStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:normal_stone_stairs")

    def Noteblock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:noteblock")

    def OakBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oak_boat")

    def OakChestBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oak_chest_boat")

    def OakFence() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oak_fence")

    def OakHangingSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oak_hanging_sign")

    def OakLeaves() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oak_leaves")

    def OakLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oak_log")

    def OakPlanks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oak_planks")

    def OakSapling() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oak_sapling")

    def OakSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oak_sign")

    def OakSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oak_slab")

    def OakStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oak_stairs")

    def OakWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oak_wood")

    def Observer() -> MinecraftItemDescriptor:
        return item_factory("minecraft:observer")

    def Obsidian() -> MinecraftItemDescriptor:
        return item_factory("minecraft:obsidian")

    def OcelotSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ocelot_spawn_egg")

    def OchreFroglight() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ochre_froglight")

    def OminousBottle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ominous_bottle")

    def OminousTrialKey() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ominous_trial_key")

    def OpenEyeblossom() -> MinecraftItemDescriptor:
        return item_factory("minecraft:open_eyeblossom")

    def OrangeBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:orange_bundle")

    def OrangeCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:orange_candle")

    def OrangeCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:orange_carpet")

    def OrangeConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:orange_concrete")

    def OrangeConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:orange_concrete_powder")

    def OrangeDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:orange_dye")

    def OrangeGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:orange_glazed_terracotta")

    def OrangeHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:orange_harness")

    def OrangeShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:orange_shulker_box")

    def OrangeStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:orange_stained_glass")

    def OrangeStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:orange_stained_glass_pane")

    def OrangeTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:orange_terracotta")

    def OrangeTulip() -> MinecraftItemDescriptor:
        return item_factory("minecraft:orange_tulip")

    def OrangeWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:orange_wool")

    def OxeyeDaisy() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oxeye_daisy")

    def OxidizedChiseledCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oxidized_chiseled_copper")

    def OxidizedCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oxidized_copper")

    def OxidizedCopperBulb() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oxidized_copper_bulb")

    def OxidizedCopperChest() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oxidized_copper_chest")

    def OxidizedCopperDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oxidized_copper_door")

    def OxidizedCopperGrate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oxidized_copper_grate")

    def OxidizedCopperTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oxidized_copper_trapdoor")

    def OxidizedCutCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oxidized_cut_copper")

    def OxidizedCutCopperSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oxidized_cut_copper_slab")

    def OxidizedCutCopperStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:oxidized_cut_copper_stairs")

    def PackedIce() -> MinecraftItemDescriptor:
        return item_factory("minecraft:packed_ice")

    def PackedMud() -> MinecraftItemDescriptor:
        return item_factory("minecraft:packed_mud")

    def Painting() -> MinecraftItemDescriptor:
        return item_factory("minecraft:painting")

    def PaleHangingMoss() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_hanging_moss")

    def PaleMossBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_moss_block")

    def PaleMossCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_moss_carpet")

    def PaleOakBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_boat")

    def PaleOakButton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_button")

    def PaleOakChestBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_chest_boat")

    def PaleOakDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_door")

    def PaleOakFence() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_fence")

    def PaleOakFenceGate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_fence_gate")

    def PaleOakHangingSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_hanging_sign")

    def PaleOakLeaves() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_leaves")

    def PaleOakLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_log")

    def PaleOakPlanks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_planks")

    def PaleOakPressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_pressure_plate")

    def PaleOakSapling() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_sapling")

    def PaleOakSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_sign")

    def PaleOakSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_slab")

    def PaleOakStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_stairs")

    def PaleOakTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_trapdoor")

    def PaleOakWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pale_oak_wood")

    def PandaSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:panda_spawn_egg")

    def Paper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:paper")

    def ParrotSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:parrot_spawn_egg")

    def PearlescentFroglight() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pearlescent_froglight")

    def Peony() -> MinecraftItemDescriptor:
        return item_factory("minecraft:peony")

    def PetrifiedOakSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:petrified_oak_slab")

    def PhantomMembrane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:phantom_membrane")

    def PhantomSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:phantom_spawn_egg")

    def PigSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pig_spawn_egg")

    def PiglinBannerPattern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:piglin_banner_pattern")

    def PiglinBruteSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:piglin_brute_spawn_egg")

    def PiglinHead() -> MinecraftItemDescriptor:
        return item_factory("minecraft:piglin_head")

    def PiglinSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:piglin_spawn_egg")

    def PillagerSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pillager_spawn_egg")

    def PinkBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_bundle")

    def PinkCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_candle")

    def PinkCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_carpet")

    def PinkConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_concrete")

    def PinkConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_concrete_powder")

    def PinkDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_dye")

    def PinkGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_glazed_terracotta")

    def PinkHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_harness")

    def PinkPetals() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_petals")

    def PinkShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_shulker_box")

    def PinkStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_stained_glass")

    def PinkStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_stained_glass_pane")

    def PinkTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_terracotta")

    def PinkTulip() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_tulip")

    def PinkWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pink_wool")

    def Piston() -> MinecraftItemDescriptor:
        return item_factory("minecraft:piston")

    def PitcherPlant() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pitcher_plant")

    def PitcherPod() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pitcher_pod")

    def PlayerHead() -> MinecraftItemDescriptor:
        return item_factory("minecraft:player_head")

    def PlentyPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:plenty_pottery_sherd")

    def Podzol() -> MinecraftItemDescriptor:
        return item_factory("minecraft:podzol")

    def PointedDripstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pointed_dripstone")

    def PoisonousPotato() -> MinecraftItemDescriptor:
        return item_factory("minecraft:poisonous_potato")

    def PolarBearSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polar_bear_spawn_egg")

    def PolishedAndesite() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_andesite")

    def PolishedAndesiteSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_andesite_slab")

    def PolishedAndesiteStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_andesite_stairs")

    def PolishedBasalt() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_basalt")

    def PolishedBlackstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_blackstone")

    def PolishedBlackstoneBrickSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_blackstone_brick_slab")

    def PolishedBlackstoneBrickStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_blackstone_brick_stairs")

    def PolishedBlackstoneBrickWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_blackstone_brick_wall")

    def PolishedBlackstoneBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_blackstone_bricks")

    def PolishedBlackstoneButton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_blackstone_button")

    def PolishedBlackstonePressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_blackstone_pressure_plate")

    def PolishedBlackstoneSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_blackstone_slab")

    def PolishedBlackstoneStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_blackstone_stairs")

    def PolishedBlackstoneWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_blackstone_wall")

    def PolishedDeepslate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_deepslate")

    def PolishedDeepslateSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_deepslate_slab")

    def PolishedDeepslateStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_deepslate_stairs")

    def PolishedDeepslateWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_deepslate_wall")

    def PolishedDiorite() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_diorite")

    def PolishedDioriteSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_diorite_slab")

    def PolishedDioriteStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_diorite_stairs")

    def PolishedGranite() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_granite")

    def PolishedGraniteSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_granite_slab")

    def PolishedGraniteStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_granite_stairs")

    def PolishedTuff() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_tuff")

    def PolishedTuffSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_tuff_slab")

    def PolishedTuffStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_tuff_stairs")

    def PolishedTuffWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:polished_tuff_wall")

    def PoppedChorusFruit() -> MinecraftItemDescriptor:
        return item_factory("minecraft:popped_chorus_fruit")

    def Poppy() -> MinecraftItemDescriptor:
        return item_factory("minecraft:poppy")

    def Porkchop() -> MinecraftItemDescriptor:
        return item_factory("minecraft:porkchop")

    def Potato() -> MinecraftItemDescriptor:
        return item_factory("minecraft:potato")

    def Potion(
        potion_addition: Literal[
            "water",
            "awkward",
            "mundane",
            "thick",
            "healing",
            "regeneration",
            "swiftness",
            "strength",
            "harming",
            "poison",
            "slowness",
            "weakness",
            "water_breathing",
            "fire_resistance",
            "nightvision",
            "invisibility",
            "leaping",
            "slow_falling",
            "turtle_master",
            "wither",
            "strong_healing",
            "strong_harming",
            "long_leaping",
            "strong_leaping",
            "long_nightvision",
            "long_poison",
            "strong_poison",
            "long_regeneration",
            "strong_regeneration",
            "long_slowness",
            "strong_slowness",
            "long_strength",
            "strong_strength",
            "long_swiftness",
            "strong_swiftness",
            "long_turtle_master",
            "strong_turtle_master",
            "long_water_breathing",
            "long_fire_resistance",
            "long_invisibility",
            "long_slow_falling",
            "long_weakness",
            "strong_wither",
        ] = None,
    ) -> MinecraftItemDescriptor:
        if potion_addition is not None:
            return item_factory("minecraft:potion_type").set_identifier_data(potion_addition)
        return item_factory("minecraft:potion")

    def PowderSnowBucket() -> MinecraftItemDescriptor:
        return item_factory("minecraft:powder_snow_bucket")

    def Prismarine() -> MinecraftItemDescriptor:
        return item_factory("minecraft:prismarine")

    def PrismarineBrickSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:prismarine_brick_slab")

    def PrismarineBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:prismarine_bricks")

    def PrismarineBricksStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:prismarine_bricks_stairs")

    def PrismarineCrystals() -> MinecraftItemDescriptor:
        return item_factory("minecraft:prismarine_crystals")

    def PrismarineShard() -> MinecraftItemDescriptor:
        return item_factory("minecraft:prismarine_shard")

    def PrismarineSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:prismarine_slab")

    def PrismarineStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:prismarine_stairs")

    def PrismarineWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:prismarine_wall")

    def PrizePotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:prize_pottery_sherd")

    def Pufferfish() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pufferfish")

    def PufferfishBucket() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pufferfish_bucket")

    def PufferfishSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pufferfish_spawn_egg")

    def Pumpkin() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pumpkin")

    def PumpkinPie() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pumpkin_pie")

    def PumpkinSeeds() -> MinecraftItemDescriptor:
        return item_factory("minecraft:pumpkin_seeds")

    def PurpleBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purple_bundle")

    def PurpleCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purple_candle")

    def PurpleCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purple_carpet")

    def PurpleConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purple_concrete")

    def PurpleConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purple_concrete_powder")

    def PurpleDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purple_dye")

    def PurpleGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purple_glazed_terracotta")

    def PurpleHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purple_harness")

    def PurpleShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purple_shulker_box")

    def PurpleStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purple_stained_glass")

    def PurpleStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purple_stained_glass_pane")

    def PurpleTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purple_terracotta")

    def PurpleWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purple_wool")

    def PurpurBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purpur_block")

    def PurpurPillar() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purpur_pillar")

    def PurpurSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purpur_slab")

    def PurpurStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:purpur_stairs")

    def Quartz() -> MinecraftItemDescriptor:
        return item_factory("minecraft:quartz")

    def QuartzBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:quartz_block")

    def QuartzBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:quartz_bricks")

    def QuartzOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:quartz_ore")

    def QuartzPillar() -> MinecraftItemDescriptor:
        return item_factory("minecraft:quartz_pillar")

    def QuartzSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:quartz_slab")

    def QuartzStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:quartz_stairs")

    def Rabbit() -> MinecraftItemDescriptor:
        return item_factory("minecraft:rabbit")

    def RabbitFoot() -> MinecraftItemDescriptor:
        return item_factory("minecraft:rabbit_foot")

    def RabbitHide() -> MinecraftItemDescriptor:
        return item_factory("minecraft:rabbit_hide")

    def RabbitSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:rabbit_spawn_egg")

    def RabbitStew() -> MinecraftItemDescriptor:
        return item_factory("minecraft:rabbit_stew")

    def Rail() -> MinecraftItemDescriptor:
        return item_factory("minecraft:rail")

    def RaiserArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:raiser_armor_trim_smithing_template")

    def RavagerSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ravager_spawn_egg")

    def RawCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:raw_copper")

    def RawCopperBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:raw_copper_block")

    def RawGold() -> MinecraftItemDescriptor:
        return item_factory("minecraft:raw_gold")

    def RawGoldBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:raw_gold_block")

    def RawIron() -> MinecraftItemDescriptor:
        return item_factory("minecraft:raw_iron")

    def RawIronBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:raw_iron_block")

    def RecoveryCompass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:recovery_compass")

    def RedBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_bundle")

    def RedCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_candle")

    def RedCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_carpet")

    def RedConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_concrete")

    def RedConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_concrete_powder")

    def RedDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_dye")

    def RedGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_glazed_terracotta")

    def RedHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_harness")

    def RedMushroom() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_mushroom")

    def RedMushroomBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_mushroom_block")

    def RedNetherBrick() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_nether_brick")

    def RedNetherBrickSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_nether_brick_slab")

    def RedNetherBrickStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_nether_brick_stairs")

    def RedNetherBrickWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_nether_brick_wall")

    def RedSand() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_sand")

    def RedSandstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_sandstone")

    def RedSandstoneSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_sandstone_slab")

    def RedSandstoneStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_sandstone_stairs")

    def RedSandstoneWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_sandstone_wall")

    def RedShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_shulker_box")

    def RedStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_stained_glass")

    def RedStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_stained_glass_pane")

    def RedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_terracotta")

    def RedTulip() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_tulip")

    def RedWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:red_wool")

    def Redstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:redstone")

    def RedstoneBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:redstone_block")

    def RedstoneLamp() -> MinecraftItemDescriptor:
        return item_factory("minecraft:redstone_lamp")

    def RedstoneOre() -> MinecraftItemDescriptor:
        return item_factory("minecraft:redstone_ore")

    def RedstoneTorch() -> MinecraftItemDescriptor:
        return item_factory("minecraft:redstone_torch")

    def ReinforcedDeepslate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:reinforced_deepslate")

    def Repeater() -> MinecraftItemDescriptor:
        return item_factory("minecraft:repeater")

    def RepeatingCommandBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:repeating_command_block")

    def ResinBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:resin_block")

    def ResinBrick() -> MinecraftItemDescriptor:
        return item_factory("minecraft:resin_brick")

    def ResinBrickSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:resin_brick_slab")

    def ResinBrickStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:resin_brick_stairs")

    def ResinBrickWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:resin_brick_wall")

    def ResinBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:resin_bricks")

    def ResinClump() -> MinecraftItemDescriptor:
        return item_factory("minecraft:resin_clump")

    def RespawnAnchor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:respawn_anchor")

    def RibArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:rib_armor_trim_smithing_template")

    def RoseBush() -> MinecraftItemDescriptor:
        return item_factory("minecraft:rose_bush")

    def RottenFlesh() -> MinecraftItemDescriptor:
        return item_factory("minecraft:rotten_flesh")

    def Saddle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:saddle")

    def Salmon() -> MinecraftItemDescriptor:
        return item_factory("minecraft:salmon")

    def SalmonBucket() -> MinecraftItemDescriptor:
        return item_factory("minecraft:salmon_bucket")

    def SalmonSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:salmon_spawn_egg")

    def Sand() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sand")

    def Sandstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sandstone")

    def SandstoneSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sandstone_slab")

    def SandstoneStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sandstone_stairs")

    def SandstoneWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sandstone_wall")

    def Scaffolding() -> MinecraftItemDescriptor:
        return item_factory("minecraft:scaffolding")

    def ScrapePotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:scrape_pottery_sherd")

    def Sculk() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sculk")

    def SculkCatalyst() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sculk_catalyst")

    def SculkSensor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sculk_sensor")

    def SculkShrieker() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sculk_shrieker")

    def SculkVein() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sculk_vein")

    def SeaLantern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sea_lantern")

    def SeaPickle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sea_pickle")

    def Seagrass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:seagrass")

    def SentryArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sentry_armor_trim_smithing_template")

    def ShaperArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:shaper_armor_trim_smithing_template")

    def SheafPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sheaf_pottery_sherd")

    def Shears() -> MinecraftItemDescriptor:
        return item_factory("minecraft:shears")

    def SheepSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sheep_spawn_egg")

    def ShelterPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:shelter_pottery_sherd")

    def Shield() -> MinecraftItemDescriptor:
        return item_factory("minecraft:shield")

    def ShortDryGrass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:short_dry_grass")

    def ShortGrass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:short_grass")

    def Shroomlight() -> MinecraftItemDescriptor:
        return item_factory("minecraft:shroomlight")

    def ShulkerShell() -> MinecraftItemDescriptor:
        return item_factory("minecraft:shulker_shell")

    def ShulkerSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:shulker_spawn_egg")

    def SilenceArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:silence_armor_trim_smithing_template")

    def SilverGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:silver_glazed_terracotta")

    def SilverfishSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:silverfish_spawn_egg")

    def SkeletonHorseSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:skeleton_horse_spawn_egg")

    def SkeletonSkull() -> MinecraftItemDescriptor:
        return item_factory("minecraft:skeleton_skull")

    def SkeletonSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:skeleton_spawn_egg")

    def SkullBannerPattern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:skull_banner_pattern")

    def SkullPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:skull_pottery_sherd")

    def Slime() -> MinecraftItemDescriptor:
        return item_factory("minecraft:slime")

    def SlimeBall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:slime_ball")

    def SlimeSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:slime_spawn_egg")

    def SmallAmethystBud() -> MinecraftItemDescriptor:
        return item_factory("minecraft:small_amethyst_bud")

    def SmallDripleafBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:small_dripleaf_block")

    def SmithingTable() -> MinecraftItemDescriptor:
        return item_factory("minecraft:smithing_table")

    def Smoker() -> MinecraftItemDescriptor:
        return item_factory("minecraft:smoker")

    def SmoothBasalt() -> MinecraftItemDescriptor:
        return item_factory("minecraft:smooth_basalt")

    def SmoothQuartz() -> MinecraftItemDescriptor:
        return item_factory("minecraft:smooth_quartz")

    def SmoothQuartzSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:smooth_quartz_slab")

    def SmoothQuartzStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:smooth_quartz_stairs")

    def SmoothRedSandstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:smooth_red_sandstone")

    def SmoothRedSandstoneSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:smooth_red_sandstone_slab")

    def SmoothRedSandstoneStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:smooth_red_sandstone_stairs")

    def SmoothSandstone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:smooth_sandstone")

    def SmoothSandstoneSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:smooth_sandstone_slab")

    def SmoothSandstoneStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:smooth_sandstone_stairs")

    def SmoothStone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:smooth_stone")

    def SmoothStoneSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:smooth_stone_slab")

    def SnifferEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sniffer_egg")

    def SnifferSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sniffer_spawn_egg")

    def SnortPotterySherd() -> MinecraftItemDescriptor:
        return item_factory("minecraft:snort_pottery_sherd")

    def SnoutArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:snout_armor_trim_smithing_template")

    def Snow() -> MinecraftItemDescriptor:
        return item_factory("minecraft:snow")

    def SnowGolemSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:snow_golem_spawn_egg")

    def SnowLayer() -> MinecraftItemDescriptor:
        return item_factory("minecraft:snow_layer")

    def Snowball() -> MinecraftItemDescriptor:
        return item_factory("minecraft:snowball")

    def SoulCampfire() -> MinecraftItemDescriptor:
        return item_factory("minecraft:soul_campfire")

    def SoulLantern() -> MinecraftItemDescriptor:
        return item_factory("minecraft:soul_lantern")

    def SoulSand() -> MinecraftItemDescriptor:
        return item_factory("minecraft:soul_sand")

    def SoulSoil() -> MinecraftItemDescriptor:
        return item_factory("minecraft:soul_soil")

    def SoulTorch() -> MinecraftItemDescriptor:
        return item_factory("minecraft:soul_torch")

    def SpiderEye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spider_eye")

    def SpiderSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spider_spawn_egg")

    def SpireArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spire_armor_trim_smithing_template")

    def SplashPotion() -> MinecraftItemDescriptor:
        return item_factory("minecraft:splash_potion")

    def Sponge() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sponge")

    def SporeBlossom() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spore_blossom")

    def SpruceBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_boat")

    def SpruceButton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_button")

    def SpruceChestBoat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_chest_boat")

    def SpruceDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_door")

    def SpruceFence() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_fence")

    def SpruceFenceGate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_fence_gate")

    def SpruceHangingSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_hanging_sign")

    def SpruceLeaves() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_leaves")

    def SpruceLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_log")

    def SprucePlanks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_planks")

    def SprucePressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_pressure_plate")

    def SpruceSapling() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_sapling")

    def SpruceSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_sign")

    def SpruceSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_slab")

    def SpruceStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_stairs")

    def SpruceTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_trapdoor")

    def SpruceWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spruce_wood")

    def Spyglass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:spyglass")

    def SquidSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:squid_spawn_egg")

    def Stick() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stick")

    def StickyPiston() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sticky_piston")

    def Stone() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stone")

    def StoneAxe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stone_axe")

    def StoneBrickSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stone_brick_slab")

    def StoneBrickStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stone_brick_stairs")

    def StoneBrickWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stone_brick_wall")

    def StoneBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stone_bricks")

    def StoneButton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stone_button")

    def StoneHoe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stone_hoe")

    def StonePickaxe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stone_pickaxe")

    def StonePressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stone_pressure_plate")

    def StoneShovel() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stone_shovel")

    def StoneStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stone_stairs")

    def StoneSword() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stone_sword")

    def StonecutterBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stonecutter_block")

    def StraySpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stray_spawn_egg")

    def StriderSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:strider_spawn_egg")

    def String() -> MinecraftItemDescriptor:
        return item_factory("minecraft:string")

    def StrippedAcaciaLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_acacia_log")

    def StrippedAcaciaWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_acacia_wood")

    def StrippedBambooBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_bamboo_block")

    def StrippedBirchLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_birch_log")

    def StrippedBirchWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_birch_wood")

    def StrippedCherryLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_cherry_log")

    def StrippedCherryWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_cherry_wood")

    def StrippedCrimsonHyphae() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_crimson_hyphae")

    def StrippedCrimsonStem() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_crimson_stem")

    def StrippedDarkOakLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_dark_oak_log")

    def StrippedDarkOakWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_dark_oak_wood")

    def StrippedJungleLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_jungle_log")

    def StrippedJungleWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_jungle_wood")

    def StrippedMangroveLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_mangrove_log")

    def StrippedMangroveWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_mangrove_wood")

    def StrippedOakLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_oak_log")

    def StrippedOakWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_oak_wood")

    def StrippedPaleOakLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_pale_oak_log")

    def StrippedPaleOakWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_pale_oak_wood")

    def StrippedSpruceLog() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_spruce_log")

    def StrippedSpruceWood() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_spruce_wood")

    def StrippedWarpedHyphae() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_warped_hyphae")

    def StrippedWarpedStem() -> MinecraftItemDescriptor:
        return item_factory("minecraft:stripped_warped_stem")

    def StructureBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:structure_block")

    def StructureVoid() -> MinecraftItemDescriptor:
        return item_factory("minecraft:structure_void")

    def Sugar() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sugar")

    def SugarCane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sugar_cane")

    def Sunflower() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sunflower")

    def SuspiciousGravel() -> MinecraftItemDescriptor:
        return item_factory("minecraft:suspicious_gravel")

    def SuspiciousSand() -> MinecraftItemDescriptor:
        return item_factory("minecraft:suspicious_sand")

    def SuspiciousStew() -> MinecraftItemDescriptor:
        return item_factory("minecraft:suspicious_stew")

    def SweetBerries() -> MinecraftItemDescriptor:
        return item_factory("minecraft:sweet_berries")

    def TadpoleBucket() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tadpole_bucket")

    def TadpoleSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tadpole_spawn_egg")

    def TallDryGrass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tall_dry_grass")

    def TallGrass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tall_grass")

    def Target() -> MinecraftItemDescriptor:
        return item_factory("minecraft:target")

    def TideArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tide_armor_trim_smithing_template")

    def TintedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tinted_glass")

    def Tnt() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tnt")

    def TntMinecart() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tnt_minecart")

    def Torch() -> MinecraftItemDescriptor:
        return item_factory("minecraft:torch")

    def Torchflower() -> MinecraftItemDescriptor:
        return item_factory("minecraft:torchflower")

    def TorchflowerSeeds() -> MinecraftItemDescriptor:
        return item_factory("minecraft:torchflower_seeds")

    def TotemOfUndying() -> MinecraftItemDescriptor:
        return item_factory("minecraft:totem_of_undying")

    def TraderLlamaSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:trader_llama_spawn_egg")

    def Trapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:trapdoor")

    def TrappedChest() -> MinecraftItemDescriptor:
        return item_factory("minecraft:trapped_chest")

    def TrialKey() -> MinecraftItemDescriptor:
        return item_factory("minecraft:trial_key")

    def TrialSpawner() -> MinecraftItemDescriptor:
        return item_factory("minecraft:trial_spawner")

    def Trident() -> MinecraftItemDescriptor:
        return item_factory("minecraft:trident")

    def TripwireHook() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tripwire_hook")

    def TropicalFish() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tropical_fish")

    def TropicalFishBucket() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tropical_fish_bucket")

    def TropicalFishSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tropical_fish_spawn_egg")

    def TubeCoral() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tube_coral")

    def TubeCoralBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tube_coral_block")

    def TubeCoralFan() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tube_coral_fan")

    def Tuff() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tuff")

    def TuffBrickSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tuff_brick_slab")

    def TuffBrickStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tuff_brick_stairs")

    def TuffBrickWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tuff_brick_wall")

    def TuffBricks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tuff_bricks")

    def TuffSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tuff_slab")

    def TuffStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tuff_stairs")

    def TuffWall() -> MinecraftItemDescriptor:
        return item_factory("minecraft:tuff_wall")

    def TurtleEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:turtle_egg")

    def TurtleHelmet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:turtle_helmet")

    def TurtleScute() -> MinecraftItemDescriptor:
        return item_factory("minecraft:turtle_scute")

    def TurtleSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:turtle_spawn_egg")

    def TwistingVines() -> MinecraftItemDescriptor:
        return item_factory("minecraft:twisting_vines")

    def UndyedShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:undyed_shulker_box")

    def Vault() -> MinecraftItemDescriptor:
        return item_factory("minecraft:vault")

    def VerdantFroglight() -> MinecraftItemDescriptor:
        return item_factory("minecraft:verdant_froglight")

    def VexArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:vex_armor_trim_smithing_template")

    def VexSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:vex_spawn_egg")

    def VillagerSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:villager_spawn_egg")

    def VindicatorSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:vindicator_spawn_egg")

    def Vine() -> MinecraftItemDescriptor:
        return item_factory("minecraft:vine")

    def WanderingTraderSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wandering_trader_spawn_egg")

    def WardArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:ward_armor_trim_smithing_template")

    def WardenSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warden_spawn_egg")

    def WarpedButton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_button")

    def WarpedDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_door")

    def WarpedFence() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_fence")

    def WarpedFenceGate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_fence_gate")

    def WarpedFungus() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_fungus")

    def WarpedFungusOnAStick() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_fungus_on_a_stick")

    def WarpedHangingSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_hanging_sign")

    def WarpedHyphae() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_hyphae")

    def WarpedNylium() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_nylium")

    def WarpedPlanks() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_planks")

    def WarpedPressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_pressure_plate")

    def WarpedRoots() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_roots")

    def WarpedSign() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_sign")

    def WarpedSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_slab")

    def WarpedStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_stairs")

    def WarpedStem() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_stem")

    def WarpedTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_trapdoor")

    def WarpedWartBlock() -> MinecraftItemDescriptor:
        return item_factory("minecraft:warped_wart_block")

    def WaterBucket() -> MinecraftItemDescriptor:
        return item_factory("minecraft:water_bucket")

    def Waterlily() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waterlily")

    def WaxedChiseledCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_chiseled_copper")

    def WaxedCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_copper")

    def WaxedCopperBulb() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_copper_bulb")

    def WaxedCopperChest() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_copper_chest")

    def WaxedCopperDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_copper_door")

    def WaxedCopperGrate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_copper_grate")

    def WaxedCopperTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_copper_trapdoor")

    def WaxedCutCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_cut_copper")

    def WaxedCutCopperSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_cut_copper_slab")

    def WaxedCutCopperStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_cut_copper_stairs")

    def WaxedExposedChiseledCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_exposed_chiseled_copper")

    def WaxedExposedCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_exposed_copper")

    def WaxedExposedCopperBulb() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_exposed_copper_bulb")

    def WaxedExposedCopperChest() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_exposed_copper_chest")

    def WaxedExposedCopperDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_exposed_copper_door")

    def WaxedExposedCopperGrate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_exposed_copper_grate")

    def WaxedExposedCopperTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_exposed_copper_trapdoor")

    def WaxedExposedCutCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_exposed_cut_copper")

    def WaxedExposedCutCopperSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_exposed_cut_copper_slab")

    def WaxedExposedCutCopperStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_exposed_cut_copper_stairs")

    def WaxedOxidizedChiseledCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_oxidized_chiseled_copper")

    def WaxedOxidizedCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_oxidized_copper")

    def WaxedOxidizedCopperBulb() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_oxidized_copper_bulb")

    def WaxedOxidizedCopperChest() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_oxidized_copper_chest")

    def WaxedOxidizedCopperDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_oxidized_copper_door")

    def WaxedOxidizedCopperGrate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_oxidized_copper_grate")

    def WaxedOxidizedCopperTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_oxidized_copper_trapdoor")

    def WaxedOxidizedCutCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_oxidized_cut_copper")

    def WaxedOxidizedCutCopperSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_oxidized_cut_copper_slab")

    def WaxedOxidizedCutCopperStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_oxidized_cut_copper_stairs")

    def WaxedWeatheredChiseledCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_weathered_chiseled_copper")

    def WaxedWeatheredCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_weathered_copper")

    def WaxedWeatheredCopperBulb() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_weathered_copper_bulb")

    def WaxedWeatheredCopperChest() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_weathered_copper_chest")

    def WaxedWeatheredCopperDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_weathered_copper_door")

    def WaxedWeatheredCopperGrate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_weathered_copper_grate")

    def WaxedWeatheredCopperTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_weathered_copper_trapdoor")

    def WaxedWeatheredCutCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_weathered_cut_copper")

    def WaxedWeatheredCutCopperSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_weathered_cut_copper_slab")

    def WaxedWeatheredCutCopperStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:waxed_weathered_cut_copper_stairs")

    def WayfinderArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wayfinder_armor_trim_smithing_template")

    def WeatheredChiseledCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:weathered_chiseled_copper")

    def WeatheredCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:weathered_copper")

    def WeatheredCopperBulb() -> MinecraftItemDescriptor:
        return item_factory("minecraft:weathered_copper_bulb")

    def WeatheredCopperChest() -> MinecraftItemDescriptor:
        return item_factory("minecraft:weathered_copper_chest")

    def WeatheredCopperDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:weathered_copper_door")

    def WeatheredCopperGrate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:weathered_copper_grate")

    def WeatheredCopperTrapdoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:weathered_copper_trapdoor")

    def WeatheredCutCopper() -> MinecraftItemDescriptor:
        return item_factory("minecraft:weathered_cut_copper")

    def WeatheredCutCopperSlab() -> MinecraftItemDescriptor:
        return item_factory("minecraft:weathered_cut_copper_slab")

    def WeatheredCutCopperStairs() -> MinecraftItemDescriptor:
        return item_factory("minecraft:weathered_cut_copper_stairs")

    def Web() -> MinecraftItemDescriptor:
        return item_factory("minecraft:web")

    def WeepingVines() -> MinecraftItemDescriptor:
        return item_factory("minecraft:weeping_vines")

    def WetSponge() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wet_sponge")

    def Wheat() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wheat")

    def WheatSeeds() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wheat_seeds")

    def WhiteBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:white_bundle")

    def WhiteCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:white_candle")

    def WhiteCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:white_carpet")

    def WhiteConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:white_concrete")

    def WhiteConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:white_concrete_powder")

    def WhiteDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:white_dye")

    def WhiteGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:white_glazed_terracotta")

    def WhiteHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:white_harness")

    def WhiteShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:white_shulker_box")

    def WhiteStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:white_stained_glass")

    def WhiteStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:white_stained_glass_pane")

    def WhiteTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:white_terracotta")

    def WhiteTulip() -> MinecraftItemDescriptor:
        return item_factory("minecraft:white_tulip")

    def WhiteWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:white_wool")

    def WildArmorTrimSmithingTemplate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wild_armor_trim_smithing_template")

    def Wildflowers() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wildflowers")

    def WindCharge() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wind_charge")

    def WitchSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:witch_spawn_egg")

    def WitherRose() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wither_rose")

    def WitherSkeletonSkull() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wither_skeleton_skull")

    def WitherSkeletonSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wither_skeleton_spawn_egg")

    def WitherSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wither_spawn_egg")

    def WolfArmor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wolf_armor")

    def WolfSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wolf_spawn_egg")

    def WoodenAxe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wooden_axe")

    def WoodenButton() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wooden_button")

    def WoodenDoor() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wooden_door")

    def WoodenHoe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wooden_hoe")

    def WoodenPickaxe() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wooden_pickaxe")

    def WoodenPressurePlate() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wooden_pressure_plate")

    def WoodenShovel() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wooden_shovel")

    def WoodenSword() -> MinecraftItemDescriptor:
        return item_factory("minecraft:wooden_sword")

    def WritableBook() -> MinecraftItemDescriptor:
        return item_factory("minecraft:writable_book")

    def YellowBundle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:yellow_bundle")

    def YellowCandle() -> MinecraftItemDescriptor:
        return item_factory("minecraft:yellow_candle")

    def YellowCarpet() -> MinecraftItemDescriptor:
        return item_factory("minecraft:yellow_carpet")

    def YellowConcrete() -> MinecraftItemDescriptor:
        return item_factory("minecraft:yellow_concrete")

    def YellowConcretePowder() -> MinecraftItemDescriptor:
        return item_factory("minecraft:yellow_concrete_powder")

    def YellowDye() -> MinecraftItemDescriptor:
        return item_factory("minecraft:yellow_dye")

    def YellowGlazedTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:yellow_glazed_terracotta")

    def YellowHarness() -> MinecraftItemDescriptor:
        return item_factory("minecraft:yellow_harness")

    def YellowShulkerBox() -> MinecraftItemDescriptor:
        return item_factory("minecraft:yellow_shulker_box")

    def YellowStainedGlass() -> MinecraftItemDescriptor:
        return item_factory("minecraft:yellow_stained_glass")

    def YellowStainedGlassPane() -> MinecraftItemDescriptor:
        return item_factory("minecraft:yellow_stained_glass_pane")

    def YellowTerracotta() -> MinecraftItemDescriptor:
        return item_factory("minecraft:yellow_terracotta")

    def YellowWool() -> MinecraftItemDescriptor:
        return item_factory("minecraft:yellow_wool")

    def ZoglinSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:zoglin_spawn_egg")

    def ZombieHead() -> MinecraftItemDescriptor:
        return item_factory("minecraft:zombie_head")

    def ZombieHorseSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:zombie_horse_spawn_egg")

    def ZombiePigmanSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:zombie_pigman_spawn_egg")

    def ZombieSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:zombie_spawn_egg")

    def ZombieVillagerSpawnEgg() -> MinecraftItemDescriptor:
        return item_factory("minecraft:zombie_villager_spawn_egg")