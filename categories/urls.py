from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from categories.views import CategoryDataView, CategoryView

urlpatterns = patterns(
    '',

    url(r'^$', TemplateView.as_view(template_name='categories/categories.html'), name='categories_page'),
    url(r'^(?P<pk>\d+)/$', CategoryView.as_view(), name='category_detail',),
    url(r'^get_data/$', CategoryDataView.as_view(), name='categories_all',),
)
