# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView
import views

urlpatterns = [
    url(r'^', include('xs2xps.xs2auth.urls')),
    url(r'^', include('xs2xps.tickets.urls')),
    url(r'^', include('favicon.urls')),
    url(r'^$', RedirectView.as_view(url='/admin')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^models', views.get_models),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#APP_URLS_HERE YOU CAN MOVE THEM TO THE TOP

