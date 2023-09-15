[//]: <> (https://squidfunk.github.io/mkdocs-material/reference/)

## Introduction

In this tutorial, we will be creating a new entity called `cube` in the `my_project` project.

## First steps

Open the `my_project.py` file in your project folder. This is the main file of your project, and is where you will be writing your code.

The first thing we need to do is import the `Entity` class from the `api.actors` module.

```py  title="my_project.py" 
from anvil.api.actors import Entity
```

## Creating the entity

Now that we have imported the `Entity` class, we can create our entity.

```py  title="my_project.py"
my_entity = Entity("cube")
```

!!! success 
    This will create a new entity called `cube` in the `my_project` project.

## Adding visuals

Each entity require a geometry and texture to be displayed in-game. We will be using a simple cube geometry and texture for this tutorial.

```py  title="my_project.py"
my_entity.Client.description.geometry("default", "cube")
my_entity.Client.description.texture("default", "cube")
my_entity.Client.description.render_controller("default").geometry("default").texture("default")
```

![Alt text](\\assets\geomtery_format.jpg)

!!!note
    The geometry namespace must follow a specific format. The namespace must be in the format `namespace.geometry_name`, where `namespace` is the namespace of the project, and `geometry_name` is the name of the geometry. This is valid for entities, blocks, attachables...
!!!tip
    The geometries must be saved under `assets/models/entity`
    The textures must be saved under `assets/textures/entity`
!!!failure
    Exporting an entity without any visuals will raise an error.


## Adding Behaviors

Behaviors are used to define the way an entity behaves in the world. In this tutorial, we will be adding a simple behavior that will make the entity move around randomly.

Firstly we need to import the necessary components from the `api.components` module.

```py title="my_project.py"
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

```py title="my_project.py"
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

```python
my_entity.queue("cubes")
```

!!! success 
    The entity will be exported to the `cubes` folder.


## Compiling the project

Now that we have created our entity, we can compile the project. this is the complete code for the `my_project.py` file.

```py title="my_project.py" linenums="1"
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
    my_entity = Entity("my_entity")
    my_entity.Client.description.geometry("default", "cube")
    my_entity.Client.description.texture("default", "cube")
    my_entity.Client.description.render_controller("default").geometry("default").texture("default")
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
    my_entity.queue("cubes")


if __name__ == "__main__":
    create_entity()

    ANVIL.compile
```
!!! note
    Note the use of ANVIL.compile at the end of the file. This is required to compile the project, anything added after this line will not be compiled.
