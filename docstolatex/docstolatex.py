# -*- coding: utf-8 -*-
from gdata.docs import client
import os
import errno
import subprocess
import shutil
from getpass import getpass


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
        self.docs_client.client_login(username, password, self.docs_client.source)

        self.document_list = None
        self.docs_folder = ''
        self.base_path = os.getcwd()
        self.download_images = None
        self.verbose = False


    def print_feed(self, feed):
        """Prints out the contents of a feed to the console."""
        table_format = '    %-30s %-20s %-12s'
        print '\n'
        if not feed.entry:
            print 'No entries in feed.\n'
        else:
            print table_format % ('TITLE', 'PARENT', 'TYPE')
            for entry in feed.entry:
                print table_format % (entry.title.text.encode('UTF-8'),
                                      [f.title for f in entry.InFolders()],
                                      entry.GetDocumentType())


    def get_folder_list(self):
        """
        Gets the user's folder list.
        """
        self.document_list = self.docs_client.GetDocList(
            uri='/feeds/default/private/full/-/folder')


    def find_selected_folder(self):
        """
        Finds the folder specified in config file or from user input.
        """
        folder_feed = None
        for folder in self.document_list.entry:
            if folder.title.text.encode('UTF-8') == self.docs_folder:
                if self.verbose:
                    print 'Contents of ' + self.docs_folder + ':'
                folder_feed = self.docs_client.GetDocList(
                    uri=folder.content.src)
        return folder_feed


    def download_folder_contents(self, folder_feed):
        """
        Sorts out if entries are a folder, a document or miscellaneous file type.
        """
        if self.verbose:
            self.print_feed(folder_feed)

        for entry in folder_feed.entry:
            if entry.GetDocumentType() == 'folder':
                if self.verbose:
                    print '\n' + entry.title.text.encode('UTF-8')
                self.download_folder_contents(self.docs_client.GetDocList(
                    uri=entry.content.src))
            elif entry.GetDocumentType() == 'document':
                self.download_document(entry)
            else:
                if not self.download_images and 'image' in entry.GetDocumentType():
                    pass
                else:
                    self.download_file(entry)
    

    def download_document(self, entry):
        """
        Downloads files of Google Documents type and puts them in the
        correct folders according to Docs collections.
        """
        current_folder_name = entry.InFolders()[0].title
        document_name = entry.title.text.encode('UTF-8')
        file_ext = '.txt'

        print '=' * 50
        print 'Document name: ' + document_name

        # if document is in the root collection, then it is
        # saved in the root
        if current_folder_name == self.docs_folder:
            file_path = os.path.join(self.base_path, document_name + file_ext)
            if make_directory(file_path):
                self.docs_client.Export(entry, file_path)
            print 'Saved in the base folder (' + os.sep + current_folder_name + os.sep \
            + ')\n'
        else:
            file_path = os.path.join(self.base_path, current_folder_name,
                                     document_name + file_ext)
            if make_directory(file_path):
                self.docs_client.Export(entry, file_path)
            print 'Saved in subfolder (' + os.sep + current_folder_name + \
                  os.sep + ')\n'

        self.remove_ext_txt(file_path)


    def download_file(self, entry):
        """
        Downloads files that are not Google Documents and puts them in the
        correct folders according to Docs collections.
        """
        current_folder_name = entry.InFolders()[0].title
        document_name = entry.title.text.encode('UTF-8')

        print '=' * 50 + '\n'
        print 'File name: ' + document_name

        if current_folder_name == self.docs_folder:
            file_path = os.path.join(self.base_path, document_name)
            if make_directory(file_path):
                self.docs_client.Download(entry, file_path)
            print 'Saved in the base folder (' + os.sep + current_folder_name + \
                  os.sep + ')\n'
        else:
            file_path = os.path.join(self.base_path, current_folder_name,
                                     document_name)
            if make_directory(file_path):
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
                if not os.path.splitext(file)[1]: #if file extension is empty
                    if os.path.exists(file_path_with_tex):
                        os.remove(file_path_with_tex)
                        os.rename(file_path_without_tex, file_path_with_tex)
                    else:
                        os.rename(file_path_without_tex, file_path_with_tex)
                else:
                    pass



class CompileLaTeX():
    def __init__(self, base_path):
        self.base_path = base_path
        #Google Docs style as key and LaTeX style as values
        self.docs_latex_quotes = {'‘': '`', '’': '\'', '“': '``', '”': '\'\''}


    def replace_quote_characters(self):
        for root, dirs, files in os.walk(self.base_path):
            print root
            for file in files:
                if file.endswith(('.tex', '.bib',)):
                    path_to_file = os.path.join(root, file)
                    current_file = open(path_to_file, "r")
                    contents = current_file.read()
                    for i, k in self.docs_latex_quotes.iteritems():
                        contents = contents.replace(i, k)
                    current_file.close()

                    current_file = open(path_to_file, "w")
                    current_file.write(contents)
                    current_file.close()


    def compile_to_latex(self, filename):
        file_path = self.find_file_to_compile(filename, self.base_path)
        output_directory = os.path.join(self.base_path)

        pdflatex = list()
        pdflatex.append('pdflatex')
        pdflatex.append('{}'.format(file_path))
        pdflatex.append('-interaction=nonstopmode')
        pdflatex.append('-output-directory={}'.format(output_directory))
        return_value = subprocess.call(pdflatex)

        if return_value == 1:
            print('Something went wrong. Check the log file.')
        else:
            self.cleanup_latex()


    def find_file_to_compile(self, filename, path):
        for root, dirs, files in os.walk(path):
            for name in files:
                if filename == name:
                    print '{} found'.format(filename)
                    return os.path.join(root, name)

                print '{} not found'.format(filename)


    def cleanup_latex(self):
        latex_temp_extensions = ('.aux', '.bbl', '.blg', '.log', '.toc',
                          '.lof', '.lot',)
        temp_folder_name = 'temp'

        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith(latex_temp_extensions):
                    source = os.path.join(root, file)
                    destination = os.path.join(root, temp_folder_name, file)
                    # path has to exist before shutil.move
                    if not os.path.exists(destination):
                        make_directory(destination)
                    shutil.move(source, destination)


def make_directory(file_path):
    if os.path.splitext(file_path)[1]:
        file_path = os.path.dirname(file_path)

    if not os.path.exists(file_path):
        try:
            os.makedirs(file_path)
            return True
        except OSError, e:
            if e.errno == errno.EEXIST:
                pass
    else:
        #folder existed
        return True
