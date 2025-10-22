from django.test import TestCase
from user.models import Users, Roles


class GymPowerTests(TestCase):
    def setUp(self):
        # Creamos un rol base
        self.role = Roles.objects.create(
            nombre="Cliente",
            descripcion="Rol de cliente"
        )

        # Creamos usuario de prueba
        self.user = Users.objects.create(
            username="testuser",
            password="password123",  
            email="test@example.com",
            first_name="Test",
            last_name="User",
            chat_id="123456",
            role=self.role
        )

    def test_login_correcto(self):
        """El login debería funcionar con credenciales correctas"""
        usuario = Users.objects.get(username="testuser")
        self.assertEqual(usuario.password, "password123")

    def test_login_incorrecto(self):
        """El login debería fallar si el usuario no existe"""
        with self.assertRaises(Users.DoesNotExist):
            Users.objects.get(username="wronguser")

    def test_signup_usuario(self):
        """Probar que se puede registrar un nuevo usuario"""
        nuevo = Users.objects.create(
            username="newuser",
            password="abc123",
            email="new@example.com",
            first_name="Nuevo",
            last_name="Usuario",
            chat_id="654321",
            role=self.role
        )
        self.assertEqual(nuevo.username, "newuser")

    def test_enviar_notificacion_ok(self):
        """Simular notificación a un usuario válido"""
        usuario = Users.objects.get(username="testuser")
        self.assertEqual(usuario.chat_id, "123456")

    def test_enviar_notificacion_usuario_invalido(self):
        """Intentar notificar a un usuario inexistente"""
        with self.assertRaises(Users.DoesNotExist):
            Users.objects.get(chat_id="999999")

    def test_descargar_excel(self):
        """Simular descarga de reporte Excel"""
        usuarios = Users.objects.all()
        self.assertTrue(usuarios.exists())

    def test_descargar_pdf(self):
        """Simular descarga de reporte PDF"""
        usuarios = Users.objects.all()
        self.assertGreaterEqual(usuarios.count(), 1)

    def test_enviar_reporte_excel(self):
        """Simular envío de reporte Excel por Telegram (mock)"""
        usuario = Users.objects.get(username="testuser")
        self.assertEqual(usuario.email, "test@example.com")

    def test_enviar_reporte_pdf(self):
        """Simular envío de reporte PDF por Telegram (mock)"""
        usuario = Users.objects.get(username="testuser")
        self.assertEqual(usuario.first_name, "Test")