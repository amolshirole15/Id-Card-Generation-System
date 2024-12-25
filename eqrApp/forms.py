from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from eqrApp import models


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[validate_password],
        label="Password",
        required=False  # Allow blank for profile update
    )
    verify_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
        required=False  # Allow blank for profile update
    )
    username = forms.CharField(max_length=150, label="Username", required=False)
    organization_code = forms.CharField(max_length=100, label="Organization Code")
    organization_name = forms.CharField(max_length=500, label="Organization Name")
    organization_type = forms.ChoiceField(choices=models.Profile.ORGANIZATION_TYPE_CHOICES)
    contact_number = forms.CharField(max_length=20, required=False)
    organization_address = forms.CharField(widget=forms.Textarea, required=False)
    contact_email = forms.EmailField(required=False)
    website = forms.URLField(required=False)
    template_id = forms.ChoiceField(
        choices=[('id_template_1', 'Template 1'), ('id_template_2', 'Template 2')],
        label="Select Template",
        required=False
    )
    profile_id = forms.UUIDField(widget=forms.HiddenInput, required=False)  # New hidden field for update check

    class Meta:
        model = User
        fields = [
            'username', 'password', 'verify_password', 'organization_code',
            'organization_name', 'organization_type', 'contact_number',
            'organization_address', 'contact_email', 'website', 'template_id'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        verify_password = cleaned_data.get("verify_password")
        organization_code = cleaned_data.get("organization_code")
        profile_id = cleaned_data.get("profile_id")

        # Check if passwords match for new profile creation
        if not profile_id and (password or verify_password) and password != verify_password:
            raise ValidationError("Passwords do not match.")
        
        # Check for unique organization_code unless updating existing profile
        if models.Profile.objects.filter(organization_code=organization_code).exclude(profile_id=profile_id).exists():
            raise ValidationError(f"Organization code '{organization_code}' is already taken.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        profile_id = self.cleaned_data.get("profile_id")
        
        if not profile_id:
            # Creating a new profile
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
                    website=self.cleaned_data['website'],
                    template_id=self.cleaned_data['template_id']
                )
        else:
            # Updating an existing profile
            if commit:
                user.save()
                profile = models.Profile.objects.get(profile_id=profile_id)
                profile.organization_code = self.cleaned_data['organization_code']
                profile.organization_name = self.cleaned_data['organization_name']
                profile.organization_type = self.cleaned_data['organization_type']
                profile.contact_number = self.cleaned_data['contact_number']
                profile.organization_address = self.cleaned_data['organization_address']
                profile.contact_email = self.cleaned_data['contact_email']
                profile.website = self.cleaned_data['website']
                profile.template_id = self.cleaned_data['template_id']
                profile.save()

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
    
    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)  # Get profile from kwargs
        print("profile data:", self.profile)
        super(SaveEmployee, self).__init__(*args, **kwargs)

    def clean_employee_code(self):
        employee_code = self.cleaned_data.get('employee_code')
        employee_id = self.instance.pk  # Check if it's an update

        # Ensure `employee_code` is unique within the current profile
        existing_employee = models.Employee.objects.filter(
            profile=self.profile, 
            employee_code=employee_code
        ).exclude(pk=employee_id)  # Exclude current employee if updating

        if existing_employee.exists():
            raise ValidationError(f"{employee_code} already exists.")
        
        return employee_code
