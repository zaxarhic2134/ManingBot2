from django import forms

from .models import Profile
from .models import ProfileSettings

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=(
            'external_id',
            'name',
        )
        widgets={
            'name':forms.TextInput,
        }
class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model=ProfileSettings
        fields=(
            'external',
            'api_key',
            'secret_key',
            'subaccount_email',
            'pool_username',
        )
        widgets={
            'api_key':forms.TextInput,
            'secret_key': forms.TextInput,
            'subaccount_email': forms.TextInput,
            'pool_username': forms.TextInput,
        }