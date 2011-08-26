from gdata.docs import client
from getpass import getpass


client = client.DocsClient(source='benregn-GoogleDocsToLaTeX-v1')


def get_folder_list():
    feed = client.GetDocList(uri='/feeds/default/private/full/-/folder')
    print_feed(feed)


def searching_title(query):
    feed = client.GetDocList(
        '/feeds/default/private/full?title=%s&title-exact=true&max-results=5'
        % query)
    print feed
    print_feed(feed)


def print_feed(feed):
    """Prints out the contents of a feed to the console."""
    print '\n'
    if not feed.entry:
        print 'No entries in feed.\n'
    for entry in feed.entry:
        print '%s /-/ %s /-/ %s' % (entry.title.text.encode('UTF-8'),
                                    entry.GetDocumentType(),
                                    entry.resource_id.text)


def main():
    username = raw_input('Enter your username: ')
    password = raw_input('Enter your password: ')
    #password = getpass('Enter your password: ')
    client.client_login(username, password, client.source)
    #get_folder_list()
    searching_title('Level')


if __name__ == '__main__':
    main()