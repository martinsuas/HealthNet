from django.contrib import admin
from Users.models import Profile, PatientProfile, DoctorProfile, NurseProfile, EmergencyContact, \
    AdminProfile, SecretaryProfile

# Registered UserProfiles
admin.site.register(Profile)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(NurseProfile)
admin.site.register(AdminProfile)
admin.site.register(SecretaryProfile)
admin.site.register(EmergencyContact)