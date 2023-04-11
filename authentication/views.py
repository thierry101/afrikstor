from django.http import JsonResponse
from django.shortcuts import redirect, render
from authentication.models import User
from django.contrib.auth import authenticate, login, logout

from settingSite.models import ConfidentialityAndRule

# Create your views here.


def templateLogin(request):
    context = {
        'login': True
    }
    return render(request, 'authentication/login.html', context)


def loginUser(request):
    if request.is_ajax():
        data = request.POST
        email = data['email']
        password = data['password']
        errors = {}
        if email == '' or password == '':
            errors['credential'] = "Veuillez entrer vos identifiants"
        else:
            try:
                use = User.objects.filter(email=email)
                if use.exists():
                    user = authenticate(email=email, password=password)
                    if user is not None and user.check_password(password) and user.statut:
                        login(request, user)
                    else:
                        errors['credential'] = 'Identifiants invalides'
                else:
                    errors['credential'] = 'Identifiants invalides'
            except User.DoesNotExist():
                pass
        if len(errors) == 0:
            return JsonResponse('success', safe=False, status=200)
        else:
            return JsonResponse(errors, safe=False, status=400)


def logoutUser(request):
    logout(request)
    return redirect('home:homeIndex')


def confiDataTempl(request):
    dataConfi = ConfidentialityAndRule.objects.all().first()
    context = {
        'dataConfi': dataConfi
    }
    return render(request, 'authentication/dataconfi.html', context)


def rulerBuyer(request):
    dataConfi = ConfidentialityAndRule.objects.all().first()
    context = {
        'dataConfi': dataConfi
    }
    return render(request, 'authentication/tempBuyer.html', context)
