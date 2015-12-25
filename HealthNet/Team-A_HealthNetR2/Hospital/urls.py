__author__ = 'Zach'
from django.conf.urls import patterns, url, include
from Hospital import views

urlpatterns = patterns('',
                       url(r'^home/$', views.hospital, name='home'),
                       url(r'^(?P<username>\w+)/detail/(?P<pk>\d+)/$', views.hospital_details, name='detail'),
                       url(r'^(?P<username>\w+)/admit/(?P<pk>\d+)/$', views.admit_patient, name='admit'),
                       url(r'^(?P<username>\w+)/discharge/(?P<pk>\d+)/$', views.discharge_patient, name='discharge'),
                       url(r'^(?P<username>\w+)/transfer/(?P<pk>\d+)/$', views.transfer_patient, name='transfer'),
                       url(r'^(?P<username>\w+)/statistics/(?P<pk>\d+)/$', views.stats, name='stats'),
)