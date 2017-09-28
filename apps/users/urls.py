from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.logreg),
    url(r'^logout/$', views.logout),
]
