# HealthNet
Version 1.0; final project delivarable.

Admin account
   username admin
   password 1234


For local testing
In Windows
Have Python 3.2 and Django 1.6.5 installed.
Change the command prompt to the directory where this file is located.
After adding Python and PythonScripts directories to the PATH, write

python manage.py runserver

This will give you the address that will allow you to access the webapp in your
preferred browser.

Log-in using the username and password above.

All information is supplied in an SQL file for convenience. Fixtures to create this initial file have been supplied, in which case just delete the local db.sqlite3 file and run

python manage.py syncdb

Default users
Doctors -Mario -Luigi
Nurses -Peach -Daisy
Patients -DK -Bowser -Goomba -Yoshi


All existing username passwords are 1234.
Log-in is CASE SENSITIVE!

Documentation at Team-A-Doc folder

#######################
#    Tasks examples   #
#######################

Register Patient

1. Click Patient Registration.
2. Enter indicated information.
3. Click register.
4. Go back to homepage.
5. Click Administrator Log In
6. Click Patients
7. Click Add Patient
8. Choose User registered in step 3
9. Click save

PatientNurseDoctor Login

1. Click User Login
2. Enter information (like already include Patient 'Bowser' Password '1234')
3. Click Login

See appointments and prescriptions

1. Do to 'PatientNurseDoctor Login' task example.
2. Click appointments or prescriptions

Add appointmentsprescriptions

1. Click Administrator Login.
2. Enter an administrator user (or use default 'user123')
3. Click Appointments or Prescriptions
4. Click Add prescription or appointment
5. Select user owner (Patient) and enter information
6. Click save

Register NurseDoctor

1. Click Administrator Login.
2. Enter an administrator user (or use default 'user123')
3. Click Users
4. Click Add user
5. Input username and password
6. Click save
7. Go to admin homepage, click Doctors or Nurses
8. Click Add doctor or Add nurse
9  Link User from step 6 to assign role
10. Click save

Register Administrator

1. Click Administrator Login
2. Enter an administrator user
3. Click Users
4. Click Add user
5. Input username and password
6. Click save
7. After created, enter optional personal information if wanted
8. Click 'Staff' for BAdministrator or 'Superuser status' for another system administrator
9. Click save
