from password_validator import PasswordValidator

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from django.http import HttpResponse

from .utils import token_generator

class SignUpView(View):
    def get(self, request):
        return render(request, 'authentication/signup.html')
    
    def post(self, request):
        MIN_USERNAME_LEN = 3
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        context = {
            'fieldValues': request.POST
        }

        if not (len(username) and len(email) and len(password)):
            messages.error(request, 'field(s) can not be left empty!')
            return render(request, 'authentication/signup.html', context=context)

        if len(username) <= MIN_USERNAME_LEN:
            messages.error(request, f'{MIN_USERNAME_LEN+1} or more characters required for username')
            return render(request, 'authentication/signup.html', context=context)
        if not username.isalnum():
            messages.error(request, 'Username should be alphanumeric only')
            return render(request, 'authentication/signup.html', context=context)
        
        schema = PasswordValidator()
        schema\
        .min(8)\
        .max(100)\
        .has().uppercase()\
        .has().lowercase()\
        .has().digits()\
        .has().no().spaces()\
        .has().symbols()\
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if schema.validate(password):
                    user = User.objects.create_user(username=username, email=email)
                    user.set_password(password)
                    user.is_active = False
                    user.save()

                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    domain = get_current_site(request).domain
                    
                    link = reverse('verify', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                    activation_url = 'http://'+ domain + link

                    SUBJECT = 'Grocer Activation Link'
                    BODY = f'Hi {username}\n. Please use this link {activation_url} to activate your account'
                    mail = EmailMessage(
                        SUBJECT,
                        BODY,
                        'abdulrahmanibrahim.ish@gmail.com',
                        [user.email],
                    )
                    mail.send(fail_silently=True)

                    messages.success(request, 'Account created. Check your email for verification!')

                else:
                    messages.error(request, 'Invalid Password!')
                    return render(request, 'authentication/signup.html', context=context)
            else:
                messages.error(request, f'{email} is taken!')
                return render(request, 'authentication/signup.html', context=context)
        else:
            messages.error(request, f'{username} is taken!')
            return render(request, 'authentication/signup.html', context=context)


        return render(request, 'authentication/signup.html', context=context)


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        pass


class VerificationView(View):
    def get(self, request, uidb64, token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
        
        if not token_generator.check_token(user, token):
            return HttpResponse('<h1>Activation Link Expired</h1>')
        
        if user.is_active:
            return redirect(reverse('login'))
        
        user.is_active = True
        user.save()

        messages.success(request, 'Account activated succesfully!')
        return redirect(reverse('login'))
