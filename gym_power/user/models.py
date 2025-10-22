from django.db import models

class Roles(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"""{self.nombre}"""


class Users(models.Model):
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    chat_id = models.CharField(unique=True, max_length=50)
    fecha_registro = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    estado = models.CharField(max_length=8, blank=True, null=True, default='Activo')
    role = models.ForeignKey(Roles, models.SET_NULL, blank=True, null=True)
    
    
    def __str__(self):
        return f"""Usuario {self.id}: 
    - {self.username} 
    - {self.email}
    - {self.first_name} {self.last_name}
    - {self.role}
    - {self.estado}"""
    
    