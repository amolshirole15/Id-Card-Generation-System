from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from eqrApp import models, forms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required



def context_data():
    context = {
        'page_name' : '',
        'page_title' : 'Chat Room',
        'system_name' : 'Employee ID with QR Code Generator',
        'topbar' : True,
        'footer' : True,
    }

    return context


# Create your views here.
def login_page(request):
    context = context_data()
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'login.html', context)

def register(request):
    context = context_data()
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'register'
    context['page_title'] = 'register'
    return render(request, 'register.html', context)

def register_user(request):
    resp = {"status": "failed", "msg": ""}

    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Create Profile for the new user
            profile = models.Profile(
                user=user,
                organization_code=form.cleaned_data.get('organization_code'),
                organization_name=form.cleaned_data.get('organization_name'),
                organization_type=form.cleaned_data.get('organization_type'),
                organization_address=form.cleaned_data.get('organization_address'),
                contact_number=form.cleaned_data.get('contact_number'),
                contact_email=form.cleaned_data.get('contact_email'),
                website=form.cleaned_data.get('website'),
                template_id=form.cleaned_data.get("template_id")
            )
            profile.save()  # Save the profile instance
            resp['status'] = 'success'
            resp['msg'] = 'User registered successfully'
        else:
            resp['msg'] = 'There were errors in the registration form'
            resp['errors'] = form.errors

    else:
        resp['msg'] = 'Invalid request method'

    return HttpResponse(json.dumps(resp), content_type='application/json')

def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
def home(request):
    context = context_data()
    context['page'] = 'home'
    context['page_title'] = 'Home'
    employee_list = request.user.profile.employees.all()
    context['employees'] = employee_list.count()
    context['isCompany'] = request.user.profile.organization_type == 'company'
    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')


@login_required
def employee_list(request):
    context =context_data()
    isCompany = request.user.profile.organization_type == 'company'
    context['page'] = 'employee_list'
    context['page_title'] = 'Employee List' if isCompany else 'Student List'
    context['employees'] = request.user.profile.employees.all()
    context['isCompany'] = isCompany

    return render(request, 'employee_list.html', context)

@login_required 
def manage_employee(request, pk=None):
    context =context_data()
    isStudent = request.user.profile.organization_type == 'college'
    context['isStudent'] = isStudent
    if pk is None:
        context['page'] = 'add_employee'
        context['page_title'] = 'Add New Student' if isStudent else 'Add New Employee'
        context['employee'] = {}
    else:
        context['page'] = 'edit_employee'
        context['page_title'] = 'Update Student' if isStudent else 'Update Employee'
        context['employee'] = models.Employee.objects.get(id=pk)

    return render(request, 'manage_employee.html', context)

@login_required
def save_employee(request):
    resp = {'status': 'failed', 'msg': ''}
    
    if request.method == 'POST':
        employee_id = request.POST.get('id', '')
        if employee_id:
            # Updating an existing employee
            employee = models.Employee.objects.get(id=employee_id)
            form = forms.SaveEmployee(request.POST, request.FILES, instance=employee, profile=request.user)
        else:
            # Creating a new employee
            form = forms.SaveEmployee(request.POST, request.FILES, profile=request.user)

        if form.is_valid():
            employee = form.save(commit=False)
            # Assign the logged-in user's profile to the employee
            employee.profile = request.user
            # Set default avatar if none is provided
            if not employee.avatar:
                employee.avatar = 'employee-avatars/avatar.jpg' if employee.gender == 'Male' else 'employee-avatars/avatar_2.png'
            employee.save()

            if not employee_id:
                messages.success(request, f"{employee.employee_code} has been added successfully.")
            else:
                messages.success(request, f"{employee.employee_code} has been updated successfully.")
                
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if resp['msg']:
                        resp['msg'] += "<br />"
                    resp['msg'] += f"[{field.label}] {error}"

    else:
        resp['msg'] = "No data has been sent into the request."

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_card(request, pk =None):
    if pk is None:
        return HttpResponse("Employee ID is Invalid")
    else:
        context = context_data()
        context['employee'] = models.Employee.objects.get(id=pk)
        context['isCompany'] = request.user.profile.organization_type == 'company'
        context['organization'] = request.user.profile
        id_template = request.user.profile.template_id + '.html' if request.user.profile.template_id else 'id_template_1.html'
        return render(request, id_template, context)

@login_required
def view_scanner(request):
    context = context_data()
    return render(request, 'scanner.html', context)


@login_required
def view_details(request, code = None):
    if code is None:
        return HttpResponse("Employee code is Invalid")
    else:
        context = context_data()
        context['employee'] = request.user.profile.employees.get(employee_code=code)
        context['isCompany'] = request.user.profile.organization_type == 'company'
        return render(request, 'view_details.html', context)

@login_required
def delete_employee(request, pk=None):
    resp = { 'status' : 'failed', 'msg' : '' }
    if pk is None:
        resp['msg'] = "No data has been sent into the request."
    else:
        try:
            models.Employee.objects.get(id=pk).delete()
            resp['status'] = 'success'
            messages.success(request, 'Employee has been deleted successfully.')
        except:
            resp['msg'] = "Employee has failed to delete."

    return HttpResponse(json.dumps(resp), content_type="application/json")
