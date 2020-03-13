from itertools import takewhile

from occheck.checks import BaseCheck

SPACES = "spaces"
TABS = "tabs"
INDENT_SIZE = 4


class IndentCheck(BaseCheck):

    def __init__(self):
        super().__init__()
        self.indent_style = None
        self.indent_size = None
        self.indent_str = None

    def initialize(self):
        """Initialize this check here."""
        self.indent_style = self.get_option("IndentStyle", SPACES)
        self.indent_size = self.get_option_int("IndentSize", INDENT_SIZE)
        self.indent_str = self.get_indent_str(self.indent_style, self.indent_size)

    def begin_check(self, filename):
        """Begin check a new file."""

        lines = self.get_lines()

        for index, line in enumerate(lines):
            indent = ''.join([x for x in takewhile(lambda x: x in '\t ', line)])
            if not indent:
                continue

            if self.indent_style == SPACES:
                if '\t' in indent:
                    self.diag("禁止使用tab键", index + 1)
                    continue

                # We do not check whether the line starts with multiple indent string, because of
                # the clang-format tool generates codes not always strictly indent-aligned.
                if line.startswith(self.indent_str):
                    continue

                if self.is_ignored(index, lines):
                    continue

                self.diag("缩进应该使用%d个空格" % self.indent_size, index + 1)
            else:
                if not line.startswith(self.indent_str):
                    self.diag("缩进应该使用tab键", index + 1)

    def finish_check(self, filename):
        """Finished check the file."""

    @classmethod
    def is_ignored(cls, line_num, lines):

        current_line = lines[line_num].lstrip()

        # This line is started with '/*'.
        if current_line.startswith("/*"):
            return False

        # This line is the end line of the block comments.
        if "*/" in current_line:
            if "/*" not in current_line:
                return True

            # The block comments end marker comes before begin marker.
            if current_line.find("*/") < current_line.find("/*"):
                return True
            else:
                return False
        elif "/*" in current_line:
            return False

        # This line is in the middle of the block comments.
        block_comments_begin = None

        for index, line in enumerate(lines[line_num:]):
            if "/*" in line:
                block_comments_begin = {"Line": index, "Column": line.find("/*")}

            if "*/" in line:
                block_comments_end = {"Line": index, "Column": line.find("*/")}
                # print("%d, %d, %d" % (line_num, index, block_comments_end["Column"]))

                # The block comments end marker found first.
                if not block_comments_begin:
                    return True

                if block_comments_begin["Line"] < block_comments_end["Line"]:
                    return False

                # The block comments end marker comes before begin marker.
                if block_comments_begin["Line"] > block_comments_end["Line"]:
                    return True
                if block_comments_begin["Column"] > block_comments_end["Column"]:
                    return True

                break

        return False

    @classmethod
    def get_indent_str(cls, indent_style, indent_size):
        if indent_style == TABS:
            indent_str = "\t"
        else:
            indent_str = "".join((" " for _ in range(indent_size)))

        return indent_str
