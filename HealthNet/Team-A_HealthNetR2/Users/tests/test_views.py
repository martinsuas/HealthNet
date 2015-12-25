from django.test import TestCase

from ..views import profile, register, user_login, user_logout

class TestProfile(TestCase):
    """ This tests that the index behaves as we expect.
    """


class TestLogin(TestCase):
    """ This tests that the login page behaves as expected.
    """


class TestRegister(TestCase):
    """ This tests that registration works as we expect.
    """


class TestLogout(TestCase):
    """ This tests that logout behaves properly.
    """


class TestHome(TestCase):
    """ This tests that the home view is operational.
    """