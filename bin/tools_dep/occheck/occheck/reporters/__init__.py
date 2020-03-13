
class BaseReporter:
    """Base class for reporters.
    """

    def __init__(self, output_stream):
        self.output_stream = output_stream

    def add_diag(self, diag):
        """Report a diagnostic."""

    def dump(self):
        """Serialize diagnostics to a formatted str."""
        return ""


class ReporterRegistry:

    _reporters = dict()

    @classmethod
    def register_reporter(cls, name, reporter_cls):
        cls._reporters[name] = reporter_cls

    @classmethod
    def create_reporter(cls, name, output_stream):
        reporter_cls = cls._reporters[name]
        return reporter_cls(output_stream)

    @classmethod
    def has_reporter(cls, name):
        return name in cls._reporters


def _register_reporters():
    from .json_reporter import JSONReporter
    from .text_reporter import TextReporter

    ReporterRegistry.register_reporter("json", JSONReporter)
    ReporterRegistry.register_reporter("text", TextReporter)


_register_reporters()
