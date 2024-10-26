import uuid
from distutils.command.upload import upload
from email.policy import default
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode
from PIL import Image
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    ORGANIZATION_TYPE_CHOICES = (
        ('college', 'College'),
        ('company', 'Company'),
    )

    profile_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_code = models.CharField(max_length=100, unique=True)
    organization_name = models.CharField(max_length=500)
    organization_type = models.CharField(max_length=50, choices=ORGANIZATION_TYPE_CHOICES)
    organization_address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization_name} ({self.get_organization_type_display()})"

    def save(self, *args, **kwargs):
        # Any custom logic can be added here
        super(Profile, self).save(*args, **kwargs)

    @property
    def employees(self):
        """Allows easy access to employees associated with this profile."""
        return self.user.employees.all()  # Access employees via related_name on Employee model

    
class Employee(models.Model):
    employee_code = models.CharField(max_length=100)
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=50, choices=(("Male","Male"), ("Female","Female")), default="Male")
    dob = models.DateField(max)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=250, blank=True)
    address = models.TextField(null=True, blank=True)
    department = models.TextField(null=True, blank=True)
    position = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to = "employee-avatars/",null=True, blank=True)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)
    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employees')

    def __str__(self):
        return str(f"{self.employee_code} - {self.first_name} "+ (f"{self.middle_name} {self.last_name}" if not self.middle_name == "" else f"{self.last_name}") )
    def name(self):
        return str(f"{self.first_name} "+ (f"{self.middle_name} {self.last_name}" if not self.middle_name == "" else f"{self.last_name}") )


    def save(self, *args, **kwargs):
        super(Employee, self).save(*args, **kwargs)
        print(self.avatar)
        imag = Image.open(self.avatar.path)
        if imag.width > 200 or imag.height> 200:
            output_size = (200, 200)
            imag.thumbnail(output_size)
            imag.save(self.avatar.path)
        
# @receiver(post_save, sender=Employee)
# def create_qr(sender, instance, **kwargs):
#     code = instance.employee_code
#     img = qrcode.make(code)
#     instance.qr_path = img
#     print(img)
#     # instance.save()

