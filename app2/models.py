from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

ROLE_CHOICES = (
    (1, 'SuperAdmin'),
    (2, 'Admin'),
    (3, 'Sub-admin'),
    (4, 'User'),
)

class UserManager(BaseUserManager):
    def create_user(self, username, email, role_id, password=None):
        if not email:
            raise ValueError("Email is required")
        user = self.model(username=username, email=self.normalize_email(email), role_id=role_id)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        return self.create_user(username, email, role_id=1, password=password)

class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role_id = models.IntegerField(choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role_id']
    objects = UserManager()

    def __str__(self):
        return self.username

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    role = models.ForeignKey(User, on_delete=models.CASCADE, related_name='department_user')  # Connected to registered user

    def __str__(self):
        return f"{self.department_name} - {self.post}"
    
# app2/models.py
from django.core.validators import RegexValidator
class Master(models.Model):
    employee_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    contact = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Contact number must be exactly 10 digits.'
            )
        ]
           )

    address = models.TextField()
    joining_date = models.DateField()
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)

    def __str__(self):
        return self.full_name





from django.utils import timezone

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Present')

    def __str__(self):
        return f"{self.user.username} - {self.date}"



 # Adjust import as per your setup

from django.db import models
from app2.models import User

class AttendanceLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    event = models.CharField(max_length=20, default="Repeat")

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.time}"


