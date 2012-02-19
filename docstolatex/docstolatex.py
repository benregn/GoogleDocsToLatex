import os
import sys
from gdata.docs import client
from clint import textui
import utilityfunctions as utilfunc


class DocsToLaTeX():
    def __init__(self, username, password):
        """
        Constructor for DocsToLaTeX.

        Takes an username or email and a password to a Google account
        to login to Google Docs.

        Args:
              username: [string] The email or username of the account
                        to use for the sample.
              password: [string] The password corresponding to the
                        account specified by the username parameter.
        """
        self.docs_client = client.DocsClient(
                source='benregn-GoogleDocsToLaTeX-v1')
        self.docs_client.client_login(username, password,
                                      self.docs_client.source)

        self.document_list = None
        self.docs_folder = ''
        self.base_path = os.getcwd()
        self.COLUMN_WIDTH = 15
        self.DOUBLE_COLUMN_WIDTH = self.COLUMN_WIDTH * 2
        self.download_images = None
        self.verbose = False

    def print_feed(self, resources_list):
        """
        Prints out the contents of a feed to the console.

        Args:
            resources_list: A list of Resource objects
        """
        textui.puts(textui.columns(['Title', self.DOUBLE_COLUMN_WIDTH],
                                   ['Collections', self.DOUBLE_COLUMN_WIDTH],
                                   ['Type', self.COLUMN_WIDTH]))
        for resource in resources_list:
            self.print_resource(resource)

    def print_resource(self, resource):
        """
        Prints out resource's title, what collections it is in and what type it
        is.

        Args:
            resource: A Resource object
        """
        textui.puts(textui.columns([resource.title.text.encode('utf-8'),
                                   self.DOUBLE_COLUMN_WIDTH],
                                   [self.get_resource_folder_list(resource),
                                   self.DOUBLE_COLUMN_WIDTH],
                                   [resource.GetResourceType(),
                                   self.COLUMN_WIDTH]))

    def get_resource_folder_list(self, resource):
        """
        Formats the list of folders that the resource belongs to into a string.

        Args:
            resource: A Resource object

        Returns:
            String
        """
        collections = resource.InCollections()
        collections_as_string = ', '.join(c.title for c in collections)

        return '[' + collections_as_string + ']'

    def get_folder_list(self):
        """
        Gets the user's folder list.
        """
        self.document_list = self.docs_client.GetAllResources(
            uri='/feeds/default/private/full/-/folder')

    def find_folder(self):
        """
        Finds the folder specified in config file or from user input.

        Returns:
            dictionary: 'folder name': folder name as it is on Docs
                        'folder feed': folder feed
        """
        folder_list = None

        for folder in self.document_list:
            if folder.title.text.lower() == self.docs_folder.lower():
                if self.verbose:
                    print 'Contents of ' + self.docs_folder + ':'
                folder_list = {'folder title': folder.title.text,
                               'folder feed': self.docs_client.GetAllResources(
                                              uri=folder.content.src)}
                break
        if not folder_list:
            sys.exit("Folder not found")
        return folder_list

    def download_folder_contents(self, folder_list):
        """
        Sorts out if entries are a folder, a document or miscellaneous file
        type.
        """
        if self.verbose:
            self.print_feed(folder_list)

        for resource in folder_list:
            resource_type = resource.GetResourceType()
            if resource_type == 'folder':
                if self.verbose:
                    print '\n' + resource.title.text
                self.download_folder_contents(self.docs_client.GetAllResources(
                    uri=resource.content.src))
            elif resource_type == 'document':
                self.download_document(resource)
            else:
                if not self.download_images and 'image' in resource_type:
                    pass
                else:
                    self.download_file(resource)

    def download_document(self, entry):
        """
        Downloads files of Google Documents type and puts them in the
        correct folders according to Docs collections.
        """
        current_folder_name = entry.InFolders()[0].title.lower()
        document_name = entry.title.text.encode('UTF-8')
        file_ext = '.txt'

        print '=' * 50
        print 'Document name: ' + document_name

        # if document is in the root collection, then it is
        # saved in the root
        if current_folder_name == self.docs_folder.lower():
            file_path = os.path.join(self.base_path, document_name + file_ext)
            if utilfunc.make_directory(file_path):
                self.docs_client.Export(entry, file_path)
            print 'Saved in the base folder (' + os.sep + current_folder_name
            + os.sep + ')\n'
        else:
            file_path = os.path.join(self.base_path, current_folder_name,
                                     document_name + file_ext)
            if utilfunc.make_directory(file_path):
                self.docs_client.Export(entry, file_path)
            print 'Saved in subfolder (' + os.sep + current_folder_name + \
                  os.sep + ')\n'

        self.remove_ext_txt(file_path)

    def download_file(self, entry):
        """
        Downloads files that are not Google Documents and puts them in the
        correct folders according to Docs collections.
        """
        current_folder_name = entry.InFolders()[0].title.lower()
        document_name = entry.title.text.encode('UTF-8')

        print '=' * 50 + '\n'
        print 'File name: ' + document_name

        if current_folder_name == self.docs_folder.lower():
            file_path = os.path.join(self.base_path, document_name)
            if utilfunc.make_directory(file_path):
                self.docs_client.Download(entry, file_path)
            print 'Saved in the base folder (' + os.sep + current_folder_name \
                    + os.sep + ')\n'
        else:
            file_path = os.path.join(self.base_path, current_folder_name,
                                     document_name)
            if utilfunc.make_directory(file_path):
                self.docs_client.Download(entry, file_path)
            print 'Saved in subfolder (' + os.sep + current_folder_name + \
                  os.sep + ')\n'

    def remove_ext_txt(self, file_path):
        """
        Removes the .txt file extension from Documents.
        """
        file_path_without_ext = file_path[:-4]

        # os.rename does not overwrite, so remove old copy first
        if os.path.exists(file_path_without_ext):
            os.remove(file_path_without_ext)
            os.rename(file_path, file_path_without_ext)
        else:
            os.rename(file_path, file_path_without_ext)

    def check_for_tex_extension(self, path):
        """
        Checks if Documents have .tex extension, adds it if it doesn't.
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path_without_tex = os.path.join(root, file)
                file_path_with_tex = os.path.join(root, file + ".tex")
                if not os.path.splitext(file)[1]:  # if file extension is empty
                    if os.path.exists(file_path_with_tex):
                        os.remove(file_path_with_tex)
                        os.rename(file_path_without_tex, file_path_with_tex)
                    else:
                        os.rename(file_path_without_tex, file_path_with_tex)
                else:
                    pass
