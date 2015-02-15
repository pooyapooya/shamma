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
    users = mommy.make_many(
        User,
        len(user_names),
        username=iter(user_names),
        first_name=iter(username.capitalize() for username in user_names),
        last_name=iter(username.capitalize() + 'an' for username in user_names),
        email=('%s@gmail.com' % username for username in user_names),
    )
    for user in users:
        user.set_password(user.username)
        user.save()

    topics = mommy.make_many(
        'categories.Topic',
        2,
        name=iter(['Agile', 'Scrum']),
    )
    topics[1].parent = topics[0]
    topics[1].save()

    mommy.make_one(
        'references.FilmReference',
        name='Daily Scrum Meeting',
        url='https://www.open.collab.net/nonav/community/swp/training/DailyScrumMeeting/DailyScrumMeeting.htm',
        description="""This module covers the second and most frequent meeting in the Scrum cycle.
         Subtopics include effective use of the taskboard, team self organization,
          how to incorporate varying skills on one team, the role of the ScrumMaster during Sprint Execution,
           pros and cons of involving the Product Owner each day, the three questions, and keeping the meeting short.
            The module briefly touches on the Agile engineering practices of Test Driven Development (TDD),
             pair programming, refactoring, and continuous integration."""
    )

    mommy.make_one(
        'references.ArticleReference',
        name='Product Owner Checklist',
        url='https://www.scrum.org/About/All-Articles/articleType/ArticleView/articleId/736/Product-Owner-Checklist',
        description="""This brief checklist helps you remember the most important things to become a good Product Owner.
         As the Product Owner you are responsible for maximizing the value of the product and the work
          of the Development Team."""
    )

    mommy.make_one(
        'references.ArticleReference',
        name='Scrum: Tactics for a Purpose',
        url='http://ullizee.wordpress.com/2013/05/14/scrum-tactics-for-a-purpose/',
        description="""The purpose of Scrum is to help people inspect & adapt,
         to provide transparency to the work being undertaken, to know reality to base decisions on,
          to adjust, to adapt, to change, to gain flexibility."""
    )

    mommy.make_one(
        'references.BookReference',
        name='Essential Scrum',
        url='http://www.innolution.com/essential-scrum/',
        description="""Introducing Essential Scrum:
         A Practical Guide to the Most Popular Agile Process by Kenneth S. Rubin."""
    )

    mommy.make_one(
        'references.SiteReference',
        name='Scrum Website',
        url='https://www.scrum.org/',
        description="""Scrum.org leads the evolution and maturity of Scrum to improve the profession of
         software development, up to the level of the enterprise agility of organizations."""
    )


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
