from django import forms
from django.contrib.auth import get_user_model


class LoginForm(forms.ModelForm):
    telephone = forms.CharField(max_length=20)
    remember = forms.IntegerField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['password']