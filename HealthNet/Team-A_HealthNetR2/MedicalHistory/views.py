from .models import Appointment, Prescription
from .forms import AppointmentModify, PrescriptionModify
from django.shortcuts import render
import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, HttpResponseRedirect, redirect
from datetime import date, datetime, timedelta
from django.core.urlresolvers import reverse
import calendar
from django.utils import timezone
from django.contrib.auth.models import User
from Hospital.models import Hospital
from MedicalHistory.models import Appointment, InsurancePolicy, Condition, TestResult
from Users.models import Profile, DoctorProfile, PatientProfile, NurseProfile, SecretaryProfile, AdminProfile
import logging
from django.db.models import Q

# Create your views here.

logger = logging.getLogger('general')
dlogger = logging.getLogger('debug')

################
# Appointments #
################

### MONTHS
cal_months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


def appointments(request, year=time.strftime("%Y"), month=time.strftime("%m"), change=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        hospital_list = Hospital.objects.all()
    """Listing of days in `month`."""
    year, month = int(year), int(month)

    if year:
        year = int(year)
    else:
        year = time.localtime()[0]

    # apply next / previous change
    if change in ("next", "prev"):
        now, month_span = date(year, month, 15), timedelta(days=31)
        if change == "next":
            mod = month_span
        elif change == "prev":
            mod = -month_span

        year, month = (now + mod).timetuple()[:2]

    # init variables
    cal = calendar.Calendar()
    month_days = cal.itermonthdays(year, month)
    year_now, month_now, day_now = time.localtime()[:3]
    lst = [[]]
    week = 0
    appointment_list = Appointment.objects.none()

    if request.user.profile.role == "Nurse":
        appointment_list = Appointment.objects.filter(appointment_date__range=[datetime.today() - timedelta(days=4), datetime.today() + timedelta(days=4)])
    elif request.user.profile.role == "Secretary" or "Admin":
        appointment_list = Appointment.objects.all()

    elif request.user.profile.role == "Doctor":
        appointment_list = Appointment.objects.filter(doctor=request.user.profile.doctorprofile)

    elif request.user.profile.role == "Patient":
        appointment_list = Appointment.objects.filter(user=request.user.profile.patientprofile)

    for day in month_days:
        appointments = current = False
        if day:
            appointments = appointment_list.filter(appointment_date__year=year, appointment_date__month=month,
                                                   appointment_date__day=day)
            if day == day_now and year == year_now and month == month_now:
                current = True

        lst[week].append((day, appointments, current))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1

    appointment_list = Appointment.objects.filter(user=request.user)

    return render_to_response("Medical_History/Appointments/month.html",
                              dict(year=year, month=month, user=request.user,
                                   month_days=lst, mname=cal_months[month - 1], appointment_list=appointment_list,
                                   hospital_list=hospital_list))


def day(request, year, month, day ):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        hospital_list = Hospital.objects.all()
        day_date = (cal_months[int(month) - 1] + ' ' + day + ' ' + year)
        appointments = []
        if request.user.profile.role == "Admin" or "Secretary":
            appointments = Appointment.objects.filter(appointment_date__year=year,
                                                      appointment_date__month=month, appointment_date__day=day, )

        elif request.user.profile.role == "Nurse":
            appointments = Appointment.objects.filter(appointment_date__year=year,
                                                      appointment_date__range=[datetime.today() - timedelta(days=4), datetime.today() + timedelta(days=4)],
                                                      appointment_date__month=month, appointment_date__day=day,)

        elif request.user.profile.role == "Doctor":
            appointments = Appointment.objects.filter(doctor=request.user.profile.doctorprofile, appointment_date__year=year,
                                                      appointment_date__month=month, appointment_date__day=day,)

        elif request.user.profile.role == "Patient":
            appointments = Appointment.objects.filter(user=request.user.profile.patientprofile, appointment_date__year=year,
                                                      appointment_date__month=month, appointment_date__day=day,)
        if appointments:
            day_date = appointments[0].appointment_date
        return render(request, 'Medical_History/Appointments/day.html',
                      {'date': day_date, 'appointments': appointments, 'hospital_list': hospital_list})




# def appointment_add(request):
#     if not request.user.is_authenticated():
#         return HttpResponseRedirect(reverse('user:login'))
#     else:
#         if request.method == "POST":
#             form = AppointmentModify(request.POST)
#             if form.is_valid():
#                 appointment = form.save(commit=False)
#                 appointment_list = Appointment.objects.filter((Q(doctor=appointment.doctor)| Q(user=appointment.user)),
#                 appointment_date=appointment.appointment_date, appointment_time=appointment.appointment_time)
#                 dlogger.info(str(appointment_list))
#                 for app in appointment_list:
#                     dlogger.info(str(app))
#
#                 if appointment_list.count():
#                     logger.info(str(request.user) + " tried to create appointment, but failed.")
#                     return appointment_detail(request, -1)
#
#                 else:
#                     appointment.date_created = datetime.now()
#                     logger.info(str(request.user) + " created appointment: \"" + appointment.name + "\" with doctor "
#                                + str(appointment.doctor) + " and patient " + str(appointment.user) + " at " +
#                                 str(appointment.appointment_date) + ':' + str(appointment.appointment_time))
#
#                     appointment.save()
#                     return appointment_detail(request, appointment.pk)
#
#
#                 # return redirect('user:med_his:appointments_details', args={appointment.pk, username})
#
#         else:
#             form = AppointmentModify()
#
#         return render(request, 'Medical_History/Appointments/appointment_edit.html', {'form': form})


def appointment_add(request):
    warning = None
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        hospital_list = Hospital.objects.all()
        if request.method == "POST":
            user = request.POST.get('User')
            try:
                user = User.objects.get(username=user)
                user = Profile.objects.get(user=user)
                user = PatientProfile.objects.get(profile=user)
            except:
                Warning = "Patient doesn't exist. Please try again."
                return render(request, 'Medical_History/Appointments/appointment_edit.html',
                              {'warning': warning, 'hospital_list': hospital_list})
            doctor = request.POST.get('Doctor')
            try:
                doctor = User.objects.get(username=doctor)
                doctor = Profile.objects.get(user=doctor)
                doctor = DoctorProfile.objects.get(profile=doctor)
            except:
                Warning = "Doctor doesn't exist. Please try again."
                return render(request, 'Medical_History/Appointments/appointment_new.html',
                              {'warning': warning, 'hospital_list': hospital_list})
            name = request.POST.get('Name')
            description = request.POST.get('Description')
            date_created = timezone.now().date()
            appointment_date = request.POST.get('Date')
            appointment_time = request.POST.get('Time')
            appointment = Appointment.create(user, doctor, name, description, date_created, appointment_date,
                                             appointment_time)
            appointment.save()
            if (appointment.appointment_date == Appointment.objects.filter(doctor=appointment.doctor,
                                                                           appointment_date=appointment.appointment_date,
                                                                           appointment_time=appointment.appointment_time)[
                0].appointment_date) \
                    or (appointment.appointment_date == Appointment.objects.filter(doctor=appointment.doctor,
                                                                                   appointment_date=appointment.appointment_date,
                                                                                   appointment_time=appointment.appointment_time)[
                        0].appointment_date):
                logger.info(str(request.user) + " tried to create appointment, but failed.")
                return redirect('user:med_his:appointments_new')

            appointment_list = Appointment.objects.filter(Q(doctor=appointment.doctor) | Q(user=appointment.user))
            appointment_list = appointment_list.filter(appointment_date=appointment.appointment_date,
                                                       appointment_time=appointment.appointment_time)

            if not appointment_list or appointment.appointment_date == appointment_list[0].appointment_date:
                logger.info(str(request.user) + " tried to create appointment, but failed.")
                return redirect('user:med_his:appointments_new')

            else:
                appointment.date_created = datetime.now()
                logger.info(str(request.user) + " created appointment: \"" + appointment.name + "\" with doctor "
                            + str(appointment.doctor) + " and patient " + str(appointment.user) + " at " +
                            str(appointment.appointment_date) + ':' + str(appointment.appointment_time))

                appointment.save()
                return redirect('user:med_his:appointments')
                # return redirect('user:med_his:appointments_details', args={appointment.pk, username})
        return render(request, 'Medical_History/Appointments/appointment_edit.html',
                      {'warning': warning, 'hospital_list': hospital_list})


def appointment_remove(request, pk):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.delete()
        logger.info(str(request.user) + " removed appointment: \"" + appointment.name + "\" with doctor "
                    + str(appointment.doctor) + " and patient " + str(appointment.user) + " at " +
                    str(appointment.appointment_date) + ':' + str(appointment.appointment_time))
        return redirect('user:med_his:appointments')


def appointment_edit(request, pk):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        Warning = None
        appointment = get_object_or_404(Appointment, pk=pk)
        hospital_list = Hospital.objects.all()
        if request.method == 'POST':
            if request.method == "POST":
                user = request.POST.get('User')
                try:
                    user = User.objects.get(username=user)
                    user = Profile.objects.get(user=user)
                except:
                    Warning = "Patient doesn't exist. Please try again."
                    return render(request, 'Medical_History/Appointments/appointment_edit.html',
                                  {'item': appointment, 'warning': Warning, 'hospital_list': hospital_list})

                appointment.user = PatientProfile.objects.get(profile=user)
                doctor = request.POST.get('Doctor')
                try:
                    doctor = User.objects.get(username=doctor)
                    doctor = Profile.objects.get(user=doctor)

                except:
                    Warning = "Doctor doesn't exist. Please try again."
                    return render(request, 'Medical_History/Appointments/appointment_edit.html',
                                  {'item': appointment, 'warning': Warning, 'hospital_list': hospital_list})

                appointment.doctor = DoctorProfile.objects.get(profile=doctor)
                appointment.name = request.POST.get('Name')
                appointment.description = request.POST.get('Description')
                appointment.date_created = timezone.now().date()
                appointment.appointment_date = request.POST.get('Date')
                appointment.appointment_time = request.POST.get('Time')
                appointment.save()
                logger.info(str(request.user) + " modified appointment: \"" + appointment.name + "\" with doctor "
                            + str(appointment.doctor) + " and patient " + str(appointment.user) + " at " +
                            str(appointment.appointment_date) + ':' + str(appointment.appointment_time) +
                            " >> to: \"" + appointment.name + "\" with doctor "
                            + str(appointment.doctor) + " and patient " + str(appointment.user) + " at " +
                            str(appointment.appointment_date) + ':' + str(appointment.appointment_time))
                return redirect('user:med_his:appointments')
                # return redirect(reverse('user:med_his:appointment_detail', args={appointment.pk, username}))

        else:
            form = AppointmentModify(instance=appointment)

        return render(request, 'Medical_History/Appointments/appointment_edit.html',
                      {'item': appointment, 'warning': Warning, 'hospital_list': hospital_list})

#################
# Prescriptions #
#################

def prescriptions(request, username):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = request.user
        hospital_list = Hospital.objects.all()
        if active_user.profile.role == "Patient":
            active_user = active_user.profile.patientprofile
            prescription_list = Prescription.objects.filter(user=active_user)
            return render(request, 'Medical_History/Prescriptions/Patient/prescriptions.html',
                          {'prescription_list': prescription_list})

        elif active_user.profile.role == 'Doctor':
            active_user = active_user.profile.doctorprofile
            patient_list = active_user.patient_list.all()
            prescription_list = Prescription.objects.filter(doctor=active_user)
            prescription_list = prescription_list.order_by('user')
            return render(request, 'Medical_History/Prescriptions/Doctor/patients_prescriptions.html',
                          {'prescription_list': prescription_list, 'hospital_list': hospital_list})

        elif active_user.profile.role == 'Nurse':
            active_user = active_user.profile.nurseprofile
            patient_list = active_user.patient_list.all()
            prescription_list = Prescription.objects.filter(user=patient_list)
            prescription_list = prescription_list.order_by('user')
            return render(request, 'Medical_History/Prescriptions/Staff/patients_prescriptions.html',
                          {'prescription_list': prescription_list, 'hospital_list': hospital_list})


def prescription_add(request, username):
    warning = None
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        hospital_list = Hospital.objects.all()
        active_user = get_object_or_404(User, username=username)
        if active_user.profile.role == 'Doctor':
            if request.method == "POST":
                user = request.POST.get('User')
                try:
                    user = User.objects.get(username=user)
                    user = Profile.objects.get(user=user)
                    user = PatientProfile.objects.get(profile=user)
                except:
                    Warning = "Patient doesn't exist. Please try again."
                    return render(request, 'Medical_History/Prescriptions/Doctor/prescription_new.html',
                                  {'warning': warning, 'hospital_list': hospital_list})
                doctor = request.user.profile.doctorprofile
                dosage = request.POST.get('Dosage')
                drug_name = request.POST.get('Name')
                refills = request.POST.get('Refills')
                direction = request.POST.get('Direction')
                date_prescribed = request.POST.get('Date')
                prescription = Prescription.create(user, doctor, drug_name, dosage, refills, direction, date_prescribed)
                prescription.save()
                logger.info(
                    str(request.user) + " created prescription " + str(prescription.drug_name) + " for patient " + str(
                        prescription.user) + ".")
                return redirect('user:med_his:prescriptions', username=username)
            return render(request, 'Medical_History/Prescriptions/Doctor/prescription_new.html',
                          {'warning': warning, 'hospital_list': hospital_list})


def prescription_edit(request, pk, username):
    warning = None
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        hospital_list = Hospital.objects.all()
        prescription = get_object_or_404(Prescription, pk=pk)
        if request.method == 'POST':
            user = request.POST.get('User')
            try:
                user = User.objects.get(username=user)
                user = Profile.objects.get(user=user)
                prescription.user = PatientProfile.objects.get(profile=user)
            except:
                Warning = "Patient doesn't exist. Please try again."
                return render(request, 'Medical_History/Prescriptions/Doctor/prescription_edit.html',
                              {'warning': warning, 'prescription': prescription, 'hospital_list': hospital_list})

            prescription.dosage = request.POST.get('Dosage')
            prescription.drug_name = request.POST.get('Name')
            prescription.refills = request.POST.get('Refills')
            prescription.direction = request.POST.get('Direction')
            prescription.date_prescribed = request.POST.get('Date')
            prescription.save()
            logger.info(str(request.user) + " updated prescription " + str(prescription.drug_name) + " for patient "
                        + str(prescription.user) + ".")
            return redirect('user:med_his:prescriptions', username=username)
        return render(request, 'Medical_History/Prescriptions/Doctor/prescription_edit.html',
                      {'warning': warning, 'prescription': prescription, 'hospital_list': hospital_list})


def prescription_remove(request, username, pk):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        prescription = get_object_or_404(Prescription, pk=pk)
        prescription.delete()
        logger.info(str(request.user) + " deleted prescription " + str(prescription.drug_name) + " for patient "
                    + str(prescription.user) + ".")
        return redirect('user:med_his:prescriptions', username=username)


def insurance(request, username):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = get_object_or_404(User, username=username)
        active_profile = active_user.profile
        active_patient = active_profile.patientprofile
        try:
            insurance = InsurancePolicy.objects.filter(user=active_patient)
            insurance = get_object_or_404(insurance)
        except:
            return HttpResponseRedirect(reverse('user:med_his:insurance_new', args={username}))
        return render(request, 'Medical_History/Insurance/Patient/insurance.html', {'insurance': insurance})


def insurance_new(request, username):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = get_object_or_404(User, username=username)
        active_profile = active_user.profile
        active_patient = active_profile.patientprofile
        if request.method == 'POST':
            user = active_patient
            company = request.POST.get('company')
            insurance_id = request.POST.get('ID')
            policy_number = request.POST.get('policy_number')
            policy = InsurancePolicy.create(user, company, insurance_id, policy_number)
            policy.save()
            logger.info(str(request.user) + " created insurance with " + str(company) + " for patient "
                        + str(user) + ".")
            return HttpResponseRedirect(reverse('user:med_his:insurance', args={username}))
        else:
            print(request.POST.get('company'))
            return render(request, 'Medical_History/Insurance/Patient/insurance_edit.html', {})


def insurance_edit(request, username):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = get_object_or_404(User, username=username)
        active_profile = active_user.profile
        active_patient = active_profile.patientprofile
        insurance = InsurancePolicy.objects.filter(user=active_patient)
        policy = get_object_or_404(insurance)

        if request.method == 'POST':
            policy.company = request.POST.get('company')
            policy.insurance_id = request.POST.get('ID')
            policy.policy_number = request.POST.get('policy_number')
            policy.save()
            logger.info(str(request.user) + " updated insurance with " + str(policy.company) + " for patient "
                        + str(policy.user) + ".")
            return redirect('user:med_his:insurance', username=username)
        else:
            print(request.POST.get('company'))
            return render(request, 'Medical_History/Insurance/Patient/insurance_edit.html', {'insurance': policy})


def conditions(request, username):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = get_object_or_404(User, username=username)
        active_profile = get_object_or_404(Profile, user=active_user)
        hospital_list = Hospital.objects.all()
        if active_profile.role == 'Patient':
            active_patient = get_object_or_404(PatientProfile, profile=active_profile)
            conditions = Condition.objects.filter(user=active_patient)
            return render(request, 'Medical_History/Conditions/Patient/conditions.html',
                          {'conditions': conditions, 'hospital_list': hospital_list})
        elif active_profile.role == "Doctor":
            active_doctor = get_object_or_404(DoctorProfile, profile=active_profile)
            conditions = []
            for patient in active_doctor.patient_list.all():
                temp = Condition.objects.filter(user=patient).all()
                if temp:
                    for item in temp:
                        conditions.append(item)
            return render(request, 'Medical_History/Conditions/Doctor/conditions.html',
                          {'conditions': conditions, 'hospital_list': hospital_list})
        elif active_profile.role == "Nurse":
            active_nurse = get_object_or_404(NurseProfile, profile=active_profile)
            conditions = []
            for patient in active_nurse.patient_list.all():
                temp = Condition.objects.filter(user=patient).all()
                if temp:
                    for item in temp:
                        conditions.append(item)
            return render(request, 'Medical_History/Conditions/Staff/conditions.html',
                          {'conditions': conditions, 'hospital_list': hospital_list})


def conditions_new(request, username):
    warning = None
    hospital_list = Hospital.objects.all()
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        if request.method == "POST":
            user = request.POST.get('User')
            try:
                user = User.objects.get(username=user)
                user = Profile.objects.get(user=user)
                user = PatientProfile.objects.get(profile=user)
            except:
                Warning = "Patient doesn't exist. Please try again."
                return render(request, 'Medical_History/Conditions/Doctor/condtion_new.html',
                              {'warning': warning, 'hospital_list': hospital_list})
            name = request.POST.get('Name')
            currently_afflicted = request.POST.get('Afflicted')
            date_diagnosed = request.POST.get('Diagnosed')
            if request.POST.get('Recovered') == '' and not currently_afflicted:
                date_recovered = request.POST.get('Recovered')
            else:
                date_recovered = None
            condition = Condition.create(user, name, currently_afflicted, date_recovered, date_diagnosed)
            condition.save()
            logger.info(str(request.user) + " created prescription " + str(condition.name) + " for patient "
                        + str(condition.user) + ".")
            return redirect('user:med_his:conditions', username=username)
        return render(request, 'Medical_History/Conditions/Doctor/condtion_new.html',
                      {'warning': warning, 'hospital_list': hospital_list})


def conditions_edit(request, pk, username):
    warning = None
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        hospital_list = Hospital.objects.all()
        condition = get_object_or_404(Condition, pk=pk)
        if request.method == 'POST':
            user = request.POST.get('User')
            try:
                user = User.objects.get(username=user)
                user = Profile.objects.get(user=user)
                condition.user = PatientProfile.objects.get(profile=user)
            except:
                Warning = "Patient doesn't exist. Please try again."
                return render(request, 'Medical_History/Prescriptions/Doctor/prescription_new.html',
                              {'warning': warning, 'condition': condition, 'hospital_list': hospital_list})
            condition.name = request.POST.get('Name')
            condition.currently_afflicted = request.POST.get('Afflicted')
            condition.date_diagnosed = request.POST.get('Diagnosed')
            if request.POST.get('Recovered') == '' and not condition.currently_afflicted:
                condition.date_recovered = request.POST.get('Recovered')
            else:
                condition.date_recovered = None
            condition.save()
            logger.info(str(request.user) + " updated condition " + str(condition.name) + " for patient "
                        + str(condition.user) + ".")
            return redirect('user:med_his:conditions', username=username)
        return render(request, 'Medical_History/Conditions/Doctor/condition_edit.html',
                      {'warning': warning, 'condition': condition, 'hospital_list': hospital_list})


def condition_remove(request, username, pk):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        condition = get_object_or_404(Condition, pk=pk)
        condition.delete()
        logger.info(str(request.user) + " deleted condition " + str(condition.drug_name) + " for patient "
                    + str(condition.user) + ".")
        return redirect('user:med_his:conditions', username=username)


def test_results(request, username):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = get_object_or_404(User, username=username)
        active_profile = get_object_or_404(Profile, user=active_user)
        if active_profile.role == "Patient":
            active_patient = get_object_or_404(PatientProfile, profile=active_profile)
            test_results = TestResult.objects.filter(user=active_patient)
            return render(request, 'Medical_History/Test Results/Patient/testResults.html',
                          {'test_results': test_results})
        elif active_profile.role == 'Doctor':
            hospital_list = Hospital.objects.all()
            active_doctor = get_object_or_404(DoctorProfile, profile=active_profile)
            test_results = TestResult.objects.filter(doctor=active_doctor)
            return render(request, 'Medical_History/Test Results/Doctor/test_results.html',
                          {'test_results': test_results, 'hospital_list': hospital_list})
        elif active_profile.role == 'Nurse':
            hospital_list = Hospital.objects.all()
            active_nurse = get_object_or_404(NurseProfile, profile=active_profile)
            test_results = []
            for users in active_nurse.patient_list.all():
                for item in TestResult.objects.filter(user=users):
                    test_results.append(item)
            return render(request, 'Medical_History/Test Results/Staff/test_results.html',
                          {'test_results': test_results, 'hospital_list': hospital_list})


def test_remove(request, username, pk):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = get_object_or_404(User, username=username)
        active_profile = get_object_or_404(Profile, user=active_user)
        if active_profile.role == 'Doctor':
            hospital_list = Hospital.objects.all()
            active_doctor = get_object_or_404(DoctorProfile, profile=active_profile)
            test = get_object_or_404(TestResult, pk=pk)
            test.delete()
            return redirect('user:med_his:tests', username=username)
        else:
            render(request, 'PermissionDenied.html')


def test_release_toggle(request, username, pk):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = get_object_or_404(User, username=username)
        active_profile = get_object_or_404(Profile, user=active_user)
        if active_profile.role == 'Doctor':
            test = get_object_or_404(TestResult, pk=pk)
            if test.released:
                test.released = False
            else:
                test.released = True
            test.save()
            return redirect('user:med_his:tests', username=username)
        else:
            render(request, 'PermissionDenied.html')


def test_edit(request, username, pk):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        active_user = get_object_or_404(User, username=username)
        active_profile = get_object_or_404(Profile, user=active_user)
        if active_profile.role == 'Doctor':
            active_doctor = get_object_or_404(DoctorProfile, profile=active_profile)
            hospital_list = Hospital.objects.all()
            test = get_object_or_404(TestResult, pk=pk)
            if request.method == 'POST':
                released = request.POST.get('Released')
                if released == None:
                    released = False
                test.released = released
                test.notes = request.POST.get('Notes')
                test.save()
                return redirect('user:med_his:tests', username=username)
            else:
                return render(request, 'Medical_History/Test Results/Doctor/test_edit.html',
                              {'test': test, 'hospital_list': hospital_list})
        else:
            render(request, 'PermissionDenied.html')


def test_create(request, username):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        warning = None
        active_user = get_object_or_404(User, username=username)
        active_profile = get_object_or_404(Profile, user=active_user)
        if active_profile.role == 'Doctor':
            active_doctor = get_object_or_404(DoctorProfile, profile=active_profile)
            hospital_list = Hospital.objects.all()
            if request.method == 'POST':
                user = request.POST.get('UserName')
                try:
                    user = User.objects.get(username=user)
                    user = Profile.objects.get(user=user)
                    user = PatientProfile.objects.get(profile=user)
                except:
                    warning = "User does not exist!"
                    return render(request, 'Medical_History/Test Results/Doctor/test_create.html',
                                  {'hospital_list': hospital_list, 'warning': warning})
                doctor = active_doctor
                test_name = request.POST.get('TestName')
                pub_date = request.POST.get('PubDate') + " " + request.POST.get('PubTime')
                released = request.POST.get('Released')
                if released == None:
                    released = False
                report = request.FILES.get('Report')
                notes = request.POST.get('Notes')
                test = TestResult.create(user, doctor, test_name, pub_date, released, report, notes)
                test.save()
                return redirect('user:med_his:tests', username=username)
            else:
                return render(request, 'Medical_History/Test Results/Doctor/test_create.html',
                              {'hospital_list': hospital_list, 'warning': warning})
        else:
            render(request, 'PermissionDenied.html')

def export(request, username):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        return render(request, 'Medical_History/Export/export.html')