from gdata.docs import client


client = client.DocsClient(source='benregn-GoogleDocsToLaTeX-v1')


def GetFolderList():
    feed = client.GetDocList(uri='/feeds/default/private/full/-/folder')
    PrintFeed(feed)


def PrintFeed(feed):
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
    client.client_login(username, password, client.source)
    GetFolderList()


if __name__ == '__main__':
    main()