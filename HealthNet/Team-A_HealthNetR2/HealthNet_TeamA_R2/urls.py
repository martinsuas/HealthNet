from django.conf.urls import patterns, include, url
from django.contrib import admin
from HealthNet_TeamA_R2 import views
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^user/', include('Users.urls', namespace="user")),
    url(r'^hospital/', include('Hospital.urls', namespace="hospital")),
    url(r'^statistics/', include('Statistics.urls', namespace="statistics")),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)