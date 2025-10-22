from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

# Vistas propias del proyecto
from user import views as user_views
from home import views as home_views
from notifications import views as notis_views
from clases import views as class_views

urlpatterns = [
    # 🔄 Redirección según autenticación
    path('', lambda request: redirect('home') if request.user.is_authenticated else redirect('login')),

    # ⚙️ Administración Django
    path('admin/', admin.site.urls),

    # 👥 Autenticación y usuarios
    path('signup/', user_views.signup_view, name='signup'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('editar/<int:user_id>/', user_views.editar_perfil, name='editar_usuario'),
    path('listar/', user_views.listar_usuarios, name='listar_usuarios'),
    path('eliminar/<int:user_id>/', user_views.eliminar_usuario, name='eliminar_usuario'),

    # 🏠 Página de inicio
    path('home/', home_views.home, name='home'),

    # 🔐 Recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),

    # 🏋️‍♂️ CRUD de clases (módulo gimnasio)
    path('clases/', class_views.listar_clases, name='listar_clases'),
    path('clases/crear/', class_views.crear_clase, name='crear_clase'),
    path('clases/editar/<int:clase_id>/', class_views.editar_clase, name='editar_clase'),
    path('clases/eliminar/<int:clase_id>/', class_views.eliminar_clase, name='eliminar_clase'),
    path('clases/inscribirse/<int:clase_id>/', class_views.inscribirse_clase, name='inscribirse_clase'),
    path('clases/ver/<int:clase_id>/', class_views.ver_clase, name='ver_clase'),


    # 📊 Reportes y notificaciones
    path("reporte/pdf/", notis_views.generar_pdf, name="generar_pdf"),
    path("reportes/", notis_views.reportes_view, name="reportes"),
    path("reportes/pdf/", notis_views.generar_pdf, name="export_pdf"),
    path("reportes/excel/", notis_views.generar_excel, name="export_excel"),
    path("reportes/telegram/", notis_views.enviar_reporte_telegram, name="send_report_telegram"),

    # 🔔 Envío de notificaciones
    path("enviar_notificacion/", notis_views.enviar_notificacion, name="enviar_notificacion"),
  # 🌐 API de usuarios
    path('api/v1/users/', user_views.UserListView.as_view(), name='api_users'),
]
