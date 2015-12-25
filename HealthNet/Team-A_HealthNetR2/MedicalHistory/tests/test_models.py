from django.test import TestCase
from django.contrib.auth.models import User
from MedicalHistory.models import TestResult, Prescription, Condition, InsurancePolicy, Appointment
from django.utils import timezone
import time, datetime


class TestTestResults(TestCase):
    """ Tests results of the test results model.
    """


class TestAppointment(TestCase):
    """ Tests functions of appointments.
    """

    def test_due_today(self):
        appointment = Appointment()
        appointment.appointment_date = time.localtime()
        self.assertEqual(appointment.due_today(), True)

    def test_not_due_today_after(self):
        """ Tests that we do not say an appointment due after today is due.
        """
        appointment = Appointment()
        appointment.appointment_date = time.localtime() + datetime.timedelta(days=1)
        self.assertEqual(appointment.due_today(), False)

    def test_not_due_today_before(self):
        """ Tests that we do not say an appointment due before today is due.
        """
        appointment = Appointment()
        appointment.appointment_date = time.localtime() - datetime.timedelta(days=1)
        self.assertEqual(appointment.due_today(), False)


    def test_past_due(self):
        appointment = Appointment()
        appointment.appointment_date = timezone.now().date()
        appointment.appointment_time = timezone.now().time() + timezone.timedelta(minutes=1)
        self.assertEqual(appointment.past_due(), False)
        appointment.appointment_time = timezone.now().time() - timezone.timedelta(minutes=1)
        self.assertEqual(appointment.past_due(), True)

    def test_get_patient(self):
        appointment = Appointment()
        appointment_user = User()
        appointment.user = appointment_user
        self.assertEqual(appointment.user, appointment_user)


class TestPrescription(TestCase):
    """ Tests functionality of prescriptions.
    """


class TestCondition(TestCase):
    """ Tests the condition model.
    """


class TestInsurancePolicy(TestCase):
    """ Ensures the insurance policy works.
    """


class TestMedProfile(TestCase):
    """ Tests medical profile functionality.
    """