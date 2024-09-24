# your_app/forms.py

from django.contrib.admin.forms import AdminAuthenticationForm
from django import forms

class CustomAdminAuthenticationForm(AdminAuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active or not user.is_staff:
            raise forms.ValidationError(
                "Siz admin panelga kira olmaysiz.",
                code='invalid_login',
            )
