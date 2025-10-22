from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import Users


@login_required
def home(request):
    """Home con rol del usuario"""
    # Buscar el perfil extendido por username
    try:
        perfil = Users.objects.get(username=request.user.username)
        role_name = perfil.role.nombre if perfil.role else None
    except Users.DoesNotExist:
        role_name = None 

    return render(request, "home.html", {
        "role_name": role_name,
        "user": request.user
    })
