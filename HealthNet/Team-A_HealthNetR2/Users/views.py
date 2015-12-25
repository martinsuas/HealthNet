from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from Users.forms import UserForm, ProfileForm, PatientProfileForm, EditProfile, EditPatient
from django.db import models
from Users.models import Profile, PatientProfile, DoctorProfile, NurseProfile, EmergencyContact, SecretaryProfile, \
    AdminProfile
from Hospital.models import Hospital
from MedicalHistory.models import InsurancePolicy, Prescription, Condition, TestResult
import logging

logger = logging.getLogger('general')

def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = request.user
        if active_user.profile.role == 'Patient':
            name = active_user.profile.get_name()
        elif active_user.profile.role == 'Doctor':
            name = "Dr. " + active_user.profile.get_name()
        elif active_user.profile.role == 'Nurse':
            name = "Nurse " + active_user.profile.get_name()
        elif active_user.profile.role == "Secretary":
            name = 'Secretary' + active_user.profile.get_name()
            return render(request, 'Users/home.html', {'name': name})
        elif active_user.profile.role == 'Admin':
            name = 'Administrator, ' + active_user.profile.get_name()
            return render(request, 'Users/home.html', {'name': name})
        else:
            name = active_user.username
        return render(request, 'Users/home.html', {'name': name})



def profile(request, username):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = request.user
        if active_user.profile.role == 'Patient':
            name = active_user.profile.get_name()
        elif active_user.profile.role == 'Doctor':
            name = "Dr. " + active_user.profile.get_name()
            num_patients = len(active_user.profile.doctorprofile.patient_list.all())
            hospital_list = Hospital.objects.all()
            return render(request, 'Users/Staff/Doctor/doctor_profile.html',
                          {"name": name, 'patient_num': num_patients, 'hospital_list': hospital_list})
        elif active_user.profile.role == 'Nurse':
            name = "Nurse " + active_user.profile.get_name()
            num_patients = len(active_user.profile.nurseprofile.patient_list.all())
            hospital_list = Hospital.objects.all()
            return render(request, 'Users/Staff/Nurse/profile.html',
                          {"name": name, 'patient_num': num_patients, 'hospital_list': hospital_list})
        elif active_user.profile.role == "Secretary":
            name = 'Secretary' + active_user.profile.get_name()
            hospital_list = Hospital.objects.all()
            return render(request, 'Users/Staff/Secretary/profile.html', {'name': name, 'hospital_list': hospital_list})
        elif active_user.profile.role == 'Admin':
            name = 'Administrator, ' + active_user.profile.get_name()
            hospital_list = Hospital.objects.all()
            return render(request, 'Users/Staff/Admin/profile.html', {'name': name, 'hospital_list': hospital_list})
        else:
            name = active_user.username
        return render(request, 'Users/Patient/patient_profile.html', {"name": name, 'user': active_user})


# This registers a standard user "Patient" to the web page
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)
        patient_profile_form = PatientProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid() and patient_profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            standard_profile = profile_form.save(commit=False)
            standard_profile.user = user
            standard_profile.role = 'Patient'
            standard_profile.save()
            patient_profile = patient_profile_form.save(commit=False)
            patient_profile.profile = standard_profile
            patient_profile.save()
            registered = True
            logger.info(str(user) + " has registered into HealthNet.")
        else:
            print(user_form.errors, profile_form.errors, patient_profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = ProfileForm()
        patient_profile_form = PatientProfileForm()

    return render(
        request,
        'Users/register.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'patient_profile_form': patient_profile_form,
            'registered': registered
        }
    )


def user_login(request):
    auth = 3
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                auth = 0
                return HttpResponseRedirect(reverse('user:home'))
            else:
                auth = 1
                return HttpResponse('Your HealthNet account is inactive.'
                                    '<a href=' + reverse('user:login') + '>Return to login?.</a>')
        else:
            print("Invalid login: {0}, {1}".format(username, password))
            auth = 2
            return render(request, 'Users/login.html', {'authenticated': auth})

    else:
        return render(request, 'Users/login.html', {'authenticated': auth})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def profile_edit(request, username):
    # Almost working need to either create another form to ignore the username and password or figure out a workaround
    # There is another issue with the html where the date has to be set every time you want to edit
    # This page is still broken with my update to the User model
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = get_object_or_404(User, username=username)
        profile = Profile.objects.filter(user=active_user)
        user_profile = get_object_or_404(profile)
        if active_user.profile.role == 'Patient':

            patient_profile = PatientProfile.objects.filter(profile=user_profile)
            patient_profile = get_object_or_404(patient_profile)

            if request.method == 'POST':
                user_profile.email = request.POST.get('Email')
                user_profile.first_name = request.POST.get('FirstName')
                user_profile.middle_name = request.POST.get('MiddleName')
                user_profile.last_name = request.POST.get('LastName')
                # patient profile isn't working right still
                if request.POST.get('DateofBirth'):
                    patient_profile.date_of_birth = request.POST.get('DateofBirth')
                patient_profile.home_address = request.POST.get('HomeAddress')
                user_profile.home_phone_number = request.POST.get('HomePhone')
                user_profile.cell_phone_number = request.POST.get('WorkPhone')
                user_profile.work_phone_number = request.POST.get('CellPhone')
                user_profile.save()
                patient_profile.save()
                logger.info(str(request.user) + " has updated its profile." )
                return redirect('user:profile', username=username)

            else:
                return render(
                    request,
                    'Users/Patient/patient_edit.html',
                    {'user': active_user, 'profile': user_profile, 'patient_profile': patient_profile}
                )
        elif active_user.profile.role == 'Doctor':
            doctor_profile = DoctorProfile.objects.filter(profile=user_profile)
            doctor_profile = get_object_or_404(doctor_profile)
            hospital_list = Hospital.objects.all()

            if request.method == 'POST':
                user_profile.email = request.POST.get('Email')
                user_profile.first_name = request.POST.get('FirstName')
                user_profile.middle_name = request.POST.get('MiddleName')
                user_profile.last_name = request.POST.get('LastName')
                user_profile.home_phone_number = request.POST.get('HomePhone')
                user_profile.cell_phone_number = request.POST.get('WorkPhone')
                user_profile.work_phone_number = request.POST.get('CellPhone')
                user_profile.save()
                return redirect('user:profile', username=username)
            else:
                return render(request, 'Users/Staff/Doctor/doctor_edit.html',
                              {'user': active_user, 'profile': user_profile, 'doctor_profile': doctor_profile,
                               'hospital_list': hospital_list})
        elif active_user.profile.role == 'Nurse':
            nurse_profile = NurseProfile.objects.filter(profile=user_profile)
            nurse_profile = get_object_or_404(nurse_profile)
            hospital_list = Hospital.objects.all()

            if request.method == 'POST':
                user_profile.email = request.POST.get('Email')
                user_profile.first_name = request.POST.get('FirstName')
                user_profile.middle_name = request.POST.get('MiddleName')
                user_profile.last_name = request.POST.get('LastName')
                user_profile.home_phone_number = request.POST.get('HomePhone')
                user_profile.cell_phone_number = request.POST.get('WorkPhone')
                user_profile.work_phone_number = request.POST.get('CellPhone')
                user_profile.save()
                return redirect('user:profile', username=username)
            else:
                return render(request, 'Users/Staff/Nurse/profile_edit.html',
                              {'user': active_user, 'profile': user_profile, 'nurse_profile': nurse_profile,
                               'hospital_list': hospital_list})

        elif active_user.profile.role == 'Secretary':
            secretary_profile = SecretaryProfile.objects.filter(profile=user_profile)
            secretary_profile = get_object_or_404(secretary_profile)
            hospital_list = Hospital.objects.all()

            if request.method == 'POST':
                user_profile.email = request.POST.get('Email')
                user_profile.first_name = request.POST.get('FirstName')
                user_profile.middle_name = request.POST.get('MiddleName')
                user_profile.last_name = request.POST.get('LastName')
                user_profile.home_phone_number = request.POST.get('HomePhone')
                user_profile.cell_phone_number = request.POST.get('WorkPhone')
                user_profile.work_phone_number = request.POST.get('CellPhone')
                user_profile.save()
                return redirect('user:profile', username=username)
            else:
                return render(request, 'Users/Staff/Secretary/profile_edit.html',
                              {'user': active_user, 'profile': user_profile, 'secretary_profile': secretary_profile,
                               'hospital_list': hospital_list})
        elif active_user.profile.role == 'Nurse':
            nurse_profile = NurseProfile.objects.filter(profile=user_profile)
            nurse_profile = get_object_or_404(nurse_profile)
            hospital_list = Hospital.objects.all()

            if request.method == 'POST':
                user_profile.email = request.POST.get('Email')
                user_profile.first_name = request.POST.get('FirstName')
                user_profile.middle_name = request.POST.get('MiddleName')
                user_profile.last_name = request.POST.get('LastName')
                user_profile.home_phone_number = request.POST.get('HomePhone')
                user_profile.cell_phone_number = request.POST.get('WorkPhone')
                user_profile.work_phone_number = request.POST.get('CellPhone')
                user_profile.save()
                return redirect('user:profile', username=username)
            else:
                return render(request, 'Users/Staff/Nurse/profile_edit.html',
                              {'user': active_user, 'profile': user_profile, 'nurse_profile': nurse_profile,
                               'hospital_list': hospital_list})
        elif active_user.profile.role == 'Admin':
            admin_profile = AdminProfile.objects.filter(profile=user_profile)
            admin_profile = get_object_or_404(admin_profile)
            hospital_list = Hospital.objects.all()

            if request.method == 'POST':
                user_profile.email = request.POST.get('Email')
                user_profile.first_name = request.POST.get('FirstName')
                user_profile.middle_name = request.POST.get('MiddleName')
                user_profile.last_name = request.POST.get('LastName')
                user_profile.home_phone_number = request.POST.get('HomePhone')
                user_profile.cell_phone_number = request.POST.get('WorkPhone')
                user_profile.work_phone_number = request.POST.get('CellPhone')
                user_profile.save()
                return redirect('user:profile', username=username)
            else:
                return render(request, 'Users/Staff/Admin/profile_edit.html',
                              {'user': active_user, 'profile': user_profile, 'admin_profile': admin_profile,
                               'hospital_list': hospital_list})
        else:
            return render(request, 'PermissionDenied.html')


def contact(request, username):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = get_object_or_404(User, username=username)
        contact_list = EmergencyContact.objects.filter(owner=active_user)
        return render(request, 'Users/EmergencyContacts/contacts.html', {'contact_list': contact_list})


def contact_details(request, username, pk):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        contact = get_object_or_404(EmergencyContact, pk=pk)
        return render(request, 'Users/EmergencyContacts/contact_detail.html', {'contact': contact})


def contact_edit(request, username, pk):
    # there is a bug here
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        contact = get_object_or_404(EmergencyContact, pk=pk)
        if request.method == 'POST':
            contact.first_name = request.POST.get('first_name')
            contact.last_name = request.POST.get('last_name')
            contact.address = request.POST.get('address')
            contact.home_phone = request.POST.get('home_phone')
            contact.cell_phone = request.POST.get('work_phone')
            contact.work_phone = request.POST.get('cell_phone')
            contact.email = request.POST.get('email')
            contact.save()
            logger.info(str(request.user) + " updated contact information.")
            return redirect('user:contact', username=username)
        else:
            return render(request, 'Users/EmergencyContacts/edit_contacts.html', {'contact': contact})


def create_contact(request, username):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = get_object_or_404(User, username=username)
        if request.method == 'POST':
            owner = active_user
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            address = request.POST.get('address')
            home_phone = request.POST.get('home_phone')
            cell_phone = request.POST.get('work_phone')
            work_phone = request.POST.get('cell_phone')
            email = request.POST.get('email')
            contact = EmergencyContact.create(owner, first_name, last_name, address, home_phone, cell_phone, work_phone,
                                              email)
            contact.save()
            logger.info(str(request.user) + " created contact information.")
            return HttpResponseRedirect(reverse('user:contact', args={username}))
        else:
            return render(request, 'Users/EmergencyContacts/create_contact.html', {})


def view_patient(request, username, patient):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = get_object_or_404(User, username=username)
        user_profile = active_user.profile
        if active_user.profile.role == 'Doctor':
            hospital_list = Hospital.objects.all()
            doctor_profile = get_object_or_404(DoctorProfile, profile=user_profile)
            patient = get_object_or_404(User, username=patient)
            insurance = get_object_or_404(InsurancePolicy, user=patient.profile.patientprofile)
            prescription = Prescription.objects.filter(user=patient.profile.patientprofile)
            conditions = Condition.objects.filter(user=patient.profile.patientprofile)
            tests = TestResult.objects.filter(user=patient.profile.patientprofile)
            return render(request, 'Users/Staff/Doctor/patient_medical_profile.html',
                          {'user': active_user, 'patient': patient, 'insurance': insurance,
                           'prescriptions': prescription, 'conditions': conditions, 'tests': tests,
                           'hospital_list': hospital_list})
        elif active_user.profile.role == 'Nurse':
            hospital_list = Hospital.objects.all()
            nurse_profile = get_object_or_404(NurseProfile, profile=user_profile)
            patient = get_object_or_404(User, username=patient)
            insurance = get_object_or_404(InsurancePolicy, user=patient.profile.patientprofile)
            prescription = Prescription.objects.filter(user=patient.profile.patientprofile)
            conditions = Condition.objects.filter(user=patient.profile.patientprofile)
            tests = TestResult.objects.filter(user=patient.profile.patientprofile)
            return render(request, 'Users/Staff/Nurse/patient_medical_profile.html',
                          {'user': active_user, 'patient': patient, 'insurance': insurance,
                           'prescriptions': prescription, 'conditions': conditions, 'tests': tests,
                           'hospital_list': hospital_list})
        elif active_user.profile.role == 'Secretary':
            hospital_list = Hospital.objects.all()
            doctor_profile = get_object_or_404(SecretaryProfile, profile=user_profile)
            patient = get_object_or_404(User, username=patient)
            insurance = get_object_or_404(InsurancePolicy, user=patient.profile.patientprofile)
            prescription = Prescription.objects.filter(user=patient.profile.patientprofile)
            return render(request, 'Users/Staff/Secretary/patient_profile.html',
                          {'user': active_user, 'patient': patient, 'insurance': insurance,
                           'prescriptions': prescription, 'hospital_list': hospital_list})


def remove_patient(request, username, pk):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = get_object_or_404(User, username=username)
        active_profile = get_object_or_404(Profile, user=active_user)
        active_doctor = get_object_or_404(DoctorProfile, profile=active_profile)
        patient_list = active_doctor.patient_list
        patient = get_object_or_404(PatientProfile, pk=pk)
        patient_list.remove(patient)
        return redirect('user:profile', username=username)


def patient_search(request, username):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = get_object_or_404(User, username=username)
        hospital_list = Hospital.objects.all()
        error = False
        if active_user.profile.role == 'Doctor':
            if request.method == 'POST':
                search = request.POST.get('query')
                if search:
                    try:
                        result_user = User.objects.get(username=search)
                        return redirect('user:view_patient', username=username, patient=result_user)
                    except:
                        error = True
                        return render(request, 'Users/Staff/Doctor/patient_search.html',
                                      {'error': error, 'hospital_list': hospital_list})
                else:
                    error = True
            else:
                return render(request, 'Users/Staff/Doctor/patient_search.html',
                              {'error': error, 'hospital_list': hospital_list})
        elif active_user.profile.role == 'Nurse':
            patients = []
            for patient in active_user.profile.nurseprofile.patient_list.all():
                patients.append(patient)
            if request.method == 'POST':
                search = request.POST.get('query')
                print(search)
                return redirect('user:view_patient', username=username, patient=search)
            else:
                return render(request, 'Users/Staff/Nurse/patient_search.html',
                              {'error': error, 'hospital_list': hospital_list, 'patients': patients})
        elif active_user.profile.role == 'Secretary':
            if request.method == 'POST':
                search = request.POST.get('query')
                if search:
                    try:
                        result_user = User.objects.get(username=search)
                        return redirect('user:view_patient', username=username, patient=result_user)
                    except:
                        error = True
                        return render(request, 'Users/Staff/Secretary/patient_search.html',
                                      {'error': error, 'hospital_list': hospital_list})
                else:
                    error = True
            else:
                return render(request, 'Users/Staff/Secretary/patient_search.html',
                              {'error': error, 'hospital_list': hospital_list})
        else:
            return render(request, 'PermissionDenied.html')


def add_patient(request, username, pk):
    active_user = get_object_or_404(User, username=username)
    active_profile = get_object_or_404(Profile, user=active_user)
    active_doctor = get_object_or_404(DoctorProfile, profile=active_profile)
    patient_list = active_doctor.patient_list
    patient = get_object_or_404(PatientProfile, pk=pk)
    patient_list.add(patient)
    return redirect('user:view_patient', username=username, patient=patient)
