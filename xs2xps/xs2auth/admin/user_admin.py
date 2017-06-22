from __future__ import absolute_import

from django.contrib import admin

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from ..models import UserWithEmail

# Register your models here.

class UserWithEmailAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'name', 'provider', 'provider_id', 'date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'name',  'password', 'provider', 'provider_id', 'active', )}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'name',  'password1', 'password2',)}),
    )
    search_fields = ('email',)
    ordering = ('email',)



admin.site.register(UserWithEmail, UserWithEmailAdmin)