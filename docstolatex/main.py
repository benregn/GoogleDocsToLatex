import os
import textwrap
from getpass import getpass
from docstolatex import DocsToLaTeX
from compilelatex import CompileLaTeX
from configfile import ConfigFile


def get_folder_name(dtl, parse_conf):
    """
    Check if folder name is defined in the config file. Otherwise print folder
    list and ask for user input.

    Returns:
        String
    """
    folder_name = ''
    if parse_conf.folder_name:
        folder_name = parse_conf.folder_name
    else:
        dtl.print_feed(dtl.document_list)
        folder_name = raw_input('Select folder: ')
    return folder_name

def main():
    parse_conf = ConfigFile('config.cfg')
    parse_conf.read_config_file()

    if not parse_conf.username:
        username = raw_input('Enter your username: ')
    else:
        username = parse_conf.username
        print 'Logging in as {}'.format(username)

    password = getpass('Enter your password: ')

    dtl = DocsToLaTeX(username, password)
    dtl.verbose = parse_conf.verbose

    dtl.get_folder_list()

    dtl.docs_folder = get_folder_name(dtl, parse_conf)

    docs_folder_feed = dtl.find_folder()

    #if user enters the name in different capitalization then on Docs
    #then reset docs_folder to Docs version
    dtl.docs_folder = docs_folder_feed['folder title']

    download_images = raw_input('Download images? (y = yes, defaults to no) ')
    if download_images.lower() == 'y':
        dtl.download_images = True
    else:
        dtl.download_images = False

    dtl.base_path = os.path.join(dtl.base_path, dtl.docs_folder)
    print 'File path to save to is: ' + dtl.base_path

    dtl.download_folder_contents(docs_folder_feed['folder feed'])
    dtl.check_for_tex_extension(dtl.base_path)

    comp_latex = CompileLaTeX(dtl.base_path)
    comp_latex.replace_quote_characters()
    main_latex_file = raw_input('Enter the name of the main LaTeX file: ')
    if main_latex_file:
        comp_latex.compile_to_latex(main_latex_file)
    else:
        print 'No file name entered.'

    if not parse_conf.config_exists():
        config_saved = """\
                        Your username ({}) and chosen folder ({}) have 
                        been saved in {}""".format(username, dtl.docs_folder, 
                        os.path.join(dtl.base_path, 'config.cfg'))
        print textwrap.dedent(config_saved)
        parse_conf.write_config_file(username=username, folder_name=dtl.docs_folder)


if __name__ == '__main__':
    main()
