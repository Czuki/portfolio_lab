from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from in_good_hands.models import Donation, Institution


class LandingPageView(View):
    def get(self, request, *args, **kwargs):

        choice = request.GET.get('choice', '1')
        institutions = Institution.objects.filter(type=choice)

        context = {
            'choice': choice,
            'donation': Donation,
            'institutions': institutions,
        }

        return render(request, 'index.html', context)


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if all((email, password, )):
            user = authenticate(username=email, password=password)
            if user is not None:
                return redirect('/')
            else:
                pass
                #not logged in
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        message = ''
        errors = False

        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if all((name, surname, email, password, password2, )):
            if password == password2:
                try:
                    validate_email(email)
                    validate_password(password=password)

                    user = User.objects.create_user(
                        first_name=name,
                        last_name=surname,
                        username=email,
                        email=email,
                        password=password)

                    user.save()
                    return redirect('/login#login')

                except ValidationError:
                    message = 'Something went wrong'
                    errors = True

        context = {
            'message': message,
            'errors': errors
        }

        return render(request, 'register.html', context)
