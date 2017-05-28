from django import forms

from .models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['battlenet', 'iccup', 'shield_battery', 'race']

    def clean_battlenet(self):
        return self.cleaned_data['battlenet'] or None

    def clean_iccup(self):
        return self.cleaned_data['iccup'] or None

    def clean_shield_battery(self):
        return self.cleaned_data['shield_battery'] or None
