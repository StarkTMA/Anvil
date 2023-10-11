[//]: <> (https://squidfunk.github.io/mkdocs-material/reference/)

## Introduction
Creating a One Block SkyBlock map can be a repetitive task that involves writing a lot of functions and commands. This tutorial will guide you through the process of creating a One Block SkyBlock map with Anvil in more productive, extensible and maintainable way.

let's first start by creating a new project.

```bash
anvil create starktma oneblock
```

## Overworld
The first step is to create the overworld system. The overworld system is responsible for generating the one block island and the player's spawn point. The more the player mines blocks the more blocks they unlock.

```py title="oneblock.py"
def over_block_place():
    overworld_step = 100
```
!!! info
    We've taken 100 blocks as the interval at which new tiers of blocks unlock.

We will create a list of lists, where each list contains the blocks players unlock at each 100 mined block.

The first list will be available from the start of the game, the second list will be available after mining 100 blocks, the third list will be available after mining 200 blocks and so on.


```py title="oneblock.py"
from anvil.api.vanilla import Blocks, BlockStates

def over_block_place():
    overworld_step = 100
    overworld_block = [
        [Blocks.Grass()],
        [Blocks.AcaciaLog(), Blocks.BirchLog(), Blocks.DarkOakLog(), Blocks.JungleLog(), Blocks.MangroveLog(), Blocks.OakLog(), Blocks.SpruceLog()],
        [
            Blocks.Stone(BlockStates.StoneType.ANDESITE),
            Blocks.Stone(BlockStates.StoneType.DIORITE),
            Blocks.Stone(BlockStates.StoneType.GRANITE),
            Blocks.Stone(BlockStates.StoneType.STONE),
        ],
        [Blocks.MobSpawner()],
        [Blocks.CoalOre()],
        [Blocks.Snow()],
        [Blocks.RedstoneOre()],
        [Blocks.Clay()],
        [Blocks.IronOre()],
        [Blocks.Ice()],
        [Blocks.Sand(BlockStates.SandType.NORMAL)],
        [Blocks.Sand(BlockStates.SandType.RED)],
        [Blocks.CopperOre()],
        [Blocks.Gravel()],
        [Blocks.EmeraldOre()],
        [Blocks.BrownMushroomBlock()],
        [Blocks.RedMushroomBlock()],
        [Blocks.GoldOre()],
        [Blocks.Podzol()],
        [Blocks.DiamondOre()],
        [Blocks.Obsidian()],
        [Blocks.LapisOre()],
        [Blocks.Mycelium()],
    ]
```

!!! info
    We've only used Vanilla blocks for this example, Anvil supports all vanilla blocks with their states.
    
Now that we have the blocks, we need to place them in the world. For that, we'll need an `mcfunction` that runs on loop and places the blocks based on the mined amount.

We will be using `mined_over` score to track the blocks.

```py title="oneblock.py"
def over_block_place():
    ANVIL.score(mined_over=0)
    overworld_setter = Function("overworld_setter")
    overworld_setter.add(
        Scoreboard().players.add(PROJECT_NAME, "mined_over", 1),
        Teleport(Selector(Target.E).distance(r=1), ("~", "~1", "~")),
    )
    overworld_setter.queue("misc")
```
!!! note
    It is advised to register the scores to Anvil so that can be easily reset and removed through the built in setup function. `/function setup`.

We will also implement a chance system that uniformly picks of the unlocked blocks to place back. This will make the map more interesting and less predictable.
We will be using the `over_chance` to randomly pick a block to place.

```py title="oneblock.py"
def over_block_place():
    ANVIL.score(over_chance=0)
    chance = 0
    for i, group in enumerate(overworld_block):
        chance += len(group)
        overworld_setter.add(
            Execute()
            .If.ScoreMatches(
                PROJECT_NAME,
                "mined_over",
                f"{i*overworld_step+1}..{overworld_step * (i+1)}",
            )
            .run(Scoreboard().players.random(PROJECT_NAME, "over_chance", 0, chance - 1))
        )

        for j, block in enumerate(group):
            overworld_setter.add(
                Execute().If.ScoreMatches(PROJECT_NAME, "over_chance", chance - len(group) + j).run(Setblock(block)),
            )
    return overworld_setter
```
!!! info
    The function `over_block_place()` returns the function overworld_setter which is the function that places the blocks in the world. This will be used at a later point.


## Nether
Similar to what we've done in the overword, we will start by defining the list of our blocks, the interval at which new blocks unlock and the score that tracks the mined blocks.
    
```py title="oneblock.py"
def nether_block_place():
    nether_step = 100
    nether_block = [
        [Blocks.CrimsonStem(), Blocks.WarpedStem()],
        [Blocks.Netherrack()],
        [
            Blocks.Blackstone(),
            Blocks.NetherGoldOre(),
            Blocks.Basalt(),
            Blocks.SoulSand(),
            Blocks.QuartzOre(),
            Blocks.CrimsonNylium(),
            Blocks.WarpedNylium(),
            Blocks.Shroomlight(),
        ],
        [Blocks.SoulSoil()],
        [Blocks.MobSpawner()],
        [Blocks.Magma()],
        [Blocks.NetherWartBlock()],
        [Blocks.WarpedWartBlock()],
        [Blocks.AncientDebris()],
    ]

    nether_setter = (
        Function("nether_setter")
        .add(
            Scoreboard().players.add(PROJECT_NAME, "mined_nether", 1),
            Teleport(Selector(Target.E).distance(r=1), ("~", "~1", "~")),
        )
        .queue("misc")
    )
    chance = 0
    for i, group in enumerate(nether_block):
        chance += len(group)
        nether_setter.add(
            Execute()
            .If.ScoreMatches(
                PROJECT_NAME,
                "mined_nether",
                f"{i*nether_step+1}..{nether_step * (i+1)}",
            )
            .run(Scoreboard().players.random(PROJECT_NAME, "nether_chance", 0, chance - 1))
        )

        for j, block in enumerate(group):
            nether_setter.add(
                Execute().If.ScoreMatches(PROJECT_NAME, "nether_chance", chance - len(group) + j).run(Setblock(block)),
            )

    return nether_setter
```

## Game Loop

Now that we have the functions that place the blocks in the world, we need to create a game loop that runs on loop and calls the functions.

We will be using StateMachine, a built in class that manages players, levels and states.

```py title="oneblock.py"
from anvil.tools.functions import StateMachine
from anvil.api.commands import Execute, Scoreboard, Setblock, Teleport

def state_machine():
    state_machine = StateMachine()
    level_1 = state_machine.add_main_level()
    level_1.init_world.add(
        Execute().In(Dimension.Overworld).Positioned((0, 70, 0)).run(Setblock(Blocks.Grass())),
        Execute().In(Dimension.Nether).Positioned((0, 70, 0)).run(Setblock(Blocks.CrimsonStem())),
    )
    level_1.game_loop.add(
        Execute().In(Dimension.Overworld).Positioned((0, 70, 0)).If.Block(("~", "~", "~"), Blocks.Air()).run(over_block_place().execute),
        Execute().In(Dimension.Nether).Positioned((0, 70, 0)).If.Block(("~", "~", "~"), Blocks.Air()).run(nether_block_place().execute),
    )
    state_machine.queue
```
!!! note
    Notice how we're calling `.execute` on both `over_block_place()` and `nether_block_place()`.

!!! info
    The StateMachine ticks by default, more on the StateMachine [here]("../adding_your_first_entity").

## Compiling
Now that we have the entire game Logic, we need to compile it and package it into an mcworld.

```py title="oneblock.py"
if __name__ == "__main__":
    state_machine()

    ANVIL.compile()
    ANVIL.mcworld()
```