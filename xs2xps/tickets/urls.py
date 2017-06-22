import views
from django.conf.urls import  url


urlpatterns = [
    url(r'^tickets$', views.tickets, name='tickets'),
    url(r'^ratings$', views.ratings, name='ratings'),
    url(r'^apitickets$', views.apitickets, name='apitickets$'),
    url(r'^setmotion/(?P<value>[\w]+)$', views.set_motion_detected, name='motion'),
]
