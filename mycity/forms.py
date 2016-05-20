from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from mysite.authuser.models import MyUser
from .models import *


class ProfileForm(forms.ModelForm):
    post_types = forms.MultipleChoiceField(
                label=_('Tipos de postagens'),
                widget=forms.CheckboxSelectMultiple(),
                choices=POST_TYPES
                )
    class Meta:
        model = UserProfile
        fields = ['img_usr', 'first_name', 'last_name', 'occupation',\
                'date_of_birth', 'country', 'state', 'city', 'post_types']
        exclude = ['validation_key', 'key_expires']
        labels = {
            'img_usr':_('Imagem do perfil'), 'first_name':_('Nome'),\
            'last_name':_('Sobrenome'), 'occupation':_('Ocupação'),\
            'date_of_birth':_('Data de nascimento'), 'country':_('País'),\
            'state':_('Estado'), 'city':_('Cidade'),
        }
        widgets = {
            'img_usr': forms.FileInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs) 

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.widgets.TextInput,
                        label="E-mail", max_length=254)
    password = forms.CharField(widget=forms.widgets.PasswordInput,
                        label="Senha")
    remember_me = forms.BooleanField(required=False, label="Lembrar")

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'remember_me']


class SignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.widgets.TextInput,
                        label="E-mail", max_length=254)
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação da senha',
                        widget=forms.PasswordInput)
    
    class Meta:
        model = MyUser
        fields = ['email']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SolicChangePassword(forms.Form):
    email = forms.EmailField(widget=forms.widgets.TextInput,
                        label="E-mail", max_length=254)


class ChangePasswordForm(forms.ModelForm):
    password1 = forms.CharField(label='Nova senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação da nova senha',
                        widget=forms.PasswordInput)
    
    class Meta:
        model = MyUser
        fields = []

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ChangePasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    