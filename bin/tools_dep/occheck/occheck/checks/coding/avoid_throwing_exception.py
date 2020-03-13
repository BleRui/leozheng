from occheck.checks import BaseCheck


class AvoidThrowingExceptionCheck(BaseCheck):

    def __init__(self):
        super().__init__()

    def enterThrowStatement(self, ctx):
        token = ctx.start
        self.diag("应该避免@throw异常", token.line, token.column)

