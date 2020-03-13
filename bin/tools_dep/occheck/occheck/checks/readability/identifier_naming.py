import re
from enum import Enum

from antlr4.Token import CommonToken
from antlr4.ParserRuleContext import ParserRuleContext

from occheck.checks import BaseCheck
from occheck.grammar.ObjectiveCParser import ObjectiveCParser

_auto_null = object()


class Auto:
    """
    Instances are replaced with an appropriate value in Enum class suites.
    """
    value = _auto_null


class StyleName(Enum):
    Class = Auto(),
    Method = Auto(),
    Function = Auto(),
    Parameter = Auto(),
    LocalVariable = Auto(),
    GlobalVariable = Auto(),
    Macro = Auto(),


class CaseType(Enum):
    AnyCase = 0,        # default
    LowerCase = 1,      # lower_case
    CamelBack = 2,      # camelBack
    UpperCase = 3,      # UPPER_CASE
    CamelCase = 4,      # CamelCase

    @classmethod
    def from_string(cls, name):
        if name == 'camelBack':
            return cls.CamelBack
        elif name == 'CamelCase':
            return cls.CamelCase
        elif name == 'lower_case':
            return cls.LowerCase
        elif name == 'UPPER_CASE':
            return cls.UpperCase
        else:
            return cls.AnyCase


class NamingStyle:
    def __init__(self, case: CaseType, prefix="", suffix=""):
        self.case = case
        self.prefix = prefix
        self.suffix = suffix

    def explain_style(self):
        usage = ""

        if self.prefix:
            usage += "前缀('%s') + " % self.prefix

        if self.case is CaseType.CamelCase:
            usage += '大驼峰命名'
        elif self.case is CaseType.CamelBack:
            usage += '小驼峰命名'
        elif self.case is CaseType.LowerCase:
            usage += '全部小写'
        elif self.case is CaseType.UpperCase:
            usage += '全部大写'
        else:
            usage += '任意字符'

        if self.suffix:
            usage += " + 后缀('%s')" % self.suffix

        return usage


class IdentifierNamingCheck(BaseCheck):
    def __init__(self):
        super().__init__()

        self.cached_options = dict()
        self.naming_styles = dict()

    def initialize(self):
        """Initialize this check here."""
        style_names = [style.name for style in StyleName]
        for name in style_names:
            case = CaseType.from_string(self.get_option(name + 'Case', ""))
            prefix = self.get_option(name + 'Prefix', "")
            suffix = self.get_option(name + 'Suffix', "")
            style = NamingStyle(case, prefix, suffix)
            self.naming_styles[name] = style

    def begin_check(self, filename):
        style = self.get_naming_style(StyleName.Macro)
        pattern = re.compile(r'^#define\s+(?P<macro_name>\w+)(\s+|\s*\()')

        lines = self.get_lines()

        for index, line in enumerate(lines):
            match = pattern.match(line.lstrip())
            if match:
                name = match.group('macro_name')
                if not self.match_style(name, style):
                    fixup = self.fixup_with_style(name, style)
                    if fixup != name:
                        explain_str = '建议使用："%s"。期望的格式为："%s"' % (fixup, style.explain_style())
                    else:
                        explain_str = '要求的格式为："%s"' % style.explain_style()

                    column = line.find(name)
                    self.diag("不合规的命名：'%s'，%s" % (name, explain_str), index + 1, column)

    def get_naming_style(self, style: StyleName):
        return self.naming_styles[style.name]

    def exitMethodSelector(self, ctx: ObjectiveCParser.MethodSelectorContext):
        """Check method/parameter names."""
        selector = ctx.selector()
        if selector:
            token = selector.start
            self.check_identifier(token, StyleName.Method)
            return

        keyword_declarator = ctx.keywordDeclarator()
        for index, keyword in enumerate(keyword_declarator):
            if index == 0:
                is_method_name = True
            else:
                is_method_name = False

            label_token = keyword.selector().identifier().start
            param_token = keyword.identifier().start

            if is_method_name:
                self.check_identifier(label_token, StyleName.Method)
                self.check_identifier(param_token, StyleName.Parameter)
            else:
                self.check_identifier(label_token, StyleName.Parameter)
                self.check_identifier(param_token, StyleName.Parameter)

    def exitClassInterface(self, ctx: ObjectiveCParser.ClassInterfaceContext):
        context = ctx.genericTypeSpecifier()

        # get class name
        identifier = context.identifier()
        if not identifier:
            return

        token = identifier.start
        self.check_identifier(token, StyleName.Class)

    def exitParameterDeclaration(self, ctx: ObjectiveCParser.ParameterDeclarationContext):
        """Check function parameter names match the specified naming style."""
        if not ctx.declarator():
            # ignore void type.
            return

        declarator = ctx.declarator().directDeclarator()
        identifier = declarator.identifier()
        if not identifier:
            return

        token = identifier.start
        self.check_identifier(token, StyleName.Parameter)

    def exitFunctionSignature(self, ctx: ObjectiveCParser.FunctionSignatureContext):
        """Check function names match the specified naming style."""
        identifier = ctx.identifier()
        if not identifier:
            return

        token = identifier.start
        self.check_identifier(token, StyleName.Function)

    def check_var_declaration(self, declaration: ObjectiveCParser.VarDeclarationContext,  style_name: StyleName):
        """Check variable declaration."""
        init_declarator_list = declaration.initDeclaratorList()
        if init_declarator_list is not None:
            for init_declarator in init_declarator_list.initDeclarator():
                identifier = init_declarator.declarator().directDeclarator().identifier()
                if not identifier:
                    return

                token = identifier.start
                self.check_identifier(token, style_name)

    def exitVarDeclaration(self, ctx: ObjectiveCParser.VarDeclarationContext):
        """Check global/local variable names match the specified naming style."""

        if self.match_tree(ctx, 'compoundStatement.declaration.varDeclaration'):
            self.check_var_declaration(ctx, StyleName.LocalVariable)
        elif self.match_tree(ctx, 'topLevelDeclaration.declaration.varDeclaration'):
            self.check_var_declaration(ctx, StyleName.GlobalVariable)
        elif self.match_tree(ctx, 'implementationDefinitionList.declaration.varDeclaration'):
            self.check_var_declaration(ctx, StyleName.GlobalVariable)
        elif self.match_tree(ctx, 'interfaceDeclarationList.declaration.varDeclaration'):
            self.check_var_declaration(ctx, StyleName.GlobalVariable)
        else:
            return

    def check_identifier(self, token: CommonToken, style_name: StyleName):
        # print("%s, %s" % (token, style_name))
        name = token.text
        style = self.get_naming_style(style_name)

        if self.match_style(name, style):
            return

        fixup = self.fixup_with_style(name, style)
        if fixup != name:
            explain_str = '建议使用："%s"。期望的格式为："%s"' % (fixup, style.explain_style())
        else:
            explain_str = '要求的格式为："%s"' % style.explain_style()

        self.diag("不合规的命名：'%s'，%s" % (name, explain_str), token.line, token.column)

    @classmethod
    def match_tree(cls, ctx: ParserRuleContext, tree):
        nodes = tree.split('.')
        nodes.reverse()

        def get_name(current_ctx: ParserRuleContext):
            rule_index = current_ctx.getRuleIndex()
            return ObjectiveCParser.ruleNames[rule_index]

        for node in nodes:
            rule_name = get_name(ctx)
            if rule_name != node:
                return False

            parent = ctx.parentCtx
            if not parent:
                return False
            ctx = parent

        return True

    @classmethod
    def get_pattern(cls, case_type):
        if case_type is CaseType.CamelCase:
            pattern = re.compile(r'^[A-Z][a-zA-Z0-9_]*$')
        elif case_type is CaseType.CamelBack:
            pattern = re.compile(r'^[a-z][a-zA-Z0-9_]*$')
        elif case_type is CaseType.LowerCase:
            pattern = re.compile(r'^[a-z_][a-z0-9_]*$')
        elif case_type is CaseType.UpperCase:
            pattern = re.compile(r'^[A-Z_][A-Z0-9_]*$')
        else:
            pattern = re.compile(r'^.*$')

        return pattern

    @classmethod
    def match_style(cls, name, style: NamingStyle):
        # "_" is a special name.
        if name == "_":
            return True

        matches = True
        if name.startswith(style.prefix):
            name = name[len(style.prefix):]
        else:
            matches = False

        if name.endswith(style.suffix):
            name = name[:len(name) - len(style.suffix)]
        else:
            matches = False

        pattern = cls.get_pattern(style.case)
        if not pattern.match(name):
            if style.case is CaseType.CamelBack and len(name) >= 2:
                # If the first two letters are upper case, we think it's a legal abbreviation.
                if not name[0:2].isupper():
                    matches = False
            else:
                matches = False

        return matches

    @classmethod
    def fixup_with_style(cls, name, style: NamingStyle):
        fixup = cls.fixup_with_case(name, style.case)
        mid = fixup.strip('_')
        return style.prefix + mid + style.suffix

    @classmethod
    def fixup_with_case(cls, name: str, case: CaseType):
        fixup = ""
        words = name.strip("_").split('_')
        words = [word for word in words if word]

        if case is CaseType.LowerCase:
            for index, word in enumerate(words):
                if index != 0:
                    fixup += '_'
                fixup += word.lower()
        elif case is CaseType.UpperCase:
            for index, word in enumerate(words):
                if index != 0:
                    fixup += '_'
                fixup += word.upper()
        elif case is CaseType.CamelBack:
            for index, word in enumerate(words):
                if index == 0:
                    fixup += word[0].lower()
                else:
                    fixup += '_'
                    fixup += word[0].capitalize()
                fixup += word[1:]
        elif case is CaseType.CamelCase:
            for index, word in enumerate(words):
                if index != 0:
                    fixup += '_'
                fixup += word[0].capitalize()
                fixup += word[1:]
        else:
            fixup = name

        return fixup

