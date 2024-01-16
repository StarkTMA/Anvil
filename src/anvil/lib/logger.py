import logging
from datetime import datetime

import click

from ..__version__ import __version__


class Logger:
    """A class used to log messages to the console and to a log file."""

    @staticmethod
    def Red(text: str):
        return click.style(text, "red")

    @staticmethod
    def Yellow(text: str):
        return click.style(text, "yellow")

    @staticmethod
    def Green(text: str):
        return click.style(text, "green")

    @staticmethod
    def Cyan(text: str):
        return click.style(text, "cyan")

    def __init__(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename="anvil.log",
            filemode="w",
        )
        self.logger = logging.getLogger()

    # Console header
    def header(self):
        click.clear()
        click.echo(
            "\n".join(
                [
                    f"{self.Cyan('Anvil')} - by Yasser A. Benfoughal.",
                    f"Version {self.Cyan(__version__)}.",
                    f"Copyright © {datetime.now().year} {self.Red('StarkTMA')}.",
                    "All rights reserved.",
                    "",
                    "",
                ]
            )
        )

    # ------------------------------------------------------------------------
    # Addon Objects
    # ------------------------------------------------------------------------
    # Info
    def object_initiated(self, name: str):
        self.logger.info(f"Object initiated: {name}.")

    # Info
    def object_queued(self, name: str):
        self.logger.info(f"Object queued: {name}.")

    # Info
    def object_exported(self, name: str):
        self.logger.info(f"Object exported: {name}.")

    # Info
    def new_minecraft_build(self, old, new):
        m = f"A newer vanilla packages were found. Updating from {old} to {new}"
        self.logger.info(m)
        click.echo(m)

    # Info
    def minecraft_build_up_to_date(self):
        m = "Packages up to date"
        self.logger.info(m)
        click.echo(m)

    # Error
    def score_error(self, score):
        m = f"{[self.Red('ERROR')]}: Score objective must be 16 characters, Error at {score}"
        self.logger.error(m)
        raise ValueError(m)

    # Error
    def not_compiled(self):
        m = 'Code must be compiled before packaging, make sure to run "ANVIL.compile"'
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Info
    def packaging_zip(self):
        m = "Packaging submission .zip"
        self.logger.info(m)
        click.echo(self.Cyan(m))

    # Info
    def packaging_mcaddon(self):
        m = "Packaging .mcaddon"
        self.logger.info(m)

    # Info
    def packaging_mcworld(self):
        m = "Packaging .mcworld"
        self.logger.info(m)

    # Warn
    def file_exist_warning(self, filename):
        m = f"{filename} does not exist. This will cause validator fails."
        self.logger.warn(m)
        click.echo(self.Yellow("[WARNING]: " + m))

    # Error
    def file_exist_error(self, filename, directory):
        m = f'{filename} could not be found at "{directory}".'
        self.logger.error(m)
        raise FileNotFoundError(self.Red("[ERROR]: " + m))

    # Error
    def path_length_error(self, path):
        m = f"Relative file path [{path}] has [{len(path)}] characters, but cannot be more than [80] characters."
        self.logger.error(m)
        raise FileNotFoundError(self.Red("[ERROR]: " + m))

    # Error
    def component_version_error(self, component, current_version, target_version):
        m = f"The component [{component}] cannot be used with a format version below {target_version}. Current version is {current_version}."
        self.logger.error(m)
        raise FileNotFoundError(self.Red("[ERROR]: " + m))

    # Error
    def runtime_entity_error(self, entity):
        m = f"Runtime Identifier type must be a [Vanilla.Entities] type. Error at {entity}."
        self.logger.error(m)
        raise TypeError(self.Red("[ERROR]: " + m))

    # Error
    def runtime_entity_not_allowed(self, entity):
        m = f"Entity [{entity}] does not allow runtime identifier usage."
        self.logger.error(m)
        raise TypeError(self.Red("[ERROR]: " + m))

    # Error
    def unsupported_font_size(self):
        m = f"Font character_size must be a multiple of 16."
        self.logger.error(m)
        raise ValueError(self.Red("[ERROR]: " + m))

    # Error
    def unsupported_block_type(self, block):
        m = f"block must be  of a [Blocks] or [str] type. Error at {block}."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def namespace_not_in_geo(self, geo_file, geo_namespace):
        m = f"The geometry file {geo_file}.geo.json doesn't contain a geometry called {geo_namespace}"
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def multiple_rotations(self):
        m = f"Multiple rotation StrEnum were used. A maximum of 1 is allowed."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Warn
    def missing_state(self, target, controller, state):
        m = f'{target} {controller} is missing the animation state "{state}".'
        self.logger.warn(m)
        click.echo(self.Yellow("[WARNING]: " + m))

    # Error
    def dialogue_max_buttons(self, scene_tag, buttons_len):
        m = f"The Dialogue scene {scene_tag} has {buttons_len} buttons, The maximum allowed is 6."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def fog_start_end(self, fog_start, fog_end):
        m = f"fog_end: [{fog_end}] must be greater than fog_start: [{fog_start}]."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def unsupported_model_type(self, model):
        m = f"model must be of a [actors] or [blocks] type. Error at {model}."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def no_geo_found(self, geo):
        m = f"The Geometry file {geo} does not have any geometry."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def no_anim_found(self, anim):
        m = f"The Animation file {anim} does not have any animations."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def client_type_unsupported(self, type, entity):
        m = f"{type} is not a supported Actor Type, error at {entity}."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def namespaces_not_allowed(self, name):
        m = f"Identifiers are not valid name formats, error at {name}."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Info
    def project_missing_config(self):
        m = f"The project require missing configuration. Please fill in the following options:"
        self.logger.info(m)
        click.echo(self.Cyan("[Info]: " + m))

    # Info
    def config_added_option(self, section: str, option: str):
        m = f"{option} was added to {section}"
        self.logger.info(m)
        click.echo(self.Cyan("[Info]: " + m))

    # Info
    def config_option_changeable(self, *options: str):
        m = f"The options {options} can be changed from the config file at any time, recompilation will be required."
        self.logger.info(m)
        click.echo(self.Cyan("[Info]: " + m))

    # Error
    @staticmethod
    def namespace_too_long(namespace):
        m = f"Namespace must be 8 characters or less. {namespace} is {len(namespace)} characters long."
        raise ValueError(Logger.Red("[ERROR]: " + m))

    # Error
    @staticmethod
    def reserved_namespace(namespace):
        m = f"{namespace} is a reserved namespace and cannot be used."
        raise ValueError(Logger.Red("[ERROR]: " + m))

    # Error
    @staticmethod
    def unique_namespace(namespace):
        m = f"Every namespace must be unique to the pack. For this pack it should be {namespace}."
        raise ValueError(Logger.Red("[ERROR]: " + m))

    # Error
    @staticmethod
    def project_name_too_long(project_name):
        m = f"Project name must be 16 characters or less. {project_name} is {len(project_name)} characters long."
        raise ValueError(Logger.Red("[ERROR]: " + m))

    # Error
    def missing_animation(self, animation_path, animation):
        m = f"{animation_path} is missing the animation {animation}"
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def entity_missing_texture(self, entity):
        m = f"{entity} has no textures added."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def block_missing_texture(self, block):
        m = f"{block} has no default material instance added."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def block_missing_geometry(self, block):
        m = f"{block} has no default geometry added."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def block_state_values_out_of_range(self, block, state, values):
        m = f"Block states cannot have more than 16 values. {block} state [{state}] has {values} values."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    def missing_render_controller(self, entity):
        m = f"[{entity}] is missing a render_controller"
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))
    
    def missing_geometry(self, entity):
        m = f"[{entity}] is missing a geometry"
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))
    
    def missing_texture(self, entity):
        m = f"[{entity}] is missing a texture"
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))
    
    def lang_error(self, text):
        m = f"Invalid localized string at {text}"
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    def sound_category_error(self):
        m = f"Invalid sound category"
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    def music_category_error(self):
        m = f"Invalid music category"
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    def damage_cause_error(self):
        m = f"Invalid damage cause"
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # General
    def check_update(self):
        m = f"Checking for updates..."
        self.logger.info(m)

    def anvil_type_error(self, type):
        m = f"{type} Is not a valid Anvil Type."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Molang
    def molang_only(self, command):
        m = f"Molang operations only, Error at {command}"
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def digits_not_allowed(self, identifier):
        m = f"Names starting with a digit are not allowed {identifier}."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def runtime_not_allowed(self, identifier):
        m = f"runtime_identifer is not allowed for packages of type : 'addon'. Error at {identifier}."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def invalid_target(self, target):
        m = f"Package target must only be one of ['world', 'addon'], Error at {target}."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def experimental_not_allowed(self, identifier):
        m = f"Experimental features are not allowed for packages of type : 'addon'. Error at {identifier}."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))
    
    # Warn
    def entity_marked_as_experimental(self, identifier):
        m = f"Entity {identifier} is marked as experimental. This may be unintentional."
        self.logger.warn(m)
        click.echo(self.Yellow("[WARNING]: " + m))
    
    # Error
    def too_many_permutations(self, count):
        m = f"Total Block permutations exceeded 10000 ({count}). For minimal performance impact, reduce the number of permutations."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))
    
    # Warn
    def too_many_permutations_warn(self, count):
        m = f"Total Block permutations exceeded 10000 ({count}). For minimal performance impact, consider reducing the number of permutations."
        self.logger.warn(m)
        click.echo(self.Yellow("[WARNING]: " + m))

    # Error
    def multiple_rp_uuids(self, identifier):
        m = f"Multiple resource pack uuids found. Error at {identifier}."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))
    
    # Error
    def multiple_bp_uuids(self, identifier):
        m = f"Multiple behavior pack uuids found. Error at {identifier}."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def vanilla_override_error(self, identifier):
        m = f"Overriding vanilla features is not allowed for packages of type : 'addon'. Error at {identifier}."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def invalid_score_format(self, start, score):
        m = f"Scores must start with the namespace [{start}]. Error at {score}. Consider using 'ANVIL.definitions.get_new_score' to dynamically get unique scores."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def invalid_tag_format(self, start, tag):
        m = f"Tags must start with the namespace [{start}]. Error at {tag}."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))

    # Error
    def component_required(self, identifier, requirer, required):
        m = f"The component {requirer} requires the component {required} to be added to {identifier}."
        self.logger.error(m)
        raise RuntimeError(self.Red("[ERROR]: " + m))