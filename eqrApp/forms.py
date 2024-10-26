from secrets import choice
from django import forms
from numpy import require
from eqrApp import models
import qrcode
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[validate_password],
        label="Password"
    )
    verify_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )
    organization_name = forms.CharField(max_length=500)
    user_type = forms.ChoiceField(choices=models.Profile.USER_TYPE_CHOICES)
    contact_number = forms.CharField(max_length=20, required=False)
    organization_address = forms.CharField(widget=forms.Textarea, required=False)
    contact_email = forms.EmailField(required=False)
    website = forms.URLField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'verify_password', 'organization_name', 'user_type']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        verify_password = cleaned_data.get("verify_password")

        if password and verify_password and password != verify_password:
            raise ValidationError("Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            models.Profile.objects.create(
                user=user,
                organization_name=self.cleaned_data['organization_name'],
                user_type=self.cleaned_data['user_type'],
                contact_number=self.cleaned_data['contact_number'],
                organization_address=self.cleaned_data['organization_address'],
                contact_email=self.cleaned_data['contact_email'],
                website=self.cleaned_data['website']
            )
        return user


class SaveEmployee(forms.ModelForm):
    employee_code = forms.CharField(max_length=250, label="Company ID")
    first_name = forms.CharField(max_length=250, label="First Name")
    middle_name = forms.CharField(max_length=250, label="Middle Name", required=False)
    last_name = forms.CharField(max_length=250, label="Last Name")
    dob = forms.DateField(label="Birthday")
    gender = forms.ChoiceField(choices=[("Male","Male"), ("Female","Female")], label="Gender")
    contact = forms.CharField(max_length=250, label="Contact #")
    email = forms.CharField(max_length=250, label="Email")
    address = forms.Textarea()
    department = forms.CharField(max_length=250, label="Department")
    position = forms.CharField(max_length=250, label="Position")
    avatar = forms.ImageField(label="Avatar")

    class Meta():
        model = models.Employee
        fields = ('employee_code',
                  'first_name',
                  'middle_name',
                  'last_name',
                  'dob',
                  'gender',
                  'contact',
                  'email',
                  'address',
                  'department',
                  'position',
                  'avatar', )

    def clean_employee_code(self):
        id = self.data['id'] if self.data['id'] != '' else 0
        employee_code = self.cleaned_data['employee_code']
        try:
            if id > 0:
                employee = models.Employee.exclude(id=id).get(employee_code = employee_code)
            else:
                employee = models.Employee.get(employee_code = employee_code)
        except:
            return employee_code
        return forms.ValidationError(f"{employee_code} already exists.")

