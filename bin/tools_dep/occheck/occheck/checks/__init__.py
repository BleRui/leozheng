from ..grammar.ObjectiveCParserListener import ObjectiveCParserListener
from ..diagnostic import Diagnostic


__all__ = ["BaseCheck", "CheckRegistry"]


class BaseCheck(ObjectiveCParserListener):
    def __init__(self):
        super().__init__()
        self.check_name = None
        self.current_file = None
        self.consumer = None

        # FileContext
        self.context = None
        self.options = None

    def diag(self, message, line, column=0):
        """Add a diagnostic with the check's name.
        """
        diag = Diagnostic(self.current_file, self.check_name, message, line, column)
        self.consumer.consume_diagnostic(diag, self.context)

    def initialize(self):
        """Initialize this check."""

    def begin_check(self, filename):
        """Begin check a new file."""

    def finish_check(self, filename):
        """Finished check the file."""

    def get_current_filename(self):
        """Get the name of the currently analyzed file."""
        return self.context.get_current_file()

    def get_source_code(self):
        """Return the source code."""
        return self.context.get_source_code()

    def get_lines(self):
        """Return the lines with line ending kept."""
        return self.context.get_lines()

    def get_name(self):
        return self.check_name

    def get_option(self, key, default):
        desired_key = "%s.%s" % (self.check_name, key)

        for option in self.options:
            if option["key"] == desired_key:
                return option["value"]

        return default

    def get_option_int(self, key, default):
        option = self.get_option(key, default)
        return int(option)

    def get_ast(self):
        return self.context.get_ast()

    def get_parser(self):
        return self.context.get_parser()

    def set_name(self, name):
        """Specify check name"""
        self.check_name = name

    def set_consumer(self, consumer):
        """Set consumer of diagnostics."""
        self.consumer = consumer

    def set_current_context(self, context):
        """Set the current FileContext."""
        self.context = context
        self.current_file = context.get_current_file()

    def set_options(self, check_options):
        self.options = check_options


class CheckRegistry:
    _checks = dict()

    @classmethod
    def register_check(cls, check_name, check_cls):
        cls._checks[check_name] = check_cls

    @classmethod
    def create_check(cls, check_name):
        check_cls = cls._checks[check_name]
        return check_cls()

    @classmethod
    def get_check(cls, check_name):
        return cls._checks[check_name]

    @classmethod
    def list_checks(cls):
        return list(cls._checks.keys())


def _register_builtin_module():
    """register builtin module here."""

    from . import readability
    from . import coding


# def _register_legacy_checks():
#     import occheck.rules


_register_builtin_module()
# _register_legacy_checks()
