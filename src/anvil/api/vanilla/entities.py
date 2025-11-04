from anvil.lib.schemas import MinecraftEntityDescriptor

entity_factory = lambda identifier: MinecraftEntityDescriptor(identifier)


class MinecraftEntityTypes:
    def Agent() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:agent")

    def Allay() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:allay")

    def AreaEffectCloud() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:area_effect_cloud")

    def Armadillo() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:armadillo")

    def ArmorStand() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:armor_stand")

    def Arrow() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:arrow")

    def Axolotl() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:axolotl")

    def Bat() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:bat")

    def Bee() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:bee")

    def Blaze() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:blaze")

    def Boat() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:boat")

    def Bogged() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:bogged")

    def Breeze() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:breeze")

    def BreezeWindChargeProjectile() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:breeze_wind_charge_projectile")

    def Camel() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:camel")

    def Cat() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:cat")

    def CaveSpider() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:cave_spider")

    def ChestBoat() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:chest_boat")

    def ChestMinecart() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:chest_minecart")

    def Chicken() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:chicken")

    def Cod() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:cod")

    def CommandBlockMinecart() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:command_block_minecart")

    def CopperGolem() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:copper_golem")

    def Cow() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:cow")

    def Creaking() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:creaking")

    def Creeper() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:creeper")

    def Dolphin() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:dolphin")

    def Donkey() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:donkey")

    def DragonFireball() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:dragon_fireball")

    def Drowned() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:drowned")

    def Egg() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:egg")

    def ElderGuardian() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:elder_guardian")

    def EnderCrystal() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:ender_crystal")

    def EnderDragon() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:ender_dragon")

    def EnderPearl() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:ender_pearl")

    def Enderman() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:enderman")

    def Endermite() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:endermite")

    def EvocationIllager() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:evocation_illager")

    def EyeOfEnderSignal() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:eye_of_ender_signal")

    def Fireball() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:fireball")

    def FireworksRocket() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:fireworks_rocket")

    def FishingHook() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:fishing_hook")

    def Fox() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:fox")

    def Frog() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:frog")

    def Ghast() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:ghast")

    def GlowSquid() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:glow_squid")

    def Goat() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:goat")

    def Guardian() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:guardian")

    def HappyGhast() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:happy_ghast")

    def Hoglin() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:hoglin")

    def HopperMinecart() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:hopper_minecart")

    def Horse() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:horse")

    def Husk() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:husk")

    def IronGolem() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:iron_golem")

    def LightningBolt() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:lightning_bolt")

    def LingeringPotion() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:lingering_potion")

    def Llama() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:llama")

    def LlamaSpit() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:llama_spit")

    def MagmaCube() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:magma_cube")

    def Minecart() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:minecart")

    def Mooshroom() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:mooshroom")

    def Mule() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:mule")

    def Npc() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:npc")

    def Ocelot() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:ocelot")

    def OminousItemSpawner() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:ominous_item_spawner")

    def Panda() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:panda")

    def Parrot() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:parrot")

    def Phantom() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:phantom")

    def Pig() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:pig")

    def Piglin() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:piglin")

    def PiglinBrute() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:piglin_brute")

    def Pillager() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:pillager")

    def Player() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:player")

    def PolarBear() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:polar_bear")

    def Pufferfish() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:pufferfish")

    def Rabbit() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:rabbit")

    def Ravager() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:ravager")

    def Salmon() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:salmon")

    def Sheep() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:sheep")

    def Shulker() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:shulker")

    def ShulkerBullet() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:shulker_bullet")

    def Silverfish() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:silverfish")

    def Skeleton() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:skeleton")

    def SkeletonHorse() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:skeleton_horse")

    def Slime() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:slime")

    def SmallFireball() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:small_fireball")

    def Sniffer() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:sniffer")

    def SnowGolem() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:snow_golem")

    def Snowball() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:snowball")

    def Spider() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:spider")

    def SplashPotion() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:splash_potion")

    def Squid() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:squid")

    def Stray() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:stray")

    def Strider() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:strider")

    def Tadpole() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:tadpole")

    def ThrownTrident() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:thrown_trident")

    def Tnt() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:tnt")

    def TntMinecart() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:tnt_minecart")

    def TraderLlama() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:trader_llama")

    def TripodCamera() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:tripod_camera")

    def Tropicalfish() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:tropicalfish")

    def Turtle() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:turtle")

    def Vex() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:vex")

    def Villager() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:villager")

    def VillagerV2() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:villager_v2")

    def Vindicator() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:vindicator")

    def WanderingTrader() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:wandering_trader")

    def Warden() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:warden")

    def WindChargeProjectile() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:wind_charge_projectile")

    def Witch() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:witch")

    def Wither() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:wither")

    def WitherSkeleton() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:wither_skeleton")

    def WitherSkull() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:wither_skull")

    def WitherSkullDangerous() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:wither_skull_dangerous")

    def Wolf() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:wolf")

    def XpBottle() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:xp_bottle")

    def XpOrb() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:xp_orb")

    def Zoglin() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:zoglin")

    def Zombie() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:zombie")

    def ZombieHorse() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:zombie_horse")

    def ZombiePigman() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:zombie_pigman")

    def ZombieVillager() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:zombie_villager")

    def ZombieVillagerV2() -> MinecraftEntityDescriptor:
        return entity_factory("minecraft:zombie_villager_v2")
