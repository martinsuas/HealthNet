from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from Users.models import Profile, PatientProfile, DoctorProfile


def generate_filename(self, filename):
    path = "FileStorage/users/%s/%s" % (self.user.profile.user.username, filename)
    return path


class Appointment(models.Model):
    user = models.ForeignKey(PatientProfile, related_name='appointment_users')
    doctor = models.ForeignKey(DoctorProfile, related_name='appointment_doctors')
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=400)
    date_created = models.DateTimeField()
    appointment_date = models.DateField()
    appointment_time = models.TimeField()


    def __str__(self):
        return str(self.name) + " - " + self.description[:30]


    def due_today(self):
        return self.appointment_date.day == timezone.now().day

    def past_due(self):
        return self.appointment_date <= timezone.now().date() and self.appointment_time < timezone.now().time()


    def get_patient(self):
        # Who's appointment is this
        return self.patient.get_username()

        # def get_doctor(self):
        # # Who's the doctor of this appointment
        # return self.doctor.get_username()

    @classmethod
    def create(cls, user, doctor, name, description, date_created, appointment_date, appointment_time):
        new = cls(user=user, doctor=doctor, name=name, description=description, date_created=date_created,
                  appointment_date=appointment_date, appointment_time=appointment_time)
        return new




class TestResult(models.Model):
    user = models.ForeignKey(PatientProfile, related_name='test_users')
    doctor = models.ForeignKey(DoctorProfile, related_name='test_doctors')
    test_name = models.CharField(
        max_length=30,
    )
    pub_date = models.DateTimeField()
    released = models.BooleanField()
    # uploads the file to /FileStorage/users/username/filename.extension
    report = models.FileField(upload_to=generate_filename)
    notes = models.TextField(blank=True, null=True, )

    def __str__(self):
        return self.test_name

    @classmethod
    def create(cls, user, doctor, test_name, pub_date, released, report, notes):
        new = cls(user=user, doctor=doctor, test_name=test_name, pub_date=pub_date, released=released, report=report,
                  notes=notes)
        return new

    class Meta:
        permissions = (
            ('can_view', 'Determines if a Users can view the test results'),
            ('can_edit', 'Determines if a Users can edit the test results'),
            ('can_release', 'Determines if a Users can release a test'),
            ('can_create', 'Determines if a Users can create a test result')
        )
        ordering = ['pub_date']
        verbose_name = 'Test Result'



class Prescription(models.Model):
    user = models.ForeignKey(PatientProfile, related_name='prescription_users')
    doctor = models.ForeignKey(DoctorProfile, related_name='prescription_test_doctors')
    drug_name = models.CharField(
        max_length=50
    )
    dosage = models.CharField(
        max_length=20
    )
    refills = models.IntegerField(
        default=0
    )
    direction = models.TextField()
    date_prescribed = models.DateField()
    #   prescribing_hospital = models.OneToOneField(Hospital)

    def __str__(self):
        return self.drug_name+':'+str(self.date_prescribed.month)+'/'+str(self.date_prescribed.year)

    @classmethod
    def create(cls, user, doctor, drug_name, dosage, refills, direction, date_prescribed):
        new = cls(user=user, doctor=doctor, drug_name=drug_name, dosage=dosage, refills=refills, direction=direction,
                  date_prescribed=date_prescribed)
        return new

    class Meta:
        permissions = (
            ('can_view', 'Determines if a Users can view the prescription'),
            ('can_edit', 'Determines if a Users can edit the prescription'),
            ('can_release', 'Determines if a Users can release a prescription'),
            ('can_create', 'Determines if a Users can create a prescription')
        )


class Condition(models.Model):
    user = models.ForeignKey(PatientProfile)

    name = models.CharField(
        max_length=20
    )
    currently_afflicted = models.BooleanField()
    date_diagnosed = models.DateField()
    date_recovered = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, user, name, currently_afflicted, date_recovered, date_diagnosed):
        new = cls(user=user, name=name, currently_afflicted=currently_afflicted, date_recovered=date_recovered,
                  date_diagnosed=date_diagnosed)
        return new
    class Meta:
        ordering = ['currently_afflicted', 'date_diagnosed']
        permissions = (
            ('can_view', 'Determines if a Users can view the condition'),
            ('can_edit', 'Determines if a Users can edit the condition'),
            ('can_release', 'Determines if a Users can release a condition'),
            ('can_create', 'Determines if a Users can create a condition')
        )


class InsurancePolicy(models.Model):
    user = models.OneToOneField(PatientProfile)
    company = models.CharField(
        max_length=30
    )
    insurance_id = models.SlugField()
    policy_number = models.SlugField()

    def __str__(self):
        return self.company+':'+str(self.insurance_id)

    @classmethod
    def create(cls, user, company, insurance_id, policy_number):
        new = cls(user=user, company=company, insurance_id=insurance_id, policy_number=policy_number)
        return new

    class Meta:
        permissions = (
            ('can_view', 'Determines if a Users can view the Insurance Policy'),
            ('can_edit', 'Determines if a Users can edit the Insurance Policy'),
        )
        verbose_name_plural = 'Insurance Policies'


class MedProfile(models.Model):
    patient = models.ForeignKey(PatientProfile)
    prescriptions = models.ForeignKey(
        Prescription,
        blank=True,
        null=True,
    )
    conditions = models.ForeignKey(
        Condition,
        blank=True,
        null=True,
    )
    insurance_policy = models.OneToOneField(
        InsurancePolicy,
        unique=True,
        blank=True,
        null=True,
    )
    tests = models.ForeignKey(
        TestResult,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.patient.first_name

    class Meta:
        permissions = (
            ('can_view', 'Determines if a Users can view the MedProfile'),
            ('can_edit', 'Determines if a Users can edit the MedProfile'),
        )