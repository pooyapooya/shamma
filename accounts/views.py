# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import UpdateView
from accounts.forms import UserForm, UserProfileForm, UserProfileEditForm
from accounts.models import UserProfile
from django.core.mail import send_mail
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib import messages
import hashlib, datetime, random


class UserLogin(TemplateView):
    template_name = 'accounts/accounts_login.html'

    def get_context_data(self, **kwargs):
        ret = super(UserLogin, self).get_context_data(**kwargs)
        ret['redirect_url'] = self.request.GET.get('next', '/')
        return ret

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
            else:
                messages.error(request, u'Your account is inactive')
                return render_to_response(self.template_name, {}, RequestContext(request))
        else:
            messages.error(request, u'Username or Password is wrong')
            return render_to_response(self.template_name, {}, RequestContext(request))


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, u'You have successfully logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)


class Register(TemplateView):
    registered = False

    def generate_key(self, email):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(salt + email).hexdigest()
        key_expires = timezone.now() + datetime.timedelta(2)
        return activation_key, key_expires

    def send_activation_email(self, activation_key, email, username):
        email_subject = 'Account confirmation'
        email_body = "Hey %s, thanks for signing up. To activate your account, click this link within 48hours http://127.0.0.1:8000/accounts/confirm/%s" % (
            username, activation_key)
        send_mail(email_subject, email_body, 'shamma@gmail.com',
                  [email], fail_silently=False)

    def process_valid_forms(self, profile_form, user_form):
        user = user_form.save()
        user.set_password(user.password)
        user.is_active = False
        user.save()
        username = user.username
        email = user.email
        activation_key, key_expires = self.generate_key(email)
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.activation_key = activation_key
        profile.key_expires = key_expires
        profile.save()
        self.send_activation_email(activation_key, email, username)

    def post(self, request):
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            self.process_valid_forms(profile_form, user_form)

        else:
            print user_form.errors, profile_form.errors
            return render_to_response(
                'accounts/register.html',
                {'user_form': user_form, 'profile_form': profile_form, 'registered': False},
                RequestContext(request))

        return render_to_response(
            'accounts/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': True},
            RequestContext(request))


    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        profile_form = UserProfileForm()
        return render_to_response(
            'accounts/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': False},
            RequestContext(request))


class RegisterConfirm(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            HttpResponseRedirect('/home')

        # check if there is UserProfile which matches the activation key (if not then display 404)
        user_profile = get_object_or_404(UserProfile, activation_key=kwargs['activation_key'])

        # check if the activation key has expired, if it has then render confirm_expired.html
        if user_profile.key_expires < timezone.now():
            messages.error(request, u'Link has expired')
            return HttpResponseRedirect('/', {})

        # if the key hasn't expired save user and set him as active and render some template to confirm activation
        user = user_profile.user
        user.is_active = True
        user.save()
        messages.info(request, u'Your account has activated')
        return HttpResponseRedirect('/')


class AccountsEdit(UpdateView):
    template_name = 'accounts/accounts_edit.html'
    model = UserProfile
    form_class = UserProfileEditForm
    changed_password = False

    def get_object(self, queryset=None):
        user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return user_profile

    def form_valid(self, form):
        if form.has_changed_password():
            self.changed_password = True
            messages.success(self.request, u'Your password has changed. Please log in again')
        else:
            messages.success(self.request, u'Your profile has updated')
        return super(AccountsEdit, self).form_valid(form)

    def get_success_url(self):
        if ( self.changed_password ):
            return '/'
        else:
            return reverse_lazy('accounts_edit')



