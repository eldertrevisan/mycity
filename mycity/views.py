from django.shortcuts import (
    render, redirect, get_object_or_404)
from django.contrib.auth import (
    logout as logout_user, login as login_user, authenticate)
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import (
    datetime, timedelta)
import hashlib, random
from django.utils import timezone
from mysite.authuser.models import MyUser
from .forms import *
from .models import *


@login_required(login_url='/login/')
def  index(request):
    title = "MyCity | Início"
    return render(request, 'mycity/index.html', {'title':title})

@login_required(login_url='/login/')
def profile(request):
    title = "MyCity | Perfil de usuário"
    pk = request.user.id
    user = UserProfile.objects.get(user=pk)
    if request.method == "POST":
        profileform = ProfileForm(request.POST, request.FILES, instance=user)
        if profileform.is_valid():
            post_types = dict(request.POST)['post_types']
            up = profileform.save(commit=False)
            for pt in post_types:
                ptu = PostTypeUser(
                    post_types=pt
                    )
                ptu.save()
                up.post_types.add(ptu)
                up.save()
            profileform.save_m2m()
            return redirect('/profile/')
    else:
        profileform = ProfileForm(instance=user)
    return render(request, 'mycity/profile.html', {
        'title':title, 'profileform':profileform})

def signup(request):
    title = "MyCity | Cadastro de usuário"
    if request.method == "POST":
        signupform = SignupForm(data=request.POST)
        if signupform.is_valid():
            signupform.save()
            email = signupform.cleaned_data['email']
            random_string = str(random.random()).encode('utf8')
            salt = hashlib.sha1(random_string).hexdigest()[:5]
            salted = (salt + email).encode('utf8')
            validation_key = hashlib.sha1(salted).hexdigest()
            key_expires = datetime.today() + timedelta(2)
            user = MyUser.objects.get(email=email)
            new_user = UserProfile(
                user = user,
                validation_key = validation_key,
                key_expires = key_expires,
                first_name = '',
                last_name = '',
                state = '',
                city = '',
                )
            new_user.save()
            #send email with activation key
            email_subject = "MyCity - Confirmação de cadastro"
            email_text = "Clique no link para ativar sua conta: http://10.0.0.230:8000/confirm/{:s}/".format(validation_key)
            email_html = """
             <table style="width:450px" border="0" cellspacing="0" cellpadding="0" align="center">
                <tr>
                    <th bgcolor="#008CBA" valign="middle" width="100" height="50">
                        MyCity - Confirmação de Cadastro
                    </th>
                </tr>
                <tr>
                    <td  valign="top" width="600" height="50">
                        Prezado usuário, estamos lhe enviando este e-mail para confirmação de 
                        cadastro. Este link irá expirar em um prazo de 48 horas!
                        <br>
                        <br>
                        Para ativar sua conta, clique 
                        <a href="http://10.0.0.230:8000/confirm/{:s}/" 
                        title="Confirmação" targe="_blank">aqui</a>
                        <br>
                        <br>
                        <h5>Obs.: Não responder a este e-mail</h5>
                     </td>
                 </tr>
              </table>""".format(validation_key)
            send_mail(email_subject, email_text, 'activation-code@mycity.com',
                    [email], fail_silently=False, html_message=email_html)
            return render(request, 'mycity/register_success.html', {})                        
    else:
        signupform = SignupForm()
    return render(request, 'mycity/signup.html', {'signupform':signupform, 'title':title})

def register_confirm(request, validation_key):
    title = "MyCity | Confirmação de ativação"
    if request.user.is_authenticated():
        return redirect('/')
    profile_user = get_object_or_404(UserProfile, validation_key=validation_key)
    if profile_user.key_expires < timezone.now():
        return render(request, 'mycity/confirm_expired.html', {})
    user = profile_user.user
    user.is_active = True
    user.save()
    return render(request, 'mycity/confirm.html', {'title':title})

def login(request):
    title = "MyCity | Login"
    msg = ""
    active = None
    if request.method == "POST":
        loginform = LoginForm(data=request.POST)
        if loginform.is_valid():
            user = authenticate(email=request.POST['email'],
             password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    if not request.POST.get('remember_me', None):
                        request.session.set_expiry(0)
                    login_user(request, user)
                    return redirect('/')
                else:
                    active = False
                    msg = "Este e-mail ainda não está ativado! Favor verificar sua caixa de e-mail."
            else:
                active = False
                msg = "E-mail ou senha incorreto."
    else:
        loginform = LoginForm
    return render(request, 'mycity/login.html', {
        'title':title, 'loginform':loginform, 'active':active, 'msg':msg})

def forgot_password(request):
    title = "MyCity | Esqueci a senha"
    msg = ""
    if request.method == "POST":
        forgotpwdform = SolicChangePassword(data=request.POST)
        if forgotpwdform.is_valid():
            email = forgotpwdform.cleaned_data['email']
            if MyUser.objects.filter(email=email):
                user = MyUser.objects.get(email=email)
                random_string = str(random.random()).encode('utf8')
                salt = hashlib.sha1(random_string).hexdigest()[:5]
                salted = (salt + str(email)).encode('utf8')
                validation_key = hashlib.sha1(salted).hexdigest()
                key_expires = datetime.today() + timedelta(1)
                User.objects.filter(user=user).update(
                    activation_key=validation_key,
                    key_expires=key_expires)
            
                #send email with activation key
                email_subject = "MyCity - Alteração de senha"
                email_text = "Clique no link para alterar sua senha: http://10.0.0.230:8000/changepwd/{:s}/".format(validation_key)
                email_html = """
                <table style="width:450px" border="0" cellspacing="0" cellpadding="0" align="center">
                    <tr>
                        <th bgcolor="#008CBA" valign="middle" width="100" height="50">
                            MyCity - Alteração de senha
                        </th>
                    </tr>
                    <tr>
                        <td  valign="top" width="600" height="50">
                            Prezado usuário, estamos lhe enviando este e-mail para alteração de sua senha. 
                            Este link irá expirar em um prazo de 24 horas!
                            <br>
                            <br>
                            Para alterar sua senha, clique 
                            <a href="http://10.0.0.230:8000/change_password/{:s}/" 
                            title="Alteração de senha" targe="_blank">aqui</a>
                            <br>
                            <br>
                            <h5>Obs.: Não responder a este e-mail</h5>
                        </td>
                    </tr>
                </table>""".format(validation_key)
                send_mail(email_subject, email_text, 'changepwd@mycity.com',
                        [email], fail_silently=False, html_message=email_html)
                return render(request, 'mycity/forgot_password_success.html', {
                    'title':"MyCity | Alteração de senha"})      
            else:
                msg = "Usuário inexistente!"            
    forgotpwdform = SolicChangePassword()
    return render(request, 'mycity/forgot_password.html', {
        'title':title, 'forgotpwdform':forgotpwdform, 'msg':msg})

def change_password(request, validation_key):
    title = "MyCity | Alteração de senha"
    if request.user.is_authenticated():
        return redirect('/')
    profile_user = get_object_or_404(UserProfile, validation_key=validation_key)
    if profile_user.key_expires < timezone.now():
        return render(request, 'mycity/changepwd_expired.html', {})
    if request.method == "POST":
        changepasswordform = ChangePasswordForm(data=request.POST)
        if changepasswordform.is_valid():
            password = request.POST['password2']
            user = profile_user.user
            user.set_password(password)
            user.save()
            return render(request, 'mycity/changepwd_confirm.html', {})
    changepasswordform = ChangePassword()
    return render(request, 'mycity/changepwd.html', {
        'title':title, 'changepasswordform':changepasswordform, 'validation_key':validation_key})

def logout(request):
    logout_user(request)
    return redirect('index')
    
#IMPLEMENTAR AS PÁGINAS DE ERRO NO FINAL DO PROJETO
def handler404(request):
    title = "MyCity | Página não encontrada"
    return render(request, 'mycity/404.html', {'title':title})
