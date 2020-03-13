from antlr4 import *

from occheck.grammar.ObjectiveCLexer import ObjectiveCLexer
from occheck.grammar.ObjectiveCParser import ObjectiveCParser


class FileContext:
    def __init__(self, file_path):
        with open(file_path, "r", encoding='utf-8') as stream:
            self.source_code = stream.read()

        self.lines = self.source_code.splitlines(keepends=True)
        self.current_file = file_path

        # parse file
        self.parser = None
        self.ast = None
        self.parse_file(file_path)

    def get_current_file(self):
        return self.current_file

    def get_lines(self):
        """Return the lines with line ending kept."""
        return self.lines

    def get_source_code(self):
        """Return the source code."""
        return self.source_code

    def get_ast(self):
        return self.ast

    def get_parser(self):
        return self.parser

    def parse_file(self, file, encoding='utf-8'):
        input_stream = FileStream(file, encoding=encoding)
        lexer = ObjectiveCLexer(input_stream)
        stream = CommonTokenStream(lexer)
        self.parser = ObjectiveCParser(stream)
        self.parser.removeErrorListeners()
        self.ast = self.parser.translationUnit()

    def has_syntax_errors(self):
        return self.parser.getNumberOfSyntaxErrors() > 0
