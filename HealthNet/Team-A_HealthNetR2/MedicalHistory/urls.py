__author__ = 'Martin'

from django.conf.urls import patterns, include, url
from MedicalHistory import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
   url(r'^appointments/$', views.appointments, name='appointments'),
   url(r'^appointments/new/$', views.appointment_add, name='appointment_new'),
   url(r'^appointments/(?P<pk>\d+)/edit/$', views.appointment_edit, name='appointment_edit'),
   url(r'^appointments/(?P<pk>\d+)/remove/$', views.appointment_remove, name='appointment_remove'),
   ##########
   #Calendar#
   ##########
   url(r'^appointments/month/(\d+)/(\d+)/(prev|next)/$', views.appointments, name="month"),
   url(r'^appointments/month/(\d+)/(\d+)/$', views.appointments, name="month"),
   url(r'^appointments/month$', views.appointments, name="month"),
   url(r'^appointments/day/(\d+)/(\d+)/(\d+)/$', views.day,  name="day"),

   url(r'^(?P<username>\w+)/prescriptions/$', views.prescriptions, name='prescriptions'),
   url(r'^(?P<username>\w+)/prescriptions/new/$', views.prescription_add, name='prescription_new'),
   url(r'^(?P<username>\w+)/prescriptions/(?P<pk>\d+)/edit/$', views.prescription_edit, name='prescription_edit'),
   url(r'^(?P<username>\w+)/prescriptions/(?P<pk>\d+)/remove/$', views.prescription_remove, name='prescription_remove'),

   url(r'^(?P<username>\w+)/insurance/$', views.insurance, name='insurance'),
   url(r'^(?P<username>\w+)/insurance/edit/$', views.insurance_edit, name='insurance_edit'),
   url(r'^(?P<username>\w+)/insurance/create/$', views.insurance_new, name='insurance_new'),

   url(r'^(?P<username>\w+)/conditions/$', views.conditions, name='conditions'),
   url(r'^(?P<username>\w+)/conditions/(?P<pk>\d+)/edit/$', views.conditions_edit, name='conditions_edit'),
   url(r'^(?P<username>\w+)/conditions/new/$', views.conditions_new, name='conditions_new'),

   url(r'^(?P<username>\w+)/tests/$', views.test_results, name='tests'),
   url(r'^(?P<username>\w+)/tests/(?P<pk>\d+)/remove/$', views.test_remove, name='test_remove'),
   url(r'^(?P<username>\w+)/tests/(?P<pk>\d+)/toggle/$', views.test_release_toggle, name='test_toggle'),
   url(r'^(?P<username>\w+)/tests/(?P<pk>\d+)/edit/$', views.test_edit, name='test_edit'),
   url(r'^(?P<username>\w+)/tests/new/$', views.test_create, name='test_new'),

   url(r'^(?P<username>\w+)/export/$', views.export, name='export'),
   )