__author__ = 'Martin'

from django.forms import Textarea, extras
from django import forms
from django.forms.widgets import DateTimeInput, SplitDateTimeWidget, DateInput, TimeInput
from MedicalHistory.models import Appointment, Prescription


class AppointmentModify(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = (
            'user',
            'doctor',
            'name',
            'appointment_date',
            'appointment_time',
            'description',

        )
        widgets = {
            'description': Textarea(attrs={'cols':60, 'rows':5}),
            'appointment_date': extras.SelectDateWidget,
        }



class PrescriptionModify(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = (
            'user',
            'doctor',
            'drug_name',
            'dosage',
            'refills',
            'direction',
        )