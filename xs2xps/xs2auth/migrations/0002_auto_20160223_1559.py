# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xs2auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwithemail',
            name='email',
            field=models.EmailField(null=True, max_length=254, blank=True, unique=True, verbose_name=b'email', db_index=True),
        ),
    ]
