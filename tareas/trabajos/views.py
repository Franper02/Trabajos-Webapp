from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Tpsterminados, Usuario, Tps

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        trabajos = Tpsterminados.objects.filter(status=True, user=request.user)
        return render(request, "usuario/index.html", {
            'trabajos': trabajos
        })
    else:
        return HttpResponseRedirect(reverse('acc:login'))


def login_view(request):
    # Muestra la pagina si es solicitada con un GET
    if request.method == "GET":
        return render(request, "usuario/login.html")

    # cuando un post es enviado
    else:
        # guarda los datos del usuario en variables
        username = request.POST["username"]
        password = request.POST["password"]

        # compara los datos enviados por el post con los que hay en la base de datos
        user = authenticate(request, username=username, password=password)

        # si los datos coinciden, logea al usuario y lo redirecciona al index
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("acc:index"))

        # sino los manda al login (agregar mensaje de error!!!)
        else:
            error = 'erraste wachin'
            return render(request, "usuario/login.html", {
                'mensaje': error
            })


def logout_view(request):
    # cierra la sesion
    logout(request)
    return HttpResponseRedirect(reverse('acc:login'))


def register_view(request):
    # guarda los datos enviados a traves del post en variables
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # checkea si la contraseña es igual a la confirmacion (agregar mensaje de error!!!)
        if password != confirmation:
            return render(request, "usuario/register.html")

        # va a intentar crear un nuevo usuario
        try:
            user = Usuario.objects.create_user(username, email, password)
            user.save()
            for tp in Tps.objects.all():
                Tpsterminados.objects.create(user=user, tps=tp)

        # si el nombre esta en uso tira un error (agregar mensaje de error!!)
        except IntegrityError:
            return render(request, "usuario/register.html")

        # si el usuario es registrado, lo logea
        login(request, user)
        return HttpResponseRedirect(reverse('acc:index'))

    else:
        return render(request, "usuario/register.html")
