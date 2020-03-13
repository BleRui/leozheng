import codecs
import re


class Diagnostic:

    def __init__(self, file_path, check_name, message, line, column=None):
        self.file_path = file_path
        self.check_name = check_name
        self.message = message
        self.line = line
        self.column = column

    def get_check_name(self):
        return self.check_name

    def __repr__(self):
        column = self.column if self.column else 0
        return "%s:%s:%s: %s [%s]" % (self.file_path, self.line, column, self.message, self.check_name)

    def __str__(self):
        return self.__repr__()


class DiagnosticConsumer:

    def __init__(self, reporter):
        self.reporter = reporter

    def consume_diagnostic(self, diag, context):
        if not self.is_line_marked_with_nolint(diag, context):
            self.reporter.add_diag(diag)

    @classmethod
    def is_nolint_found(cls, nolint_directive, line, diag, context):
        nolint_index = line.find(nolint_directive)
        if nolint_index < 0:
            return False

        pattern = r"%s\s*\((?P<checks>.*)\)" % nolint_directive
        match = re.match(pattern, line[nolint_index:])
        if match:
            checks_str = match.group("checks").strip()
            # Allow disable all the checks with "*".
            if checks_str == "*":
                return True

            checks = list(map(lambda x: x.strip(),  checks_str.split(',')))
            check_name = diag.get_check_name()
            return check_name in checks

        return True

    @classmethod
    def is_line_marked_with_nolint(cls, diag, context):
        # Check if there has a NOLINT on this line.
        line = context.get_lines()[diag.line - 1].rstrip()
        reset_of_line = line[diag.column:]

        if cls.is_nolint_found("NOLINT", reset_of_line, diag, context):
            return True

        if diag.line < 2:
            return False

        # Check if there has a NOLINTNEXTLINE on the previous line.
        line = context.get_lines()[diag.line - 2].rstrip()
        if cls.is_nolint_found("NOLINTNEXTLINE", line, diag, context):
            return True

        return False
