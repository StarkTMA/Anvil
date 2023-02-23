from github import Github

from .packages import *
from .packages import __version__


@click.group()
def cli(): pass

@cli.command(help='Initiate an Anvil project')
@click.argument('namespace')
@click.argument('project_name')
@click.option('--preview', is_flag=True, default=False, show_default=True, help="Generates the project in Minecraft Preview com.mojang instead of release.")
@click.option('--fullns', is_flag=True, default=False, show_default=True, help="Sets the Project namespace to the full NAMESPACE.PROJECT_NAME")
def create(namespace:str, project_name:str, preview:bool=False, fullns: bool = False):
    header()
    if len(namespace) > 8:
        RaiseError(click.style("Namespace must be 4 characters or less.", fg='red'))

    if len(project_name) > 16:
        RaiseError(click.style("Project name must be 16 characters or less.", fg='red'))

    global COMPANY
    global LATEST_BUILD
    global DISPLAY_NAME
            
    COMPANY = namespace.title()
    DISPLAY_NAME = project_name.title().replace("-"," ").replace("_"," ")
    PASCAL_PROJECT_NAME = ''.join(x for x in DISPLAY_NAME if x.isupper())
    github = Github().get_repo('Mojang/bedrock-samples')

    click.echo(f'Initiating {DISPLAY_NAME}')
    if preview:
        target = 'Microsoft.MinecraftWindowsBeta_8wekyb3d8bbwe'
        LATEST_BUILD = json.loads(github.get_contents('version.json', 'preview').decoded_content.decode())['latest']['version']
    else:
        target = 'Microsoft.MinecraftUWP_8wekyb3d8bbwe'
        LATEST_BUILD = json.loads(github.get_contents('version.json', 'main').decoded_content.decode())['latest']['version']

    BASE_DIR = MakePath(APPDATA,'Local','Packages',target,'LocalState','games','com.mojang','minecraftWorlds')
    os.chdir(BASE_DIR)

    project_structure = Schemes('structure', project_name)
    CreateDirectoriesFromTree(project_structure)
    File(f'{project_name}.anvil.py', Schemes('script'), project_name, "w")

    File('.gitignore', Schemes('gitignore'), project_name, "w")

    CONFIG.set('ANVIL', 'COMPANY', namespace.title())
    CONFIG.set('ANVIL', 'NAMESPACE', namespace)
    CONFIG.set('ANVIL', 'PROJECT_NAME', project_name)
    CONFIG.set('ANVIL', 'DISPLAY_NAME', DISPLAY_NAME)
    CONFIG.set('ANVIL', 'PASCAL_PROJECT_NAME', PASCAL_PROJECT_NAME)
    CONFIG.set('ANVIL', 'PROJECT_DESCRIPTION', f'{CONFIG.get("ANVIL", "DISPLAY_NAME")} Essentials')
    CONFIG.set('ANVIL', 'VANILLA_VERSION', LATEST_BUILD)
    CONFIG.set('ANVIL', 'LAST_CHECK', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    CONFIG.set('ANVIL', 'NAMESPACE_FORMAT', int(fullns is True))
    CONFIG.set('ANVIL', 'BUILD', 'preview' if preview else 'main')
    CONFIG.set('ANVIL', 'DEBUG', 'false')

    File("en_US.lang", Schemes('language', project_name, project_name),MakePath(project_name,'behavior_packs',f'BP_{PASCAL_PROJECT_NAME}','texts'), "w")
    File("en_US.lang", Schemes('language', project_name, project_name),MakePath(project_name,'resource_packs',f'RP_{PASCAL_PROJECT_NAME}','texts'), "w")
    File("manifest.json", Schemes('manifest_bp'),MakePath(project_name,'behavior_packs',f'BP_{PASCAL_PROJECT_NAME}'), "w")
    File("manifest.json", Schemes('manifest_rp'),MakePath(project_name,'resource_packs',f'RP_{PASCAL_PROJECT_NAME}'), "w")
    File(f'{project_name}.code-workspace', Schemes('code-workspace',BASE_DIR,project_name,COMPANY),DESKTOP, "w")

    with open(MakePath(project_name,'behavior_packs',f'BP_{PASCAL_PROJECT_NAME}','manifest.json')) as file:
        data = json.load(file)
        uuid = data["header"]["uuid"]
        version = data["header"]["version"]
        File("world_behavior_packs.json", Schemes('world_packs',uuid,version), project_name, "w")
    with open(MakePath(project_name,'resource_packs',f'RP_{PASCAL_PROJECT_NAME}','manifest.json')) as file:
        data = json.load(file)
        uuid = data["header"]["uuid"]
        version = data["header"]["version"]
        File("world_resource_packs.json", Schemes('world_packs',uuid,version), project_name, "w")
    
    code_wkspc = f'{project_name}.code-workspace'
    os.chdir(project_name)
    CONFIG.save()
    os.system(f'start {MakePath(BASE_DIR,project_name)}')
    os.system(f'start {MakePath(DESKTOP,code_wkspc)}')
