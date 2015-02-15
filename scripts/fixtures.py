# -*- coding: utf-8 -*-
import traceback
from django.conf import settings
from django.core.management import call_command
import os
from django.db import transaction
import itertools


@transaction.atomic()
def generate():
    from django.contrib.auth.models import User
    from model_mommy import mommy

    admin = User.objects.create_superuser(
        username='admin',
        password='admin',
        email='a@b.com',
    )

    user_names = ['ali', 'taghi', 'naghi']
    mommy.make_many(
        User,
        len(user_names),
        username=iter(user_names),
        password=iter(user_names),
        first_name=iter(username.capitalize for username in user_names),
        last_name=iter(username + 'an' for username in user_names),
        email=('%s@gmail.com' % username for username in user_names),
    )

    topics = mommy.make_many(
        'categories.Topic',
        2,
        name=iter(['Agile', 'Scrum']),
    )
    topics[1].parent = topics[0]
    topics[1].save()


def run():
    try:
        os.remove(settings.DATABASES['default']['NAME'])
    except OSError:
        pass
    call_command('migrate')
    generate()


if __name__ == '__main__':
    import django

    os.environ['DJANGO_SETTINGS_MODULE'] = 'shamma.settings'
    django.setup()
    run()
