import ConfigParser

class ConfigFileParser:
    def __init__(self, filename):
        self.config = ConfigParser.SafeConfigParser(allow_no_value=True)
        self.config_filename = filename

    def write_config_file(self):
        self.config.add_section('DocsToLatex')
        self.config.set('DocsToLatex', 'username', '')
        self.config.set('DocsToLatex', 'folder_name', '')

        with open(self.config_filename, 'wb') as configfile:
            self.config.write(configfile)


    def read_config_file(self):
        self.config.read(self.config_filename)

        self.username = self.config.get('DocsToLatex', 'username')
        self.folder_name = self.config.get('DocsToLatex', 'folder_name')