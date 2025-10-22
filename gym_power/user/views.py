# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .models import Users
from .forms import UserEditForm

import io
from reportlab.pdfgen import canvas
from openpyxl import Workbook

# Modelos y serializadores
from user.models import Users
from user.serializers import UserSerializer
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

# Telegram service (usando requests)
from telegram_service import send_telegram_message, send_telegram_document
# notificaciones 
from django.contrib import messages
from django.utils.timezone import make_aware
from datetime import datetime



# --- API para listar usuarios ---
class UserListView(ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["username", "id", "email"] 


# --- Autenticación ---
def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            context['error'] = 'Credenciales inválidas. Intenta de nuevo.'

    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            name = request.POST['name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            chat_id = request.POST['chat_id']
            role = request.POST['roles']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 != password2:
                return render(request, 'signup.html', {'error': 'Las contraseñas no coinciden.'})

            if DjangoUser.objects.filter(username=username).exists():
                return render(request, 'signup.html', {'error': 'El nombre de usuario ya está en uso.'})

            if DjangoUser.objects.filter(email=email).exists():
                return render(request, 'signup.html', {'error': 'El correo electrónico ya está registrado.'})

            # Crear usuario de Django
            user = DjangoUser.objects.create_user(username=username, email=email, password=password1)
            user.first_name = name
            user.last_name = last_name
            user.save()

            # Crear perfil extendido
            perfil = Users.objects.create(
                username=username,
                password=password1,  # 
                email=email,
                chat_id=chat_id,
                first_name=name,
                last_name=last_name,
                role_id=role
            )

            # Notificación Telegram
            if chat_id:
                send_telegram_message(
                    chat_id,
                    f"👋 ¡Hola {name}!\n\n"
                    "Bienvenido a *GymPower* \n"
                    "Tu cuenta se ha creado con éxito.\n\n"
                    "Ya puedes iniciar sesión en la plataforma."
                )

            login(request, user)
            return redirect('login')

        except IntegrityError:
            return render(request, 'signup.html', {'error': 'Ya existe un usuario con ese nombre o correo.'})
        except Exception as e:
            return render(request, 'signup.html', {'error': f'Error durante el registro: {str(e)}'})

    return render(request, 'signup.html')

@login_required
def editar_perfil(request, user_id):
    usuario = get_object_or_404(Users, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = UserEditForm(instance=usuario)

    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required
def listar_usuarios(request):
    user = request.user 
    try:
        perfil = Users.objects.get(username=user.username)
        role_name = perfil.role.nombre if perfil.role else None
    except Users.DoesNotExist:
        role_name = None

    usuarios = Users.objects.all()

    return render(request, 'listar_usuarios.html', {
        'usuarios': usuarios,
        'role_name': role_name,
    })

@login_required
def eliminar_usuario(request, user_id):
    current_user = Users.objects.get(username=request.user.username)
    if current_user.role.nombre != "Administrador":
        messages.error(request, "No tienes permiso para eliminar usuarios.")
        return redirect('listar_usuarios')

    usuario = get_object_or_404(Users, id=user_id)
    usuario.delete()
    messages.success(request, f"El usuario {usuario.username} fue eliminado correctamente.")
    return redirect('listar_usuarios')
