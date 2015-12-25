from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from Users.forms import UserForm, ProfileForm, PatientProfileForm
from django.db import models
from Users.models import Profile, PatientProfile, DoctorProfile, NurseProfile, AdminProfile
from MedicalHistory.models import Condition, TestResult, InsurancePolicy, Prescription
from Hospital.models import Hospital
from Hospital.forms import AdmitPatientQuery, DischargePatientQuery
import logging
# TransferPatient, StaffListModify

logger = logging.getLogger('general')

#   This will display a list of all the hospitals
def hospital(request):
    hospital_list = Hospital.objects.all()
    return render(request, 'Hospital/Doctor/hospital.html', {'hospital_list': hospital_list})


#   This is a details on a select Hospital
def hospital_details(request, username, pk):
    active_user = get_object_or_404(User, username=username)
    hospital_list = Hospital.objects.all()
    curr_hospital = get_object_or_404(Hospital, pk=pk)
    num_patients = len(curr_hospital.patient_list.all())
    num_doctors = len(curr_hospital.doctor_list.all())
    num_staff = len(curr_hospital.nurse_list.all()) + len(curr_hospital.secretary_list.all()) + len(
        curr_hospital.admin_list.all())
    if active_user.profile.role == 'Doctor':
        return render(
            request,
            'Hospital/Doctor/hospital_details.html',
            {'hospital_list': hospital_list,
             'num_patients': num_patients,
             'num_doctors': num_doctors,
             'num_staff': num_staff,
             'curr_hospital': curr_hospital}
        )
    if active_user.profile.role == 'Nurse':
        return render(
            request,
            'Hospital/Nurse/hospital_details.html',
            {'hospital_list': hospital_list,
             'num_patients': num_patients,
             'num_doctors': num_doctors,
             'num_staff': num_staff,
             'curr_hospital': curr_hospital}
        )
    elif active_user.profile.role == 'Secretary':
        return render(
            request,
            'Hospital/Secretary/hospital_details.html',
            {'hospital_list': hospital_list,
             'num_patients': num_patients,
             'num_doctors': num_doctors,
             'num_staff': num_staff,
             'curr_hospital': curr_hospital}
        )
    elif active_user.profile.role == 'Admin':
        return render(
            request,
            'Hospital/Admin/hospital_details.html',
            {'hospital_list': hospital_list,
             'num_patients': num_patients,
             'num_doctors': num_doctors,
             'num_staff': num_staff,
             'curr_hospital': curr_hospital}
        )


def admit_patient(request, username, pk):
    hospital_list = Hospital.objects.all()
    active_user = get_object_or_404(User, username=username)
    curr_hospital = get_object_or_404(Hospital, pk=pk)
    patient = None
    warning = None
    added = False
    if request.method == "POST":
        form = AdmitPatientQuery(request.POST)
        if form.is_valid():
            # Currently breaks if the username doesn't exist
            try:
                query = form.cleaned_data['patient']
                user = User.objects.filter(username=query)
                patient = Profile.objects.filter(user=user)
                patient = PatientProfile.objects.get(profile=patient)
                curr_hospital.patient_list.add(patient)
                added = True
                logger.info(str(request.user) + " admitted user " + str(user) + " to "
                            + str(curr_hospital) + ".")
            except:
                warning = "Patient doesn't exist. Please try again."
        else:
            print('form errors')
    else:
        form = AdmitPatientQuery()
    if active_user.profile.role == "Doctor":
        return render(request, 'Hospital/Doctor/admit.html', {
            'form': form,
            'added': added,
            'warning': warning,
            'patient': patient,
            'curr_hospital': curr_hospital,
            'hospital_list': hospital_list})
    elif active_user.profile.role == "Nurse":
        return render(request, 'Hospital/Nurse/admit.html', {
            'form': form,
            'added': added,
            'warning': warning,
            'patient': patient,
            'curr_hospital': curr_hospital,
            'hospital_list': hospital_list})
    elif active_user.profile.role == "Admin":
        return render(request, 'Hospital/Admin/admit.html', {
            'form': form,
            'added': added,
            'warning': warning,
            'patient': patient,
            'curr_hospital': curr_hospital,
            'hospital_list': hospital_list})
    else:
        return render(request, "PermissionDenied.html")


def discharge_patient(request, username, pk):
    active_user = get_object_or_404(User, username=username)
    hospital_list = Hospital.objects.all()
    curr_hospital = get_object_or_404(Hospital, pk=pk)
    patient = None
    warning = None
    removed = False
    if request.method == "POST":
        form = DischargePatientQuery(request.POST)
        if form.is_valid():
            # Currently breaks if the username doesn't exist
            try:
                query = form.cleaned_data['patient']
                user = User.objects.filter(username=query)
                patient = Profile.objects.filter(user=user)
                patient = PatientProfile.objects.get(profile=patient)
                curr_hospital.patient_list.remove(patient)
                removed = True
                logger.info(str(request.user) + " removed user " + str(user) + " from "
                            + str(curr_hospital) + ".")
            except:
                warning = "Patient doesn't exist. Please try again."
        else:
            print(form.errors)
    else:
        form = DischargePatientQuery()

    if active_user.profile.role == "Doctor":
        return render(request, 'Hospital/Doctor/discharge.html', {
            'form': form,
            'removed': removed,
            'warning': warning,
            'patient': patient,
            'curr_hospital': curr_hospital,
            'hospital_list': hospital_list})
    elif active_user.profile.role == "Admin":
        return render(request, 'Hospital/Admin/discharge.html', {
            'form': form,
            'added': removed,
            'warning': warning,
            'patient': patient,
            'curr_hospital': curr_hospital,
            'hospital_list': hospital_list})


#
def transfer_patient(request, username, pk):
    message = None
    curr_hospital = get_object_or_404(Hospital, pk=pk)
    hospital_list = Hospital.objects.all()
    active_user = get_object_or_404(User, username=username)
    active_profile = get_object_or_404(Profile, user=active_user)
    if active_profile.role == "Doctor":
        active_doctor = get_object_or_404(DoctorProfile, profile=active_profile)
        recieving_hospitals = []
        for hospital in Hospital.objects.all():
            if hospital != curr_hospital:
                for doctor in hospital.doctor_list.all():
                    if doctor == active_doctor:
                        recieving_hospitals.append(hospital)
        transferring_hospital = get_object_or_404(Hospital, pk=pk)
        if request.method == "POST":
            hospital = get_object_or_404(Hospital, name=request.POST.get('Hospital'))
            print(hospital)
            patient = request.POST.get('Patient')
            patient = get_object_or_404(User, username=patient)
            patient = get_object_or_404(Profile, user=patient)
            patient = get_object_or_404(PatientProfile, profile=patient)
            print(patient)
            hospital.patient_list.add(patient)
            hospital.save()
            curr_hospital.patient_list.remove(patient)
            message = "successfully transfered" + patient.profile.user.username + " to " + hospital.name
        return render(request, 'Hospital/Doctor/transfer.html', {
            'message': message,
            'recieving': recieving_hospitals,
            'transfering': transferring_hospital,
            'curr_hospital': curr_hospital,
            'hospital_list': hospital_list})
    if active_profile.role == "Admin":
        active_admin = get_object_or_404(AdminProfile, profile=active_profile)
        recieving_hospitals = []
        for hospital in Hospital.objects.all():
            if hospital != curr_hospital:
                for admin in hospital.admin_list.all():
                    if admin == active_admin:
                        recieving_hospitals.append(hospital)
        transferring_hospital = get_object_or_404(Hospital, pk=pk)
        if request.method == "POST":
            hospital = get_object_or_404(Hospital, name=request.POST.get('Hospital'))
            print(hospital)
            patient = request.POST.get('Patient')
            patient = get_object_or_404(User, username=patient)
            patient = get_object_or_404(Profile, user=patient)
            patient = get_object_or_404(PatientProfile, profile=patient)
            print(patient)
            hospital.patient_list.add(patient)
            hospital.save()
            curr_hospital.patient_list.remove(patient)
            message = "successfully transfered" + patient.profile.user.username + " to " + hospital.name
        return render(request, 'Hospital/Admin/transfer.html', {
            'message': message,
            'recieving': recieving_hospitals,
            'transfering': transferring_hospital,
            'curr_hospital': curr_hospital,
            'hospital_list': hospital_list})
    else:
        return render(request, 'PermissionDenied.html')


def stats(request, username, pk):
    curr_hospital = get_object_or_404(Hospital, pk=pk)
    hospital_list = Hospital.objects.all()
    active_user = get_object_or_404(User, username=username)
    active_profile = get_object_or_404(Profile, user=active_user)
    top_conditions = Condition.objects.all()
    top_conditions.order_by('name')
    pri_cond = []
    for item in top_conditions:
        priority = len(Condition.objects.filter(name=item.name))
        pri_cond.append([item.name, priority])
    pri_cond.sort()
    top_prescriptions = Prescription.objects.all()
    top_prescriptions.order_by('drug_name')
    pri_script = []
    for item in top_prescriptions:
        priority = len(Prescription.objects.filter(drug_name=item.drug_name))
        pri_script.append([item.drug_name, priority])
    pri_script.sort()
    top_insurance = InsurancePolicy.objects.all()
    pri_ins = []
    for item in top_insurance:
        priority = len(InsurancePolicy.objects.filter(company=item.company))
        pri_ins.append([item.company, priority])
    pri_ins.sort()

    top_conditions = pri_cond[0:10]
    top_prescriptions = pri_script[0:10]
    top_insurance = pri_ins[0:10]
    return render(request, 'Hospital/Admin/stats.html', {'curr_hospital': curr_hospital,
                                                         'hospital_list': hospital_list,
                                                         'top_conditions': top_conditions,
                                                         'top_prescriptions': top_prescriptions,
                                                         'top_insurance': top_insurance})