from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^destination/(?P<trip_id>\d+)/$', views.details, name='details'),
    url(r'^add/$', views.addtrip, name='add'),
    url(r'^join/(?P<trip_id>\d+)/$', views.join, name='join'),
]
