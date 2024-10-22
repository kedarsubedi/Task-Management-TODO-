from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from account.forms import UserProfileForm
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth import views as auth_views
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from . utils import generate_otp, send_otp_email 

# Create your views here.

def register_page(request):
    template_name = 'account/register.html'
    form = UserProfileForm()
    if request.user.is_authenticated:
        return redirect('todoapp_view')
    else:
        if request.method=='POST':
            form = UserProfileForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                username = form.cleaned_data.get('username')
                if User.objects.filter(email=email).exists():
                    messages.warning(request, "Email Already Exist")
                    return render(request, template_name, {'form': form})
                if User.objects.filter(username=username).exists():
                    message.warning(request, "Username Already Exist")
                    return render(request, template_name, {'form': form})
                form.save()
                #send an email to the user when registered
                subject = 'Welcome to our site!'
                message = 'Dear\t' + username + ',\n\n'+'Thank you for registrating.\n\n'+'Best regards,\n'+'Nepal'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list)
                #sending mail ends here
                messages.success(request, 'Account was created for '+ username)
                return redirect('login_page')
            else:
                messages.info(request, 'Something went wrong!')
    context = {
        'form':form
    }
    return render(request, template_name, context)

def login_page(request):
    template_name = 'account/login.html'
    if request.user.is_authenticated:
        return redirect('todoapp_view')
    else:
        if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            userdata = authenticate(request, username=username, password=password)
            if userdata is not None:
                request.session['username'] = username
                request.session['password'] = password
                # generate the otp code
                request.session['otp'] = generate_otp()
                print(request.session['otp'])
                # send the OTP code to the user's email address
                send_otp_email(userdata.email, request.session['otp'])
                messages.success(request, "OTP has been sent in your mail")
                return redirect('verify_otp')
            else:
                messages.info(request, 'Username or Password is incorrect')
    return render(request, template_name)

def logoutUser(request):
    logout(request)
    messages.warning(request, 'Logged-out Successfully!')
    return redirect('login_page')

def reset_password(request):
    form=PasswordResetForm()
    if request.method=='POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, "Mail Sent Successfully to your email!")
        else:
            form = PasswordResetForm()
    context={
        'form':form
    }
    return render(request, 'account/password-reset.html', context)

# verify user using otp while logging in
def verify_otp(request):
    template_name = 'account/login_otp.html'
    if request.user.is_authenticated:
        return redirect('todoapp_view')
    else:
        if request.method == 'POST':
            otp = request.POST.get('otp')
            if otp == request.session.get('otp'):
                userdata = authenticate(request, username=request.session.get('username'), password=request.session.get('password'))
                if userdata is not None:
                    login(request, userdata)
                    messages.success(request, 'Logged in successfully')
                    return redirect('todoapp_view')
            else:
                messages.info(request, 'OTP is incorrect')
    # messages.warning(request, 'Something went wrong')
    return render(request, template_name)
    