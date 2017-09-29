from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.logreg, name='logreg'),
    url(r'^logout/$', views.logout, name='logout'),
]
