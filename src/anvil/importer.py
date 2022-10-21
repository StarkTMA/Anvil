import commentjson as js

def sound_definition():
    with open('sound_definitions.json', 'r') as file:
        with open('b.py', 'w+') as file2:
            data = js.loads(file.read())
            file2.write('from anvil import *\n')
            for definition, definition_content in data['sound_definitions'].items():
                line = ''
                line += f"Sound('{definition}'"
                if 'category' in definition_content:
                    line += f", '{definition_content['category']}'"
                else:
                    line += f", 'ui'"

                if 'max_distance' in definition_content:
                    line += f", max_distance={definition_content['max_distance']}"

                if 'min_distance' in definition_content:
                    line += f", min_distance={definition_content['min_distance']}"
                line += ")"
                for sound in definition_content['sounds']:
                    filename = sound['name'].split("/")[-1]
                    line += "\\\n"
                    line += f"   .add_sound('{filename}'"
                    if 'volume' in sound:
                        line += f", volume={sound['volume']}"
                    if 'weight' in sound:
                        line += f", weight={sound['weight']}"
                    if 'pitch' in sound:
                        line += f", pitch={sound['pitch']}"
                    if 'is_3d' in sound:
                        line += f", is_3d={sound['is_3d']}"
                    if 'stream' in sound:
                        line += f", stream={sound['stream']}"
                    if 'load_on_low_memory' in sound:
                        line += f", load_on_low_memory={sound['load_on_low_memory']}"
                    line += ")"

                line += "\\\n"
                line += f"   .queue"
                file2.write(line + '\n')