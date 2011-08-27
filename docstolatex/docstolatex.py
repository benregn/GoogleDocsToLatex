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
                print 'doc'


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