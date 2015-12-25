from django.contrib import admin
from MedicalHistory.models import *

# Register your models here.
admin.site.register(MedProfile)
admin.site.register(Prescription)
admin.site.register(Condition)
admin.site.register(TestResult)
admin.site.register(InsurancePolicy)
admin.site.register(Appointment)