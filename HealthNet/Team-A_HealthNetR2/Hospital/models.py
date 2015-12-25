from django.db import models
from Users.models import PatientProfile, DoctorProfile, NurseProfile, AdminProfile, SecretaryProfile

# Create your models here.


class Hospital(models.Model):
    # Details of the Hospital
    name = models.CharField(max_length=100, blank=False)
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()

    # Lists of all the people in the hospital
    patient_list = models.ManyToManyField(PatientProfile, blank=True, null=True)
    doctor_list = models.ManyToManyField(DoctorProfile, blank=True, null=True)
    nurse_list = models.ManyToManyField(NurseProfile, blank=True, null=True)
    admin_list = models.ManyToManyField(AdminProfile, blank=True, null=True)
    secretary_list = models.ManyToManyField(SecretaryProfile, blank=True, null=True)

    def checkin(self, patient):
        #   adds given patient to the patient list and changes their status to
        #   admitted
        self.patient_list.add(patient)
        patient.admitted = True

    def checkout(self, patient):
        #   removes given patient from the patient list and changes their
        #   status to discharged
        self.patient_list.remove(patient)
        patient.admitted = False

    def add_nurse(self, staff):
        #   Used to add a new staff member to the list
        self.nurse_list.add(staff)

    def remove_nurse(self, staff):
        #   Used to remove a staff from the list
        self.nurse_list.remove(staff)

    def add_doctor(self, doc):
        #   Used to add a doctor to the list
        self.doctor_list.add(doc)

    def remove_doctor(self, doc):
        #   used to remove a doctor from the list
        self.doctor_list.remove(doc)

    def add_admin(self, doc):
        #   Used to add a doctor to the list
        self.admin_list.add(doc)

    def remove_admin(self, doc):
        #   used to remove a doctor from the list
        self.admin_list.remove(doc)

    def add_secretary(self, doc):
        #   Used to add a doctor to the list
        self.secretary_list.add(doc)

    def remove_secretary(self, doc):
        #   used to remove a doctor from the list
        self.secretary_list.remove(doc)

    def getConditonStats(self, condition):
        return 1
        #   TODO Implement
        # Returns all of the condition that the patients have and the number of
        #   people with them

    def getPrescriptionStats(self, prescription):
        return 0
        # TODO Implement
        # Returns all of the condition that the patients have and the number of
        #   people with them


    def getPatientStats(self):
        return None
    #   TODO Implement
    #   returns the current number of patients in the hospital

    def __str__(self):
        return self.name