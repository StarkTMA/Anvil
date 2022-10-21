from click import style
import shutil

red = lambda text : style(text, "red")
green = lambda text : style(text, "green")
yellow = lambda text : style(text, "yellow")
cyan = lambda text : style(text, "cyan")

ERROR = red('[Error]')
WARNING = yellow('[Warning]')
# Actor Client
CLIENT_TYPE_UNSUPPORTED = lambda type, entity : f'{ERROR}: {type} is an unsupported Actor Type, at {entity}.'

# Client Entity
MISSING_MODEL = lambda entity : f'{ERROR}: {green(entity)} missing a geometry.'
MISSING_TEXTURE = lambda entity : f'{ERROR}: {green(entity)} missing a texture.'
MISSING_RENDER_CONTROLLER = lambda entity : f'{ERROR}: {green(entity)} missing a render_controller.'
MISSING_ANIMATION = lambda NAMESPACE, entity, animation : f'{ERROR}: The animation file {green(f"{entity}.animation.json")} doesn\'t contain an animation called {green(NAMESPACE)}.'
LANG_ERROR = lambda text: f'{ERROR}: Invalid localized string at {green(text)}'
SOUND_CATEGORY_ERROR = f'{ERROR}: Invalid sound category.'
MUSIC_CATEGORY_ERROR = f'{ERROR}: Invalid music category.'
DAMAGE_CAUSE_ERROR = f'{ERROR}: Invalid damage cause.'
# Server Entity
MISSING_STATE = lambda identifier, controller, state : f'{WARNING}: {green(identifier)} - {controller} - Missing state "{green(state)}".'
SCORE_ERROR = lambda score: f'{ERROR}: Score objective must be 16 characters, Error at {score}'
FUNCTION_ERROR = lambda type,function: f'{ERROR}: ANVIL.{type}() accepts Function objects only, Error at {function}'

# General
MISSING_FILE = lambda type, file, folder : f'{ERROR}: A {green(type)} with the name {green(file)} cannot be found in {green(folder)}.'
CHECK_UPDATE = green('Checking for updates...')
MODULE = f'{cyan(f"Anvil")} - by Yasser Benfoguhal.'
VERSION = lambda version : f'Version {version}'
COPYRIGHT = lambda year : f'Copyright © {year} {red("StarkTMA")}. All rights reserved.\n\n'
NEW_BUILD = lambda old, new: f'A newer vanilla packages were found. Updating from {old} to {new}'
UP_TO_DATE = 'Packages up to date'
ANVIL_TYPE_ERROR = lambda type : f'{ERROR}:  {type} Is not a valid Anvil Type.'

# Identifiers
NAMESPACES_NOT_ALLOWED = lambda identifier : f'{ERROR}: Namespaces are not allowed. {green(identifier)}'

# Molang
MOLANG_ONLY = lambda command : f'{ERROR}: Molang operations only, Error at "{green(command)}".'
