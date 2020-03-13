from . import BaseReporter


class TextReporter(BaseReporter):

    def write_line(self, line):
        self.output_stream.write(line)
        self.output_stream.write("\n")

    def add_diag(self, diag):
        self.write_line(str(diag))

    def dump(self):
        self.output_stream.write("\n")
        return super().dump()
