from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
import references.urls
import accounts.urls
import categories.urls

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='homepage'),
    url(r'^references/', include(references.urls)),
    url(r'^accounts/', include(accounts.urls)),
    url(r'^categories/', include(categories.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
