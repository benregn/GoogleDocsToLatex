import os
from docstolatex import DocsToLaTeX, CompileLaTeX
from configfile import ConfigFile




def main():
    parse_conf = ConfigFile('config.cfg')
    parse_conf.write_config_file()
    parse_conf.read_config_file()

    if not parse_conf.username:
        username = raw_input('Enter your username: ')
    else:
        username = parse_conf.username
        print 'Logging in as {}'.format(username)

    password = raw_input('Enter your password: ')
    #password = getpass('Enter your password: ')

    dtl = DocsToLaTeX(username, password)
    dtl.verbose = parse_conf.verbose

    dtl.get_folder_list()

    if not parse_conf.folder_name:
        dtl.print_feed(dtl.document_list)
        dtl.docs_folder = raw_input('Select folder: ')
    else:
        dtl.docs_folder = parse_conf.folder_name

    download_images = raw_input('Download images? (y = yes, defaults to no) ')
    if download_images.lower() == 'y':
        dtl.download_images = True
    else:
        dtl.download_images = False

    dtl.base_path = os.path.join(dtl.base_path, dtl.docs_folder)
    print 'File path to save to is: ' + dtl.base_path
    dtl.find_selected_folder()
    dtl.check_for_tex_extension(dtl.base_path)

    comp_latex = CompileLaTeX(dtl.base_path)
    comp_latex.replace_quote_characters()
    main_latex_file = raw_input('Enter the name of the main LaTeX file: ')
    if main_latex_file:
        comp_latex.compile_to_latex(main_latex_file)
    else:
        print 'No file name entered.'


if __name__ == '__main__':
    main()