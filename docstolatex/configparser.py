import ConfigParser

class ConfigFileParser:
    def __init__(self):
        self.config = ConfigParser.SafeConfigParser(allow_no_value=True)

    def write_config_file(self):
        self.config.add_section('DocsToLatex')
        self.config.set('DocsToLatex', 'username', '')
        self.config.set('DocsToLatex', 'folder_name', '')

        with open('config.cfg', 'wb') as configfile:
            self.config.write(configfile)


    def read_config_file(self):
        self.config.read('config.cfg')

        self.username = self.config.get('DocsToLatex', 'username')
        self.folder_name = self.config.get('DocsToLatex', 'folder_name')