from .. import CheckRegistry
from .avoid_throwing_exception import AvoidThrowingExceptionCheck


def register_checks():
    CheckRegistry.register_check("coding-avoid-throwing-exception", AvoidThrowingExceptionCheck)
    pass


register_checks()

