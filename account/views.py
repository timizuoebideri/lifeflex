from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.urls import reverse
from django.contrib import messages

# Create your views here.
from dashboard.models import Invoice
from .forms import UserCreateForm, ProfileCreateForm, ProfileEditForm, UserChangePasswordForm
from .models import UserProfile


def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect(reverse('login'))
        else:
            return render(request, 'account/login.html', {'error': "Incorrect username or password"})
    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def register_view(request):
    form1 = UserCreateForm()
    form2 = ProfileCreateForm()
    args = {
        'form1': form1,
        'form2': form2,
    }
    if request.method == 'POST':
        form1 = UserCreateForm(request.POST)
        if form1.is_valid():
            user = form1.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            user1 = User.objects.get(username=request.POST['username'])
            userprofile = UserProfile.objects.get(user=user1)
            form2 = ProfileCreateForm(data=request.POST, instance=userprofile)
            if form2.is_valid():
                form2.save()

                # get the amount from the user registration page
                def get_amount(amount):
                    if amount == 'Bronze':
                        return 250
                    elif amount == 'Silver':
                        return 500
                    elif amount == 'Gold':
                        return 1000
                    else:
                        return 2000

                # create an invoice for the newly registered user
                Invoice.objects.create(
                    user=user1,
                    purpose=f"{request.POST['account_type']} membership fee",
                    amount=get_amount(request.POST['account_type'])
                ).save()

                return redirect(reverse('login'))
            else:
                User(username=request.POST['username']).delete()
                return render(request, 'account/register.html', args)
        else:
            return render(request, 'account/register.html', args)
    return render(request, 'account/register.html', args)


def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    form = ProfileEditForm(instance=profile)
    password_form =  UserChangePasswordForm(user=request.user)

    if request.method == 'GET':
        args = {
            'form': form,
            'password_form': password_form
        }
        return render(request, 'account/profile.html', args)
    else:
        if request.POST['type'] == 'edit-profile':
            form = ProfileEditForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Profile updated successfully'
                                     , extra_tags='ti-check green-bg')
                return redirect(reverse('profile'))
            else:
                return render(request, 'account/profile.html', {
                    'form': form, 'password_form': password_form
                })
        else:
            password_form = UserChangePasswordForm(data=request.POST, user=request.user)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user=request.user)
                messages.add_message(request, messages.SUCCESS, 'Password updated successfully'
                                     , extra_tags='ti-check green-bg')
                return redirect(reverse('profile'))
            else:
                return render(request, 'account/profile.html', {
                    'form': form, 'password_form': password_form
                })
