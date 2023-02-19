from allauth.account import app_settings
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    email = forms.EmailField(label='E-mail')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2',]


class CommonRegisterForm(SignupForm):
    username = forms.CharField(
        label=('Логин'),
        widget=forms.TextInput(attrs={"placeholder":('Логин'),}),
    )
    first_name = forms.CharField(
        label=("Имя"),
        widget=forms.TextInput(attrs={"placeholder":("Имя"),}),
    )
    last_name = forms.CharField(
        label=("Фамилия"),
        widget=forms.TextInput(attrs={"placeholder":("Фамилия"),}),
    )

    def save(self, request):
        user = super(CommonRegisterForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user



