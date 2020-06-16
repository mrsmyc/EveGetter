from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Account
from django import forms
from phonenumber_field.modelfields import PhoneNumberField



class CreateUserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('phone','password1','password2')

    def __init__(self, *args, **kwargs):
       super(CreateUserForm, self).__init__(*args, **kwargs)
       self.fields['phone'].widget.attrs['class'] = 'auth_login_input'
       self.fields['phone'].widget.attrs['placeholder'] = 'Введите номер телефона'
       self.fields['password1'].widget.attrs['class'] = 'auth_password_input'
       self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
       self.fields['password2'].widget.attrs['class'] = 'auth_password_input'
       self.fields['password2'].widget.attrs['placeholder'] = 'Введите пароль еще раз'
  

class PasswordChangeFormEdit(PasswordChangeForm):
    old_password = forms.CharField(label=('Старый пароль'),required=True,error_messages = {'invalid':("Неверный старый пароль")}, widget=forms.PasswordInput)
    new_password1 = forms.CharField(label=('Новый пароль'),required=True, widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=('Подтвердите пароль'),required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("old_password","new_password1", "new_password2",)

    def __init__(self, *args, **kwargs):
        super(PasswordChangeFormEdit, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'pass1'
        self.fields['new_password1'].widget.attrs['class'] = 'pass2'
        self.fields['new_password2'].widget.attrs['class'] = 'pass3'

        


class UserUpdateForm(forms.ModelForm):
    user_avatar = forms.ImageField(label=('Аватар'),required=False, error_messages = {'invalid':("Только фотографии")}, widget=forms.FileInput)
    
    class Meta:
        model = Account
        fields = ("email","first_name","second_name","birth_date",
        "sex","country","city","profile_status","user_avatar",)


    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget.attrs['id'] = 'id_event_date'
        self.fields['email'].widget.attrs['class'] = 'border_ch'
        self.fields['first_name'].widget.attrs['class'] = 'border_ch'
        self.fields['second_name'].widget.attrs['class'] = 'border_ch'
        self.fields['birth_date'].widget.attrs['class'] = 'border_ch'
        self.fields['sex'].widget.attrs['class'] = 'border_ch'
        self.fields['country'].widget.attrs['class'] = 'border_ch'
        #self.fields['country'].widget.attrs['id'] = 'country'
        self.fields['city'].widget.attrs['class'] = 'border_ch'
       # self.fields['city'].widget.attrs['id'] = 'city'
        self.fields['profile_status'].widget.attrs['class'] = 'border_ch'
        self.fields['city'].widget.attrs['class'] = 'border_ch'

