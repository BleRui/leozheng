from .. import CheckRegistry
from .function_size import FunctionSizeCheck
from .identifier_naming import IdentifierNamingCheck
from .line_length import LineLengthCheck
from .indent import IndentCheck


def register_checks():
    CheckRegistry.register_check("readability-function-size", FunctionSizeCheck)
    CheckRegistry.register_check("readability-identifier-naming", IdentifierNamingCheck)
    CheckRegistry.register_check("readability-line-length", LineLengthCheck)
    CheckRegistry.register_check("readability-indent", IndentCheck)
    pass


register_checks()

