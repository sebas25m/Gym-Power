from locust import HttpUser, task, between

# ---------- CLASE BASE ----------
class BaseUser(HttpUser):
    wait_time = between(1, 5)
    abstract = True

    def on_start(self):
        """Cada usuario inicia sesión antes de empezar"""
        self.login()

    def login(self):
        """Login correcto con token CSRF"""
        response = self.client.get("/login/")
        csrftoken = response.cookies.get("csrftoken", "")

        if not csrftoken:
            print("⚠️ No se encontró token CSRF en /login/")
            return

        payload = {
            "username": self.username,
            "password": self.password,
            "csrfmiddlewaretoken": csrftoken,
        }

        headers = {"Referer": self.client.base_url}

        response = self.client.post("/login/", data=payload, headers=headers)

        # Verificar éxito
        if response.status_code in [200, 302]:
            print(f"✅ {self.username} logged in correctamente")
        else:
            print(f"❌ Login failed for {self.username} ({response.status_code})")
            print(response.text[:200])


# ---------- ADMINISTRADOR ----------
class AdminUser(BaseUser):
    username = "root"
    password = "Prueba1234"

    @task(2)
    def home(self):
        self.client.get("/home/")

    @task(3)
    def listar_usuarios(self):
        self.client.get("/listar/")

    @task(2)
    def crear_clase(self):
        self.client.get("/crear_clase/")

    @task(3)
    def listar_clases(self):
        self.client.get("/listar_clases/")

    @task(1)
    def reportes(self):
        self.client.get("/reportes/")

    @task(1)
    def enviar_notificacion(self):
        self.client.get("/enviar_notificacion/")

    @task(1)
    def editar_perfil(self):
        self.client.get("/editar/1/")

    @task(1)
    def logout(self):
        self.client.post("/logout/")


# ---------- ENTRENADOR ----------
class EntrenadorUser(BaseUser):
    username = "entrenador"
    password = "entrenador123"

    @task(3)
    def home(self):
        self.client.get("/home/")

    @task(2)
    def crear_clase(self):
        self.client.get("/crear_clase/")

    @task(3)
    def listar_clases(self):
        self.client.get("/listar_clases/")

    @task(1)
    def editar_perfil(self):
        self.client.get("/editar/2/")


# ---------- CLIENTE ----------
class ClienteUser(BaseUser):
    username = "cliente"
    password = "cliente123"

    @task(3)
    def home(self):
        self.client.get("/home/")

    @task(4)
    def listar_clases(self):
        self.client.get("/listar_clases/")

    @task(2)
    def editar_perfil(self):
        self.client.get("/editar/3/")

    @task(1)
    def logout(self):
        self.client.post("/logout/")
