# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150209_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2015, 2, 10)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile_phone',
            field=models.CharField(blank=True, max_length=40, verbose_name='\u0634\u0645\u0627\u0631\u0647 \u0645\u0648\u0628\u0627\u06cc\u0644', validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Mobile phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", code=b'invalid_mobile_phone')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='national_code',
            field=models.CharField(blank=True, max_length=10, verbose_name='\u06a9\u062f \u0645\u0644\u06cc', validators=[django.core.validators.RegexValidator(regex=b'^\\d{10}$', message=b'National code must be 10 digits number', code=b'invalid_mational_code')]),
            preserve_default=True,
        ),
    ]
