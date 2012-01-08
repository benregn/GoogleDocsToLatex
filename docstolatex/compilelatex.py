# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
import utilityfunctions as utilfunc


class CompileLaTeX():
    def __init__(self, base_path):
        self.base_path = base_path
        #Google Docs style as key and LaTeX style as values
        self.docs_latex_quotes = {'‘': '`', '’': '\'', '“': '``', '”': '\'\''}


    def replace_quote_characters(self):
        for root, dirs, files in os.walk(self.base_path):
            print root
            for file in files:
                if file.endswith(('.tex', '.bib',)):
                    path_to_file = os.path.join(root, file)
                    current_file = open(path_to_file, "r")
                    contents = current_file.read()
                    for i, k in self.docs_latex_quotes.iteritems():
                        contents = contents.replace(i, k)
                    current_file.close()

                    current_file = open(path_to_file, "w")
                    current_file.write(contents)
                    current_file.close()


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
        else:
            self.cleanup_latex()


    def find_file_to_compile(self, filename, path):
        for root, dirs, files in os.walk(path):
            for name in files:
                if filename == name:
                    print '{} found'.format(filename)
                    return os.path.join(root, name)

                print '{} not found'.format(filename)


    def cleanup_latex(self):
        latex_temp_extensions = ('.aux', '.bbl', '.blg', '.log', '.toc',
                          '.lof', '.lot',)
        temp_folder_name = 'temp'

        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith(latex_temp_extensions):
                    source = os.path.join(root, file)
                    destination = os.path.join(root, temp_folder_name, file)
                    # path has to exist before shutil.move
                    if not os.path.exists(destination):
                        utilfunc.make_directory(destination)
                    shutil.move(source, destination)