## Introduction

In this tutorial, we will be creating a new entity called `skin_humanoid` in the `awesome_project` project.

## First steps

Open the `awesome_project.py` file in your project folder. This is the main file of your project, and is where you will be writing your code.

The first thing we need to do is import the `Entity` class from the `api.actors` module.

```python title="awesome_project.py"
from anvil.api.actors import Entity
```

## Creating the entity

Now that we have imported the `Entity` class, we can create our entity.

```python title="awesome_project.py"
my_entity = Entity("skin_humanoid")
```

!!! success
    This will create a new entity called `skin_humanoid` in the `awesome_project` project.

## Adding visuals

Each entity require a geometry and texture to be displayed in-game. We will be using a simple skin_humanoid geometry and texture for this tutorial.

Anvil integrates blockbench into the development workflow, all of your entity assets, the geometry with it's textures and animations should be saved in a bbmodel file in the `assets/bbmodels` folder.

```python title="awesome_project.py"
my_entity.Client.description.geometry("skin_humanoid")
my_entity.Client.description.texture("skin_humanoid", "skin_ace")
my_entity.Client.description.render_controller("default").geometry("skin_humanoid").textures("skin_ace")
```

![Alt text](\assets\bbmodel_setup.png)

!!!note
    We referenced `skin_humanoid` as the blockbench name, Anvil will expect a file named `skin_humanoid.bbmodel` in the `assets/bbmodels` folder with the model identifier of the same name.

!!!note
    We referenced `skin_humanoid` as the blockbench name and `skin_ace` as the texture name, Anvil will expect a file named `skin_humanoid.bbmodel` in the `assets/bbmodels` folder with the model identifier of the same name and a texture named `skin_ace`.

!!!failure
    Exporting an entity without any visuals will raise an error.

## Adding Behaviors

Behaviors are used to define the way an entity behaves in the world. In this tutorial, we will be adding a simple behavior that will make the entity move around randomly.

Firstly we need to import the necessary components from the `api.components` module.

```python title="awesome_project.py"
from anvil.api.components import (
    JumpStatic,
    MovementType,
    NavigationType,
    Movement,
    Physics,
    KnockbackResistance,
    Health,
    CollisionBox,
    Breathable,
    DamageSensor,
    Pushable,
    PushThrough,
)
```

```python title="awesome_project.py"
my_entity.Server.components.add(
    JumpStatic(0),
    MovementType().Basic(),
    NavigationType().Walk(),
    Movement(0.1),
    Physics(True, True),
    KnockbackResistance(10000),
    Health(6),
    CollisionBox(1, 1),
    Breathable(),
    DamageSensor().add_trigger(DamageCause.All, False),
    Pushable(False, False),
    PushThrough(1),
)
```

!!! success
    The entity will now move around randomly.

## Exporting the entity

Now that we have created our entity, we can export it to our project. Anvil follows a queue system for exporting everything. It allows Anvil to do extra processing before exporting, such as validation, translation, and more.

It is done by calling the `queue` method on the entity, and optionally passing a folder name to export to.

```python title="awesome_project.py"
my_entity.queue("humanoids")
```

!!! success
    The entity will be exported to the `humanoids` folder.

## Compiling the project

Now that we have created our entity, we can compile the project. this is the complete code for the `awesome_project.py` file.

```python title="awesome_project.py" linenums="1"
from anvil import *
from anvil.api.actors import Entity
from anvil.api.components import (
    JumpStatic,
    MovementType,
    NavigationType,
    Movement,
    Physics,
    KnockbackResistance,
    Health,
    CollisionBox,
    Breathable,
    DamageSensor,
    Pushable,
    PushThrough,
)

def create_entity():
    my_entity = Entity("skin_humanoid")
    my_entity.Client.description.geometry("skin_humanoid")
    my_entity.Client.description.texture("skin_humanoid", "skin_ace")
    my_entity.Client.description.render_controller("default").geometry("skin_humanoid").textures("skin_ace")
    my_entity.Server.components.add(
        JumpStatic(0),
        MovementType().Basic(),
        NavigationType().Walk(),
        Movement(0.1),
        Physics(True, True),
        KnockbackResistance(10000),
        Health(6),
        CollisionBox(1, 1),
        Breathable(),
        DamageSensor().add_trigger(DamageCause.All, False),
        Pushable(False, False),
        PushThrough(1),
    )
    my_entity.queue("humanoids")


if __name__ == "__main__":
    create_entity()

    ANVIL.compile()
```

!!! note
    Note the use of ANVIL.compile() at the end of the file. This is required to compile the project, anything added after this line will not be compiled.
