__author__ = 'Scott'

from django import forms
from Hospital.models import Hospital


class AdmitPatientQuery(forms.Form):
    error_css_class = "alert alert-danger"
    patient = forms.CharField(
        label='Patient',
        widget=forms.TextInput(
            attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'Enter Username of Patient to Admit'})
        )


class DischargePatientQuery(forms.Form):
    error_css_class = "alert alert-danger"
    patient = forms.CharField(
        label='Patient',
        widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control',
                                      'placeholder': 'Enter Username of Patient to Discharge'})
        )



    #
    # class TransferPatient(forms.ModelForm):
    # class Meta:
    # model = Hospital
    # fields = (
    #             'patient_list',
    #             'from_hospital',
    #             'to_hospital',
    #         )
    #
    #
    # class StaffListModify(forms.ModelForm):
    #     class Meta:
    #         model = Hospital
    #         fields = (
    #             'doctor_list',
    #             'staff_list',
    #         )