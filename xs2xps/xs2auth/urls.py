import views
from django.conf.urls import  url

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^registerfb', views.login, name='registerfb'),
    url(r'^register', views.register, name='register'),
    url(r'^request_password_reset', views.request_password_reset, name='request_password_reset'),
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.reset_password_confirm,name='reset_password_confirm'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^weblogin$', views.weblogin, name='weblogin'),
]
