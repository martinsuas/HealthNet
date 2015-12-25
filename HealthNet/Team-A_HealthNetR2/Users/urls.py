__author__ = 'Zach'
from django.conf.urls import patterns, url, include
from Users import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^(?P<username>\w+)/profile/$', views.profile, name='profile'),
    url(r'^home/$', views.home, name='home'),
    url(r'^(?P<username>\w+)/edit/$', views.profile_edit, name='edit'),

    url(r'^(?P<username>\w+)/contact/$', views.contact, name='contact'),
    url(r'^(?P<username>\w+)/contact/create/$', views.create_contact, name='create_contact'),
    url(r'^(?P<username>\w+)/contact/(?P<pk>\d+)/edit/$', views.contact_edit, name='edit_contact'),
    url(r'^(?P<username>\w+)/contact/(?P<pk>\d+)/details/$', views.contact_details, name='detail_contact'),

    url(r'^(?P<username>\w+)/view/(?P<patient>\w+)', views.view_patient, name='view_patient'),
    url(r'^(?P<username>\w+)/remove/(?P<pk>\d+)', views.remove_patient, name='remove_patient'),
    url(r'^(?P<username>\w+)/add/(?P<pk>\d+)', views.add_patient, name='add_patient'),
    url(r'^(?P<username>\w+)/search/', views.patient_search, name='patient_search'),

    url(r'^', include('MedicalHistory.urls', namespace="med_his")),
    )

