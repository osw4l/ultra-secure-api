from django import forms
from .models import Account

class AccountAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Account
        fields = ['email', 'is_active', 'is_staff', 'is_superuser', 'password']

    def clean_password(self):
        return self.cleaned_data.get("password", self.initial.get("password"))

    def save(self, commit=True):
        account = super().save(commit=False)
        if self.cleaned_data["password"]:
            account.set_password(self.cleaned_data["password"])
        if commit:
            account.save()
            self.save_m2m()
        return account