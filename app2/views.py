# app2/views.py
from django.http import HttpResponseForbidden
from .forms import RegisterUserForm, DepartmentForm, MasterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.views.decorators.csrf import csrf_protect

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'main.html', {'error': 'Invalid credentials'})

    return render(request, 'main.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'username': request.user.username,
        'role': request.user.role_id
    })

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

from .models import ROLE_CHOICES

from django.db import transaction


@login_required
def register_user(request):
    if request.user.role_id == 1:
        allowed_roles = [2, 3, 4]
    elif request.user.role_id == 2:
        allowed_roles = [3, 4]
    elif request.user.role_id == 3:
        allowed_roles = [4]
    else:
        return HttpResponseForbidden("Permission denied.")

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            request.session['reg_username'] = form.cleaned_data['username']
            request.session['reg_email'] = form.cleaned_data['email']
            request.session['reg_role_id'] = form.cleaned_data['role_id']
            request.session['reg_password'] = form.cleaned_data['password']

            return redirect('create_department')
    else:
        form = RegisterUserForm()

    return render(request, 'register.html', {
        'form': form,
        'allowed_roles': [(r, dict(ROLE_CHOICES).get(r)) for r in allowed_roles]
    })


@login_required
def view_users(request):
    if request.user.role_id in [1, 2, 3]:  # All except user
        users = User.objects.all()
        return render(request, 'view_users.html', {'users': users})
    return HttpResponseForbidden("You do not have permission.")

@login_required
def update_user(request, user_id):
    if request.user.role_id not in [1, 2]:
        return HttpResponseForbidden("You do not have permission.")
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.role_id = request.POST['role_id']
        user.save()
        return redirect('view_users')
    return render(request, 'update_user.html', {'user': user})

@login_required
def delete_user(request, user_id):
    if request.user.role_id not in [1, 2]:
        return HttpResponseForbidden("You do not have permission.")
    User.objects.get(id=user_id).delete()
    return redirect('view_users')

@login_required
def create_department(request):
    if not all(k in request.session for k in ['reg_username', 'reg_email', 'reg_password', 'reg_role_id']):
        return redirect('register_user')

    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department_data = form.cleaned_data
            request.session['department_name'] = department_data['department_name']
            request.session['post'] = department_data['post']
            return redirect('create_master')
    else:
        form = DepartmentForm()

    return render(request, 'create_data.html', {'form': form, 'title': 'Department Details'})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Department, Master
from .forms import MasterForm

from django.db import transaction

@login_required
@transaction.atomic
def create_master(request):
    if not all(k in request.session for k in ['reg_username', 'reg_email', 'reg_password', 'reg_role_id', 'department_name', 'post']):
        return redirect('register_user')

    if request.method == 'POST':
        form = MasterForm(request.POST, request.FILES)
        if form.is_valid():
            # Save all together in one transaction
            user = User.objects.create_user(
                username=request.session['reg_username'],
                email=request.session['reg_email'],
                role_id=request.session['reg_role_id'],
                password=request.session['reg_password']
            )

            department = Department.objects.create(
                department_name=request.session['department_name'],
                post=request.session['post'],
                role=user
            )

            master = form.save(commit=False)
            master.department = department
            master.save()

            # Clear session
            for key in list(request.session.keys()):
                if key.startswith('reg_') or key in ['department_name', 'post']:
                    del request.session[key]

            return redirect('dashboard')

    else:
        form = MasterForm()

    return render(request, 'create_data.html', {'form': form, 'title': 'Personal Details'})


@login_required
def view_departments(request):
    if request.user.role_id in [1, 2, 3]:
        departments = Department.objects.all()
        return render(request, 'view_departments.html', {'departments': departments})
    return HttpResponseForbidden("You do not have permission.")

@login_required
def update_department(request, dept_id):
    if request.user.role_id in [1, 2]:
        department = get_object_or_404(Department, department_id=dept_id)
        if request.method == 'POST':
            form = DepartmentForm(request.POST, instance=department)
            if form.is_valid():
                form.save()
                return redirect('view_departments')
        else:
            form = DepartmentForm(instance=department)
        return render(request, 'create_data.html', {'form': form, 'title': 'Update Department'})
    return HttpResponseForbidden("You do not have permission.")

@login_required
def delete_department(request, dept_id):
    if request.user.role_id in [1, 2]:
        department = get_object_or_404(Department, department_id=dept_id)
        department.delete()
        return redirect('view_departments')
    return HttpResponseForbidden("You do not have permission.")

@login_required
def view_masters(request):
    if request.user.role_id in [1, 2, 3]:
        masters = Master.objects.all()
        return render(request, 'view_masters.html', {'masters': masters})
    return HttpResponseForbidden("You do not have permission.")

@login_required
def update_master(request, master_id):
    if request.user.role_id in [1, 2]:
        master = get_object_or_404(Master, employee_id=master_id)
        if request.method == 'POST':
            form = MasterForm(request.POST, request.FILES, instance=master)  # ✅ include request.FILES

            if form.is_valid():
                form.save()
                return redirect('view_masters')
        else:
            form = MasterForm(instance=master)
        return render(request, 'create_data.html', {'form': form, 'title': 'Update Master'})
    return HttpResponseForbidden("You do not have permission.")

@login_required
def delete_master(request, master_id):
    if request.user.role_id in [1, 2]:
        master = get_object_or_404(Master, employee_id=master_id)
        master.delete()
        return redirect('view_masters')
    return HttpResponseForbidden("You do not have permission.")

@login_required
def view_personal_info(request):
    if request.user.role_id == 4:  # Only normal users
        try:
            department = Department.objects.get(role=request.user)
            master = Master.objects.get(department=department)
        except (Department.DoesNotExist, Master.DoesNotExist):
            return render(request, 'personal_info.html', {'error': 'Your information is incomplete.'})
        
        return render(request, 'personal_info.html', {
            'department': department,
            'master': master
        })

    return HttpResponseForbidden("You do not have permission.")

@login_required
def view_my_profile(request):
    user = request.user

    try:
        department = Department.objects.get(role=user)
        master = Master.objects.get(department=department)
    except (Department.DoesNotExist, Master.DoesNotExist):
        department = None
        master = None

    return render(request, 'my_profile.html', {
        'user': user,
        'department': department,
        'master': master,
    })

from django.shortcuts import render
from .models import AttendanceLog
from django.contrib.auth.decorators import login_required

@login_required
def view_attendance(request):
    user = request.user
    role = user.role_id

    if role in [1, 2, 3]:  # SuperAdmin, Admin, Sub-admin
        logs = AttendanceLog.objects.select_related('user').order_by('-date', '-time')
    else:
        logs = AttendanceLog.objects.filter(user=user).order_by('-date', '-time')

    return render(request, 'view_attendance.html', {
        'logs': logs
    })



