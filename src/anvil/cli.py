from .packages import *
from .packages import __version__

@click.group()
def cli(): pass


@cli.command(help='Initiate an Anvil project')
@click.argument('namespace')
@click.argument('project_name')
@click.option('--preview', is_flag=True, default=False, show_default=True, help="Generates the project in Minecraft Preview com.mojang instead of release.")
@click.option('--skip', is_flag=True, default=False, show_default=True, help="Skips downloading the Vanilla packs. Unrecommended")
@click.option('--fullns', is_flag=True, default=False, show_default=True, help="Sets the Project namespace to the full NAMESPACE.PROJECT_NAME")
def create(namespace:str, project_name:str, preview:bool=False, skip: bool = False, fullns: bool = False):
    header()
    if len(namespace) > 8:
        RaiseError(click.style("Namespace must be 4 characters or less.", fg='red'))

    if len(project_name) > 16:
        RaiseError(click.style("Project name must be 16 characters or less.", fg='red'))

    global COMPANY
    global LATEST_BUILD
    PASCAL_PROJECT_NAME = ''.join(x for x in project_name.title().replace('_', '').replace('-', '') if x.isupper())
            
    COMPANY = namespace.title()
    LATEST_BUILD = request.urlopen(BP).url.split('/')[-1].lstrip('Vanilla_Behavior_Pack_').rstrip('.zip')

    click.echo(f'Initiating {project_name.title().replace("-"," ").replace("_"," ")}')
    if preview:
        target = 'Microsoft.MinecraftWindowsBeta_8wekyb3d8bbwe'
    else:
        target = 'Microsoft.MinecraftUWP_8wekyb3d8bbwe'
    BASE_DIR = MakePath(APPDATA,'Local','Packages',target,'LocalState','games','com.mojang','minecraftWorlds')
    os.chdir(BASE_DIR)

    project_structure = Schemes('structure', project_name)
    CreateDirectoriesFromTree(project_structure)
    File(f'{project_name}.anvil.py', Schemes('script'), project_name, "w")
    File("config.json", Schemes('config', namespace,namespace,project_name,project_name,f'{project_name}_essentials',LATEST_BUILD, fullns is True), project_name, "w")
    
    File("en_US.lang", Schemes('language', project_name, project_name),MakePath(project_name,'behavior_packs',f'BP_{PASCAL_PROJECT_NAME}','texts'), "w")
    File("en_US.lang", Schemes('language', project_name, project_name),MakePath(project_name,'resource_packs',f'RP_{PASCAL_PROJECT_NAME}','texts'), "w")
    File("manifest.json", Schemes('manifest_bp'),MakePath(project_name,'behavior_packs',f'BP_{PASCAL_PROJECT_NAME}'), "w")
    File("manifest.json", Schemes('manifest_rp'),MakePath(project_name,'resource_packs',f'RP_{PASCAL_PROJECT_NAME}'), "w")
    File(f'{project_name}.code-workspace', Schemes('code-workspace',BASE_DIR,project_name),DESKTOP, "w")
    
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
    
    if not skip:
        
        DownloadFile(BP,MakePath(project_name,'assets','vanilla','BP.zip'), "Behavior")
        DownloadFile(RP,MakePath(project_name,'assets','vanilla','RP.zip'), "Resource")
    code_wkspc = f'{project_name}.code-workspace'
    os.system(f'start {MakePath(BASE_DIR,project_name)}')
    os.system(f'start {MakePath(DESKTOP,code_wkspc)}')
