from django.db import models
from django.contrib.auth.models import User

# from django.contrib.auth.models import Group
# users_is_patient = Group.objects.get(name="patient").user_set.all()
# users_is_doctor = Group.objects.get(name="doctor").user_set.all()
# users_is_nurse = Group.objects.get(name="nurse").user_set.all()


CHOICES = (
    ('Patient', 'Patient'),
    ('Doctor',  'Doctor'),
    ('Nurse',   'Nurse'),
    ('Admin',   'Admin'),
    ('Secretary', 'Secretary')
)

class Profile(models.Model):
    user = models.OneToOneField(User)
    role = models.CharField(max_length=10, choices=CHOICES)
    first_name = models.CharField(max_length= 20)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(blank=False)
    home_phone_number = models.CharField(max_length=14, blank=True, )
    work_phone_number = models.CharField(max_length=14, )
    cell_phone_number = models.CharField(max_length=14, blank=True,)

    def __str__(self):
        return self.user.username

    def get_name(self):
        return self.first_name + " " + self.last_name

    def get_role(self):
        return self.role





# This class is the patient profile which implements the
class PatientProfile(models.Model):
    # Link to a default Django Users
    profile = models.OneToOneField(Profile)
    # additional Users information
    date_of_birth = models.DateField()
    home_address = models.CharField(max_length=100, )

    def __str__(self):
        return self.profile.user.username

    def get_name(self):
        return self.profile.first_name + " " + self.profile.last_name


class DoctorProfile(models.Model):
    profile = models.OneToOneField(Profile)

    patient_list = models.ManyToManyField(PatientProfile, blank=True)

    def __str__(self):
        return self.profile.user.username

    def get_name(self):
        return self.profile.first_name + " " + self.profile.last_name


class NurseProfile(models.Model):
    profile = models.OneToOneField(Profile)

    patient_list = models.ManyToManyField(PatientProfile)

    def __str__(self):
        return self.profile.user.username

    def get_name(self):
        return self.profile.first_name + " " + self.profile.last_name


class AdminProfile(models.Model):
    profile = models.OneToOneField(Profile)

    def __str__(self):
        return self.profile.user.username
    def get_name(self):
        return self.profile.first_name + " " + self.profile.last_name


class SecretaryProfile(models.Model):
    profile = models.OneToOneField(Profile)

    def __str__(self):
        return self.profile.user.username

    def get_name(self):
        return self.profile.first_name + " " + self.profile.last_name


class EmergencyContact(models.Model):
    owner = models.ForeignKey(User, unique=False)
    first_name = models.CharField(
        max_length=20
    )
    last_name = models.CharField(
        max_length=20
    )
    address = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    home_phone = models.IntegerField(
        max_length=11
    )
    cell_phone = models.IntegerField(
        max_length=11,
        blank=True,
        null=True
    )
    work_phone = models.IntegerField(
        max_length=11,
        blank=True
    )
    email = models.EmailField()

    def __str__(self):
        return self.last_name + " " + self.first_name

    def get_name(self):
        return self.first_name+" "+self.last_name

    @classmethod
    def create(cls, owner, first_name, last_name, address, home_phone, cell_phone, work_phone, email):
        new = cls(owner=owner, first_name=first_name, last_name=last_name,
                  address=address, home_phone=home_phone, cell_phone=cell_phone, work_phone=work_phone, email=email)
        return new

    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (
            ('can_view', 'Allows users to view emergency contacts'),
            ('can_edit', 'Allows users to edit emergency contacts'),
        )