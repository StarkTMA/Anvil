from click import style
from typing import NewType

Seconds = NewType("Seconds", str)
Molang = NewType("Molang", str)
coordinate = NewType('coordinate', [float | str])
coordinates = NewType('tuple(x, y, z)', tuple[coordinate, coordinate, coordinate])
rotation = NewType('tuple(ry,rx)', tuple[coordinate, coordinate])
level = NewType('tuple(lm,l)', tuple[float, float])
Component = NewType('Component',str)
Identifier = NewType('Identifier',str)
event = NewType('Event',str)

tick = NewType('Tick', int)
_range = NewType('[range]', str)

inf = 99999999999




red = lambda text : style(text, "red")
green = lambda text : style(text, "green")
yellow = lambda text : style(text, "yellow")
cyan = lambda text : style(text, "cyan")

ERROR = red('[Error]')
WARNING = yellow('[Warning]')
PACKAGING = cyan('[Packaging]')

# Actor Client
CLIENT_TYPE_UNSUPPORTED = lambda type, entity : f'{ERROR}: {type} is an unsupported Actor Type, at {entity}.'
# Entity Client
MISSING_MODEL = lambda entity : f'{ERROR}: {green(entity)} missing a geometry.'
MISSING_TEXTURE = lambda entity : f'{ERROR}: {green(entity)} missing a texture.'
MISSING_RENDER_CONTROLLER = lambda entity : f'{ERROR}: {green(entity)} missing a render_controller.'
MISSING_ANIMATION = lambda NAMESPACE, entity, animation : f'{ERROR}: The animation file {green(f"{entity}.animation.json")} doesn\'t contain an animation called {green(NAMESPACE)}.'
LANG_ERROR = lambda text: f'{ERROR}: Invalid localized string at {green(text)}'
SOUND_CATEGORY_ERROR = f'{ERROR}: Invalid sound category.'
MUSIC_CATEGORY_ERROR = f'{ERROR}: Invalid music category.'
DAMAGE_CAUSE_ERROR = f'{ERROR}: Invalid damage cause.'
# Entity Server
MISSING_STATE = lambda identifier, controller, state : f'{WARNING}: {green(identifier)} - {controller} - Missing state "{green(state)}".'
SCORE_ERROR = lambda score: f'{ERROR}: Score objective must be 16 characters, Error at {score}'
FUNCTION_ERROR = lambda type,function: f'{ERROR}: ANVIL.{type}() accepts Function objects only, Error at {function}'
# Dialogues
DIALOGUE_MAX_BUTTONS = lambda scene_tag, buttons_len : f'{ERROR}: The Dialogue scene {scene_tag} has {buttons_len} buttons, The maximum allowed is 6.'

# General
MISSING_FILE = lambda type, file, folder : f'{ERROR}: The {green(type)} with the name {green(file)} cannot be found in {green(folder)}.'
CHECK_UPDATE = green('Checking for updates...')
MODULE = f'{cyan(f"Anvil")} - by Yasser Benfoguhal.'
VERSION = lambda version : f'Version {version}'
COPYRIGHT = lambda year : f'Copyright © {year} {red("StarkTMA")}. All rights reserved.\n\n'
NEW_BUILD = lambda old, new: f'A newer vanilla packages were found. Updating from {old} to {new}'
UP_TO_DATE = 'Packages up to date'
ANVIL_TYPE_ERROR = lambda type : f'{ERROR}:  {type} Is not a valid Anvil Type.'
EXECUTION_TIME = lambda time : f'Execution starts at: {cyan(time)}'
COMPILING = lambda filename : f'{cyan("[Compiling]")}: {green(filename)}               ' + '\033[A'
COMPILATION_TIME = lambda time: f'{cyan("[Compilation Time]")}: {green(time) if time < 15 else red(time)} s.               '
TRANSLATING = lambda filename : f'{cyan("[Translating]")}: {green(filename)}               ' + '\033[A'
TRANSLATION_TIME = lambda time: f'{cyan("[Translation Time]")}: {green(time)} s.               '
EXPORTING = lambda filename : f'{green("[Exporting]")}: {green(filename)}               ' + '\033[A'
NOT_COMPILED = f'{ERROR}: Code must be commpiled before packaging, make sure to run {cyan("ANVIL.compile")}'
PACKAGING_ZIP = f'{PACKAGING}: submission zip...'
PACKAGING_MCADDON = f'{PACKAGING}: .mcaddon'
PACKAGING_MCWORLD = f'{PACKAGING}: .mcworld'
FILE_EXIST_WARNING = lambda filename : f'{WARNING}: {cyan(filename)} does not exist. This will cause validator fails.'
FILE_EXIST_ERROR = lambda filename : f'{ERROR}: {cyan(filename)} does not exist.'
# Identifiers
NAMESPACES_NOT_ALLOWED = lambda identifier : f'{ERROR}: Namespaces are not allowed. {green(identifier)}'

# Molang
MOLANG_ONLY = lambda command : f'{ERROR}: Molang operations only, Error at "{green(command)}".'
