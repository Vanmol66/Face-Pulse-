from django import forms
from .models import User,  Department, Master
from .models import ROLE_CHOICES


from .models import User

class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role_id = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label="Choose Role",
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role_id', 'password']



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'post']

class MasterForm(forms.ModelForm):
    class Meta:
        model = Master
        fields = ['full_name', 'father_name', 'contact', 'address', 'joining_date','photo']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }
        