import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from ..models import DoctorProfile, PatientProfile, NurseProfile, EmergencyContact

# def create_patient(uid, email, first_name, last_name, date_of_birth):
def create_patient_profile(**kwargs):
    """
    Factory method to create a patient with the given username 'uid', the
    first name 'first_name', the last_name 'last_name', the date_of_birth
    'date_of_birth', and the email 'email'
    """
    uid = kwargs.get('uid', None)
    email = kwargs.get('email', None)
    first_name = kwargs.get('first_name', None)
    last_name = kwargs.get('last_name', None)
    date_of_birth = kwargs.get('date_of_birth', None)

    user = User.objects.create(username=uid, email=email, first_name=first_name,
                               last_name=last_name)

    return PatientProfile.objects.create(user=user, date_of_birth=date_of_birth)


def create_doctor_profile(**kwargs):
    """
    Factory method to create a doctor with the given username 'uid', the
    first name 'first_name', the last_name 'last_name', and the associated
    patients 'patient_list'
    """
    uid = kwargs.get('uid', None)
    email = kwargs.get('email', None)
    first_name = kwargs.get('first_name', None)
    last_name = kwargs.get('last_name', None)
    patient_list = kwargs.get('patient_list', None)

    user = User.objects.create(username=uid, email=email, first_name=first_name,
                               last_name=last_name)

    return DoctorProfile.objects.create(user=user, patient_list=patient_list)


def create_nurse_profile(**kwargs):
    """
    Factory method to create a nurse with the given username 'uid', the
    first name 'first_name', the last_name 'last_name', and the associated
    patients 'patient_list'
    """
    uid = kwargs.get('uid', None)
    email = kwargs.get('email', None)
    first_name = kwargs.get('first_name', None)
    last_name = kwargs.get('last_name', None)
    patient_list = kwargs.get('patient_list', None)

    user = User.objects.create(username=uid, email=email, first_name=first_name,
                               last_name=last_name)

    return NurseProfile.objects.create(user=user, dpatient_list=patient_list)


def create_emergency_contact(**kwargs):
    """ Factory method to create an emergency contact
    """
    owner = kwargs.get('owner', None)
    email = kwargs.get('email', None)
    first_name = kwargs.get('first_name', None)
    last_name = kwargs.get('last_name', None)
    address = kwargs.get('address', None)
    home_phone = kwargs.get('home_phone', None)
    work_phone = kwargs.get('work_phone', None)

    return EmergencyContact.objects.create(owner=owner, first_name=first_name,
                                           last_name=last_name, address=address,
                                           home_phone=home_phone,
                                           work_phone=work_phone, email=email)


class TestUserManager(TestCase):
    """Test the behavior of the UserManager model
    """


class TestPatient(TestCase):
    """Test the behavior of the Patient model
    """

    def test_patient_not_staff(self):
        """ A patient account should be separate from a staff account
        """
        uid = "username"
        email = "mail@example.com"
        first_name = "Pat"
        last_name = "Ient"
        date_of_birth = timezone.now() - datetime.timedelta(weeks=52 * 28)

        patient = create_patient_profile(uid=uid, email=email,
                                 first_name=first_name, last_name=last_name,
                                 date_of_birth=date_of_birth)

        results = patient.is_staff
        expected = False

        self.assertEqual(expected, results)

    def test_patient_is_patient(self):
        """ A patient should be a patient by the reflexive property
        """
        uid = "username"
        email = "mail@example.com"
        first_name = "Pat"
        last_name = "Ient"
        date_of_birth = timezone.now() - datetime.timedelta(weeks=52 * 28)

        patient = create_patient_profile(uid=uid, email=email,
                                 first_name=first_name, last_name=last_name,
                                 date_of_birth=date_of_birth)

        results = patient.is_patient
        expected = True

        self.assertEqual(expected, results)

    def test_patient_clean_birth_date_in_future(self):
        """ A patient should not be able to claim to be born in the future
        """
        future_date = timezone.now() + datetime.timedelta(days=52 * 28)
        uid = "username"
        email = "mail@example.com"
        first_name = "Pat"
        last_name = "Ient"

        patient = create_patient_profile(uid=uid, email=email,
                                 first_name=first_name, last_name=last_name,
                                 date_of_birth=future_date)

        self.assertRaises(ValidationError, patient.clean)


class TestDoctor(TestCase):
    """Test the behavior of the Doctor model
    """


class TestNurse(TestCase):
    """Test the behavior of the Nurse model
    """


class TestEmergencyContact(TestCase):
    """ Test the emergency contacts
    """


class TestPersonalInformation(TestCase):
    """ Test personal information
    """