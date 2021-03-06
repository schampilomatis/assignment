# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWithEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(null=True, max_length=254, blank=True, unique=True, verbose_name=b'email')),
                ('name', models.CharField(max_length=255, null=True, verbose_name=b'name', blank=True)),
                ('lastname', models.CharField(max_length=255, null=True, verbose_name=b'lastname', blank=True)),
                ('active', models.BooleanField(default=True, verbose_name=b'active')),
                ('is_active', models.BooleanField(default=True, verbose_name=b'is_active')),
                ('is_staff', models.BooleanField(default=False, verbose_name=b'is_staff')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name=b'date_joined', null=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
    ]
