from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from ..forms import UserForm, PatientProfileForm


class UserForm(TestCase):
    """ Test the behaviors of the form to log in
    """


class TestPatientProfileForm(TestCase):
    """ Test the behaviors of the form to register
    """

    def test_passwords_match(self):
        """ Same passwords should be accepted
        """
        username = "user123"
        password = "password"
        password2 = "password"
        email = "mail@example.com"

        # should not raise a ValidationError
        response = self.client.post('users/register.html', {
            'username': username,
            'password': password,
            'password2': password2,
            'email': email,
        })



