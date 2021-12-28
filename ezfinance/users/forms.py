from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class UserRegisterForm (UserCreationForm):
    email=forms.EmailField()
    first_name=forms.CharField()
    last_name=forms.CharField()

    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError("This email address is already in use. Please supply a different email address.")

    def clean_username(self):
        # Get the username
        username = self.cleaned_data.get('username')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(username=username)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return username

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError("This userid is already in use. Please supply a different userid.")

class UserUpdateForm (forms.ModelForm):
    email=forms.EmailField()
    first_name=forms.CharField(max_length=10)
    last_name=forms.CharField(max_length=20)

    class Meta:
        model=User
        fields=['first_name','last_name','email']



    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.

        try:
            match = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError("This email address is already in use. Please supply a different email address.")

class AccountUpdateForm (forms.ModelForm):
    mykad = forms.CharField()
    profesion = forms.CharField()
    phone = forms.CharField()
    address = forms.CharField()
    postcode = forms.CharField()
    city = forms.CharField()
    country = forms.CharField()

    class Meta:
        model = Account
        fields=['mykad','profesion','phone','address','postcode','city','country','image']

    def clean(self):
        super(AccountUpdateForm, self).clean()
        phone = self.cleaned_data.get('phone')
        postcode = self.cleaned_data.get('postcode')

        if not phone.isdigit() and len(phone)<13:
            self._errors['phone'] = self.error_class([
                'Please enter a valid phone number'])

        if not postcode.isdigit() and len(postcode)<6:
            self._errors['postcode'] = self.error_class([
                'Please enter a valid postcode'])

        return self.cleaned_data

