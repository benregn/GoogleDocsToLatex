from gdata.docs import client


client = client.DocsClient(source='benregn-GoogleDocsToLaTeX-v1')


def main():
    username = raw_input('Enter your username: ')
    password = raw_input('Enter your password: ')
    client.client_login(username, password, client.source)
    GetFolderList()


def GetFolderList():
    feed = client.GetDocList(uri='/feeds/default/private/full/-/folder')


if __name__ == '__main__':
    main()