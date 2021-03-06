from django.conf.urls import patterns, include, url
from accounts import views
from accounts.views import UserLogin, LogoutView, Register, RegisterConfirm

urlpatterns = patterns(
    '',
    url(r'^login/$', UserLogin.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^confirm/(?P<activation_key>\w+)/', RegisterConfirm.as_view(), name='confirm'),
    url(r'^edit/$', views.AccountsEdit.as_view(), name='accounts_edit'),
)
