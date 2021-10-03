from django.contrib import admin

from .forms import ProfileForm
from .forms import ProfileSettingsForm
from .models import Profile
from .models import ProfileSettings

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name',)
    form=ProfileForm

@admin.register(ProfileSettings)
class ProfileSettingsAdmin(admin.ModelAdmin):
    list_display = ('external', 'api_key', 'secret_key', 'subaccount_email', 'pool_username')
    form=ProfileSettingsForm
