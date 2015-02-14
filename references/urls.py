from django.conf.urls import patterns, include, url
from references import views

reference_patterns = patterns(
    '',
    url(r'^$', views.ReferenceDetailView.as_view(), name='reference_detail')
)

urlpatterns = patterns(
    '',
    url(r'^$', views.ReferencesListView.as_view(), name='reference_list'),
    url(r'^create/$', views.CreateReferenceView.as_view(), name='create_reference'),
    url(r'^(?P<pk>\d+)/', include(reference_patterns))
)
