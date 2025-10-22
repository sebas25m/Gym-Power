from django.shortcuts import render
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

import io
from reportlab.pdfgen import canvas
from openpyxl import Workbook

# Modelos y serializadores
from user.models import Users

# Telegram service (usando requests)
from telegram_service import send_telegram_message, send_telegram_document
# notificaciones 
from django.contrib import messages



# --- Reportes PDF ---
@login_required
def generar_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "📋 Reporte de Usuarios del Gym")

    p.setFont("Helvetica", 10)
    y = 750
    for user in Users.objects.all():
        texto = f"{user.first_name} {user.last_name} | {user.email} | Rol: {user.role} | Estado: {user.estado} | Registrado: {user.fecha_registro.strftime('%Y-%m-%d')}"
        p.drawString(50, y, texto)
        y -= 20
        if y < 50:  
            p.showPage()
            y = 800

    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_usuarios.pdf"'
    return response


# --- Reportes Excel ---
@login_required
def generar_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Usuarios"

    ws.append(["Nombre", "Apellido", "Email", "Rol", "Estado", "Fecha Registro"])

    for user in Users.objects.all():
        ws.append([
            user.first_name,
            user.last_name,
            user.email,
            str(user.role) if user.role else "N/A",
            user.estado,
            user.fecha_registro.strftime("%Y-%m-%d") if user.fecha_registro else "N/A"
        ])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="reporte_usuarios.xlsx"'

    wb.save(response)
    return response


# --- Enviar reporte por Telegram ---
@login_required
@csrf_exempt
def enviar_reporte_telegram(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        file_type = request.POST.get("file_type", "pdf")

        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return HttpResponse("❌ Usuario no encontrado", status=404)

        if not user.chat_id:
            return HttpResponse(f"⚠️ Usuario {user.username} no tiene chat_id", status=400)

        try:
            chat_id_int = int(user.chat_id)
        except ValueError:
            return HttpResponse(f"❌ chat_id inválido para {user.username}", status=400)

        # Generar archivo en memoria
        buffer = io.BytesIO()
        if file_type == "pdf":
            p = canvas.Canvas(buffer)
            p.setFont("Helvetica-Bold", 16)
            p.drawString(200, 800, "📋 Reporte de Usuarios del Gym")
            p.setFont("Helvetica", 10)
            y = 750
            for u in Users.objects.all():
                texto = f"{u.first_name} {u.last_name} | {u.email} | Rol: {u.role} | Estado: {u.estado} | Registrado: {u.fecha_registro.strftime('%Y-%m-%d')}"
                p.drawString(50, y, texto)
                y -= 20
                if y < 50:
                    p.showPage()
                    y = 800
            p.save()
            buffer.seek(0)
            file_name = f"reporte_usuarios_{now().strftime('%Y%m%d')}.pdf"
        else:
            wb = Workbook()
            ws = wb.active
            ws.title = "Usuarios"
            ws.append(["Nombre", "Apellido", "Email", "Rol", "Estado", "Fecha Registro"])
            for u in Users.objects.all():
                ws.append([
                    u.first_name,
                    u.last_name,
                    u.email,
                    str(u.role) if u.role else "N/A",
                    u.estado,
                    u.fecha_registro.strftime("%Y-%m-%d") if u.fecha_registro else "N/A"
                ])
            wb.save(buffer)
            buffer.seek(0)
            file_name = f"reporte_usuarios_{now().strftime('%Y%m%d')}.xlsx"

        # Enviar mensaje
        mensaje = (
            f"👋 Hola {user.first_name}, aquí tienes tu estado:\n\n"
            f"📧 Email: {user.email}\n"
            f"📌 Rol: {user.role}\n"
            f"✅ Estado: {user.estado}\n"
            f"🗓 Registrado: {user.fecha_registro.strftime('%Y-%m-%d') if user.fecha_registro else 'N/A'}\n\n"
            f"📎 Adjunto encontrarás el reporte en formato {file_type.upper()}."
        )

        send_telegram_message(chat_id_int, mensaje)
        send_telegram_document(chat_id_int, buffer, file_name)

        messages.success(request, "✅ Reporte enviado con éxito")
        return redirect("reportes")


@login_required
def reportes_view(request):
    # Obtener el perfil y su rol
    perfil = Users.objects.filter(username=request.user.username).first()
    
    # Si el usuario no es administrador, lo redirigimos al home
    if not perfil or not perfil.role or perfil.role.nombre != "Administrador":
        return redirect('home')  

    # Si es administrador, mostramos los reportes
    users = Users.objects.all()
    return render(request, "reportes.html", {"users": users})


@login_required
def enviar_notificacion(request):
    if request.method == "POST":
        destinatario_username = request.POST.get("destinatario")
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        fecha_envio = request.POST.get("fecha_envio")

        try:
            user = Users.objects.get(username=destinatario_username)
        except Users.DoesNotExist:
            messages.error(request, "❌ Usuario no encontrado")
            return redirect("enviar_notificacion")

        if not user.chat_id:
            messages.error(request, f"⚠️ Usuario {user.username} no tiene chat_id")
            return redirect("enviar_notificacion")

        try:
            chat_id_int = int(user.chat_id)
        except ValueError:
            messages.error(request, f"❌ chat_id inválido para {user.username}")
            return redirect("enviar_notificacion")

        # Crear mensaje formateado
        mensaje = (
            f"📢 <b>{titulo}</b>\n\n"
            f"{descripcion}\n\n"
            f"🗓 Fecha de envío: {fecha_envio}"
        )

        send_telegram_message(chat_id_int, mensaje)
        messages.success(request, "✅ Notificación enviada con éxito")
        return redirect("enviar_notificacion")

    usuarios = Users.objects.all()
    return render(request, "enviar_notificacion.html", {"usuarios": usuarios})