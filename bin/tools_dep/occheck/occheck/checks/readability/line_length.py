from occheck.checks import BaseCheck


class LineLengthCheck(BaseCheck):

    def __init__(self):
        super().__init__()
        self.max_line_length = None
        self.tab_width = None

    def initialize(self):
        """Initialize this check here."""
        self.tab_width = self.get_option_int("TabWidth", 4)
        self.max_line_length = self.get_option_int("MaxLineLength", 80)

    def begin_check(self, filename):
        """Begin check a new file."""

        lines = self.get_lines()

        for index, line in enumerate(lines):
            line_length = self.calc_line_length(line)
            if line_length > self.max_line_length:
                self.diag("行长度不应该超过%d" % self.max_line_length, index + 1)

    def calc_line_length(self, line):
        line_length = 0

        for x in line:
            if x == '\t':
                line_length += self.tab_width
            else:
                line_length += 1

        return line_length
