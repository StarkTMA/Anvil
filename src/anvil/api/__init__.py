from configparser import ConfigParser

class _config:
    def __init__(self) -> None:
        self._config = ConfigParser()
        self._config.read('config.ini')

    def save(self):
        with open("config.ini", "w") as f:
            self._config.write(f)

    def set(self, section, option, value):
        if not self._config.has_section(section):
            self._config.add_section(section)

        self._config[section][option] = str(value)
        self.save()
    
    def has_option(self, section, option):
        return option in self._config[section]
    
    def get(self, section, option):
        return self._config[section][option]


CONFIG = _config()