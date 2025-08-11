from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        min_length=8,
        max_length=16,
    )
    password2 = forms.CharField(
        label='confirm_password',
        widget=forms.PasswordInput,
        min_length=8,
        max_length=16,
    )

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data
        password1 = cd.get('password1')
        password2 = cd.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeFrom(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change the password using <a href="../password/">this form</a>.')

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name',
                  'is_active', 'is_admin', 'last_login')


class UserRegisterForm(forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField(label='Full Name', max_length=100)
    phone = forms.CharField(max_length=11)
    password = forms.CharField(
        widget=forms.PasswordInput, min_length=8, max_length=16)
