__author__ = 'Martin'


from django.conf.urls import patterns, url, include
from Statistics import views

urlpatterns = patterns('',
   url(r'^index/$', views.index, name='index'),
   url(r'^logs/$', views.dates, name='logs'),
   url(r'^results/$', views.display_logs, name='results'),

   )