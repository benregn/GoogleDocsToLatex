from gdata.docs import client
from getpass import getpass


client = client.DocsClient(source='benregn-GoogleDocsToLaTeX-v1')


def print_feed(feed):
    """Prints out the contents of a feed to the console."""
    print '\n'
    if not feed.entry:
        print 'No entries in feed.\n'
    print '%-30s %-20s %-12s %s' % ('TITLE', 'PARENT', 'TYPE', 'RESOURCE ID')
    for entry in feed.entry:
        print '%-30s %-20s %-12s %s' % (entry.title.text.encode('UTF-8'),
                                        [f.title for f in entry.InFolders()],
                                        entry.GetDocumentType(),
                                        entry.resource_id.text)


def get_folder_list():
    feed = client.GetDocList(uri='/feeds/default/private/full/-/folder')
    return feed


def searching_title(query):
    feed = client.GetDocList(
        '/feeds/default/private/full?title=%s&title-exact=true&max-results=5'
        % query)
    print feed
    print_feed(feed)


def get_selected_folder(folder_name):
    feed = get_folder_list()
    for folder in feed.entry:
        if folder.title.text.encode('UTF-8') == folder_name:
            print 'Contents of folder: ' + folder_name + '   ' + folder.content.src
            folder_feed = client.GetDocList(uri=folder.content.src)
            for doc in folder_feed.entry:
                print doc.title.text, [f.title for f in doc.InFolders()]


def main():
    username = raw_input('Enter your username: ')
    password = raw_input('Enter your password: ')
    #password = getpass('Enter your password: ')
    client.client_login(username, password, client.source)
    print_feed(get_folder_list())
    folder_name = raw_input('Select folder: ')
    get_selected_folder(folder_name)
    #searching_title('Level')


if __name__ == '__main__':
    main()