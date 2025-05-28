from django.shortcuts import render
from django.views.generic import View

class SignUpView(View):
    def get(self, request):
        return render(request, 'authentication/signup.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
