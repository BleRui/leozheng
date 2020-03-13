from occheck.checks import BaseCheck

LINE_THRESHOLD = -1


class FunctionSizeCheck(BaseCheck):

    def __init__(self):
        super().__init__()

        self.line_threshold = None

    def initialize(self):
        """Initialize this check here."""
        self.line_threshold = self.get_option_int("LineThreshold", LINE_THRESHOLD)

    def check_line_threshold(self, start_token, end_token):
        if self.line_threshold < 0:
            return

        if end_token.line - start_token.line + 1 > self.line_threshold:
            self.diag("函数体不应该超过%d行" % self.line_threshold, start_token.line)

    def exitMethodDefinition(self, ctx):
        compound = ctx.compoundStatement()
        start_token = compound.start
        end_token = compound.stop
        self.check_line_threshold(start_token, end_token)

    def exitFunctionDefinition(self, ctx):
        compound = ctx.compoundStatement()
        start_token = compound.start
        end_token = compound.stop
        self.check_line_threshold(start_token, end_token)
