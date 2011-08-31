import errno
from gdata.docs import client
import os
import errno
import subprocess
from getpass import getpass


class DocsToLaTeX():
    client = client.DocsClient(source='benregn-GoogleDocsToLaTeX-v1')
    document_list = None
    docs_folder = ''
    base_path = os.getcwd()

    def print_feed(self, feed):
        """Prints out the contents of a feed to the console."""
        table_format = '    %-30s %-20s %-12s %s'
        print '\n'
        if not feed.entry:
            print 'No entries in feed.\n'
        else:
            print table_format % ('TITLE', 'PARENT', 'TYPE',
                                            'RESOURCE ID')
            for entry in feed.entry:
                print table_format % (entry.title.text.encode('UTF-8'),
                                      [f.title for f in entry.InFolders()],
                                      entry.GetDocumentType(),
                                      entry.resource_id.text)


    def get_folder_list(self):
        self.document_list = self.client.GetDocList(uri='/feeds/default/private/full/-/folder')


    def find_selected_folder(self):
        for folder in self.document_list.entry:
            if folder.title.text.encode('UTF-8') == self.docs_folder:
                folder_feed = self.client.GetDocList(uri=folder.content.src)
                print 'Contents of ' + self.docs_folder + ':'
                self.download_folder_contents(folder_feed)


    def download_folder_contents(self, folder_feed):
        self.print_feed(folder_feed)

        for entry in folder_feed.entry:
            if entry.GetDocumentType() == 'folder':
                print '\n' + entry.title.text.encode('UTF-8')
                self.download_folder_contents(self.client.GetDocList(uri=entry.content.src))
            elif entry.GetDocumentType() == 'document':
                self.download_document(entry)
            else:
                self.download_file(entry)
    

    def download_document(self, entry):
        current_folder_name = entry.InFolders()[0].title
        document_name = entry.title.text.encode('UTF-8')
        file_ext = '.txt'

        print 'doc'
        print 'entry.InFolders()[0].title: ' + current_folder_name
        print 'docs_folder: ' + self.docs_folder
        print 'document_name: ' + document_name

        # if document is in the root collection, then it is
        # saved in the root
        if current_folder_name == self.docs_folder:
            print 'Document is in the base folder.'
            file_path = os.path.join(self.base_path, document_name + file_ext)
            if self.make_directory(file_path):
                self.client.Export(entry, file_path)
            print 'Saved in folder: ' + os.sep + current_folder_name + os.sep \
            + '\n'
        else:
            print 'Document is in ' + current_folder_name
            file_path = os.path.join(self.base_path, current_folder_name,
                                     document_name + file_ext)
            if self.make_directory(file_path):
                self.client.Export(entry, file_path)
            print 'Saved in subfolder: ' + os.sep + current_folder_name + \
                  os.sep + '\n'

        self.remove_ext_txt(file_path)


    def download_file(self, entry):
        current_folder_name = entry.InFolders()[0].title
        document_name = entry.title.text.encode('UTF-8')

        if current_folder_name == self.docs_folder:
            print 'File is in the base folder.'
            file_path = os.path.join(self.base_path, document_name)
            if self.make_directory(file_path):
                self.client.Download(entry, file_path)
            print 'Saved in folder: ' + os.sep + current_folder_name + \
                  os.sep + '\n'
        else:
            print 'File is in ' + current_folder_name
            file_path = os.path.join(self.base_path, current_folder_name,
                                     document_name)
            if self.make_directory(file_path):
                self.client.Download(entry, file_path)
            print 'Saved in subfolder: ' + os.sep + current_folder_name + \
                  os.sep + '\n'

    def make_directory(self, file_path):
        path = os.path.dirname(file_path)
        print path
        if not os.path.exists(path):
                try:
                    print 'Attempting to create folder.'
                    os.makedirs(path)
                    return True
                except OSError, e:
                    if e.errno == errno.EEXIST:
                        pass
                    raise
        else:
            print 'Folder existed.'
            return True


    def remove_ext_txt(self, path_to_file):
        shortened_path = path_to_file[:-4]
        print '='*50 + '\n' + shortened_path + '\n' + '='*50

        # os.rename does not overwrite, so remove old copy first
        if os.path.exists(shortened_path):
            os.remove(shortened_path)
            os.rename(path_to_file, shortened_path)
        else:
            os.rename(path_to_file, shortened_path)


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


    def find_file_to_compile(self, filename, path):
        for root, dirs, files in os.walk(path):
            for name in files:
                if filename == name:
                    return os.path.join(root, name)
                else:
                    print '{} not found'.format(filename)


    def run(self):
        username = raw_input('Enter your username: ')
        password = raw_input('Enter your password: ')
        #password = getpass('Enter your password: ')
        self.client.client_login(username, password, self.client.source)

        self.get_folder_list()
        self.print_feed(self.document_list)
        self.docs_folder = raw_input('Select folder: ')
        self.base_path = os.path.join(self.base_path, self.docs_folder)
        print 'File path to save to is: ' + self.base_path
        self.find_selected_folder()
        self.compile_to_latex('latexsheet.tex')


def main():
    dtl = DocsToLaTeX()
    dtl.run()


if __name__ == '__main__':
    main()