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

    def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name, {}, RequestContext(self.request))

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request, u'حساب کاربری شما غیرفعال می‌باشد.')
                return render_to_response(self.template_name, {}, RequestContext(request))
        else:
            messages.error(request, u'نام کاربری یا رمز عبور اشتباه می‌باشد.')
            return render_to_response(self.template_name, {}, RequestContext(request))


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, u'خروج شما موفقیت آمیز بود.')
        return super(LogoutView, self).get(request, *args, **kwargs)


class Register(TemplateView):
    registered = False

    def post(self, request):
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)

            user.is_active = False

            username = user.username
            email = user.email
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt + email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.activation_key = activation_key
            profile.key_expires = key_expires

            profile.save()

            registered = True

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within 48hours http://127.0.0.1:8000/accounts/confirm/%s" % (
                username, activation_key)

            send_mail(email_subject, email_body, 'shamma@gmail.com',
                      [email], fail_silently=False)

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
            messages.error(request, u'مدت اعتبار لینک به پایان رسیده است')
            return HttpResponseRedirect('/', {})

        #if the key hasn't expired save user and set him as active and render some template to confirm activation
        user = user_profile.user
        user.is_active = True
        user.save()
        messages.info(request, u'حساب کاربری شما فعال گردید')
        return HttpResponseRedirect('/')


class AccountsEdit(UpdateView):
    template_name = 'accounts/accounts_edit.html'
    model = UserProfile
    form_class = UserProfileEditForm
    changed_password = False

    def get_object(self, queryset=None):
        user_profile, created = UserProfile.objects.get_or_create(user=self.request.user);
        return user_profile

    def form_valid(self, form):
        if form.has_changed_password():
            self.changed_password = True
            messages.success(self.request, u'رمز عبور شما با موفقیت تغییر کرد. لطفا دوباره وارد شوید')
        else:
            messages.success(self.request, u'حساب کاربری شما با موفقیت به روزرسانی شد')
        return super(AccountsEdit, self).form_valid(form)

    def get_success_url(self):
        if ( self.changed_password ):
            return '/'
        else:
            return reverse_lazy('accounts_edit')



