import json
from . import BaseReporter


class JSONReporter(BaseReporter):

    def __init__(self, output_stream):
        super().__init__(output_stream)
        self.diagnostics = []

    def add_diag(self, diag):
        diagnostic = {
            "CheckName": diag.check_name,
            "Message": diag.message,
            "FilePath": diag.file_path,
            "Line": diag.line,
            "Column": diag.column
        }
        self.diagnostics.append(diagnostic)

    def dump(self):
        output = json.dumps(self.diagnostics, indent=2)
        return output
