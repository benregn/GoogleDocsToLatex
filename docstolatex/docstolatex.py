from gdata.docs import client
import os
from getpass import getpass


client = client.DocsClient(source='benregn-GoogleDocsToLaTeX-v1')

class DocsToLaTeX():
    docs_folder = ''
    base_file_path = os.getcwd()

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
        feed = client.GetDocList(uri='/feeds/default/private/full/-/folder')
        return feed


    def find_selected_folder(self):
        feed = self.get_folder_list()
        for folder in feed.entry:
            if folder.title.text.encode('UTF-8') == self.docs_folder:
                folder_feed = client.GetDocList(uri=folder.content.src)
                print 'Contents of ' + self.docs_folder + ':'
                self.download_folder_contents(folder_feed)


    def download_folder_contents(self, folder_feed):
        self.print_feed(folder_feed)

        for entry in folder_feed.entry:
            if entry.GetDocumentType() == 'folder':
                print '\n' + entry.title.text.encode('UTF-8')
                self.download_folder_contents(client.GetDocList(uri=entry.content.src))
            elif entry.GetDocumentType() == 'document':
                self.download_document(entry)
    

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
            file_path = self.base_file_path + '\\' + document_name + file_ext
            client.Export(entry, file_path)
            print 'Saved in folder: ' + '\\' + current_folder_name + '\\\n'
        else:
            print 'Document is in ' + current_folder_name
            file_path = self.base_file_path + '\\' + current_folder_name \
            + '\\' + document_name + '\\' + file_ext
            client.Export(entry, file_path)
            print 'Saved in subfolder: ' + '\\' + current_folder_name + '\\\n'


def main():
    username = raw_input('Enter your username: ')
    password = raw_input('Enter your password: ')
    #password = getpass('Enter your password: ')
    client.client_login(username, password, client.source)
    dtl = DocsToLaTeX()
    dtl.print_feed(dtl.get_folder_list())
    dtl.docs_folder = raw_input('Select folder: ')
    dtl.base_file_path = dtl.base_file_path + '\\' + dtl.docs_folder
    print 'File path to save to is:' + dtl.base_file_path
    dtl.find_selected_folder()


if __name__ == '__main__':
    main()