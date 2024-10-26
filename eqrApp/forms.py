from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from eqrApp import models


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
    organization_code = forms.CharField(max_length=100, label="Organization Code")
    organization_name = forms.CharField(max_length=500, label="Organization Name")
    organization_type = forms.ChoiceField(choices=models.Profile.ORGANIZATION_TYPE_CHOICES)
    contact_number = forms.CharField(max_length=20, required=False)
    organization_address = forms.CharField(widget=forms.Textarea, required=False)
    contact_email = forms.EmailField(required=False)
    website = forms.URLField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'verify_password', 'organization_code', 'organization_name', 'organization_type']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        verify_password = cleaned_data.get("verify_password")
        organization_code = cleaned_data.get("organization_code")

        if password and verify_password and password != verify_password:
            raise ValidationError("Passwords do not match.")
        
        # Check for unique organization_code
        if models.Profile.objects.filter(organization_code=organization_code).exists():
            raise ValidationError(f"Organization code '{organization_code}' already exists.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            models.Profile.objects.create(
                user=user,
                organization_code=self.cleaned_data['organization_code'],
                organization_name=self.cleaned_data['organization_name'],
                organization_type=self.cleaned_data['organization_type'],
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
    dob = forms.DateField(label="Date of Birth", widget=forms.SelectDateWidget)
    gender = forms.ChoiceField(choices=[("Male", "Male"), ("Female", "Female")], label="Gender")
    contact = forms.CharField(max_length=250, label="Contact #")
    email = forms.EmailField(max_length=250, label="Email")
    address = forms.CharField(widget=forms.Textarea, label="Address", required=False)
    department = forms.CharField(max_length=250, label="Department", required=False)
    position = forms.CharField(max_length=250, label="Position", required=False)
    avatar = forms.ImageField(label="Avatar", required=False)

    class Meta:
        model = models.Employee
        fields = ('employee_code', 'first_name', 'middle_name', 'last_name', 'dob', 'gender', 'contact',
                  'email', 'address', 'department', 'position', 'avatar',)

    def clean_employee_code(self):
        employee_code = self.cleaned_data.get('employee_code')
        employee_id = self.instance.pk  # Check if it's an update

        # Check uniqueness for the employee_code
        existing_employee = models.Employee.objects.filter(employee_code=employee_code).exclude(pk=employee_id)
        if existing_employee.exists():
            raise ValidationError(f"{employee_code} already exists.")
        
        return employee_code
