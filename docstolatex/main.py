import os
from docstolatex import DocsToLaTeX, CompileLaTeX
from configfileparser import ConfigFileParser




def main():
    dtl = DocsToLaTeX()
    parse_conf = ConfigFileParser('config.cfg')
    parse_conf.write_config_file()
    parse_conf.read_config_file()

    if not parse_conf.username:
        username = raw_input('Enter your username: ')
    else:
        username = parse_conf.username
        print 'Logging in as {}'.format(username)

    password = raw_input('Enter your password: ')
    #password = getpass('Enter your password: ')
    dtl.client.client_login(username, password, dtl.client.source)

    dtl.get_folder_list()
    dtl.print_feed(dtl.document_list)

    if not parse_conf.folder_name:
        dtl.docs_folder = raw_input('Select folder: ')
    else:
        dtl.docs_folder = parse_conf.folder_name

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