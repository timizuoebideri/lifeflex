from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
import django_filters

from activities.models import AccountActivities
from .models import UserProfile


class UserCreateForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": 'Username', 'class': 'uk-input uk-border-rounded form-control'})
    )
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": 'Password', 'class': 'uk-input uk-border-rounded form-control'})
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": 'Password Confirmation', 'class': 'uk-input uk-border-rounded form-control'})
    )


class ProfileCreateForm(forms.ModelForm):
    select = [
        ('Bronze', 'Bronze'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
    ]
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": 'Full Name', 'class': 'uk-input uk-border-rounded form-control'})
        , required=False
    )
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"placeholder": 'Email', 'class': 'uk-input uk-border-rounded form-control'})
    )
    phone = forms.CharField(widget=forms.NumberInput(
        attrs={"placeholder": 'Phone Number', 'class': 'uk-input uk-border-rounded form-control'})
    )
    account_type = forms.CharField(widget=forms.Select(
        choices=select,
        attrs={"placeholder": 'Full Name', 'class': 'uk-input uk-border-rounded form-control'})
    )

    class Meta:
        fields = (
            'fullname', 'email', 'phone', 'account_type'
        )
        model = UserProfile


class ProfileEditForm(forms.ModelForm):
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": 'Full Name', 'class': 'uk-input uk-border-rounded form-control'})
        , required=False
    )
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"placeholder": 'Email', 'class': 'uk-input uk-border-rounded form-control'})
    )
    phone = forms.CharField(widget=forms.NumberInput(
        attrs={"placeholder": 'Phone Number', 'class': 'uk-input uk-border-rounded form-control'})
    )
    bank_name = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": 'Bank Name', 'class': 'uk-input uk-border-rounded form-control'}),
        required=False
    )
    bank_account_number = forms.CharField(widget=forms.NumberInput(
        attrs={"placeholder": 'Account Number', 'class': 'uk-input uk-border-rounded form-control'})
    )
    bitcoin_wallet = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": 'Bitcoin Wallet Address', 'class': 'uk-input uk-border-rounded form-control'}),
        required=False
    )

    class Meta:
        fields = ('fullname', 'email', 'phone', 'image', 'bank_name', 'bank_account_number', 'bitcoin_wallet')
        exclude = ['account_type']
        model = UserProfile


class UserChangePasswordForm(PasswordChangeForm):
    pass


class ActivityFilterForm(django_filters.FilterSet):
    choices = [
        ('account', 'Account'),
        ('invoice', 'Invoice'),
        ('withdrawal', 'Withdrawal'),
        ('deposit', 'Deposit'),
    ]
    type = django_filters.ChoiceFilter(
        field_name='type',
        choices=choices,
        label='Filter by',
    )

    class Meta:
        fields = ('type',)
        model = AccountActivities
