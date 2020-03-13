#!/usr/bin/env python3

import sys
from io import StringIO

from antlr4 import *
from antlr4.tree.Trees import Trees
from antlr4.Utils import escapeWhitespace

from grammar.ObjectiveCLexer import ObjectiveCLexer
from grammar.ObjectiveCParser import ObjectiveCParser


def toStringTree(t, ruleNames=None, recog=None, index=0):
    if recog is not None:
        ruleNames = recog.ruleNames
    s = escapeWhitespace(Trees.getNodeText(t, ruleNames), False)
    if t.getChildCount() == 0:
        return s
    with StringIO() as buf:
        buf.write(u"\n")

        tab_num = index
        while tab_num > 0:
            buf.write(u"  ")
            tab_num = tab_num - 1

        buf.write("(")
        buf.write(s)
        buf.write(' ')
        for i in range(0, t.getChildCount()):
            if i > 0:
                buf.write(' ')
            next_index = index + 1
            buf.write(toStringTree(t.getChild(i), ruleNames, index=next_index))
        buf.write(")")
        return buf.getvalue()


def main(argv):

    filePath = argv[1]
    input = FileStream(filePath, encoding='utf-8')
    lexer = ObjectiveCLexer(input)
    stream = CommonTokenStream(lexer)
    parser = ObjectiveCParser(stream)
    tree = parser.translationUnit()

    lisp_tree_str = toStringTree(tree, recog=parser)
    print( "--parser succeed--")
    print(lisp_tree_str)


if __name__ == '__main__':
    main(sys.argv)
