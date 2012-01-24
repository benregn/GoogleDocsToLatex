import os
import ConfigParser


class ConfigFile:
    def __init__(self, filename):
        self.config = ConfigParser.SafeConfigParser(allow_no_value=True)
        self.config_filename = filename
        self.username = ''
        self.folder_name = ''
        self.verbose = None

    def write_config_file(self, username='', folder_name=''):
        """
        Checks if the file exists, if not it creates the config file and writes in the options
        without setting them.
        """
        self.config.add_section('DocsToLatex')
        self.config.set('DocsToLatex', 'username', username)
        self.config.set('DocsToLatex', 'folder_name', folder_name)
        self.config.set('DocsToLatex', '#Has to be set to \'True\' or \'False\'')
        self.config.set('DocsToLatex', 'verbose_output', 'False')

        with open(self.config_filename, 'wb') as configfile:
            self.config.write(configfile)

    def read_config_file(self):
        """
        Reads in the values from the config file.
        """
        if self.config_exists():
            self.config.read(self.config_filename)

            self.username = self.config.get('DocsToLatex', 'username')
            self.folder_name = self.config.get('DocsToLatex', 'folder_name')
            self.verbose = self.config.getboolean('DocsToLatex', 'verbose_output')

    def config_exists(self):
        file_exists = None
        if os.path.isfile(self.config_filename):
            file_exists = True
        else:
            file_exists = False

        return file_exists
