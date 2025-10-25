from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# ---------------- CONFIG ----------------
URL_LOGIN = "https://ernestine-conduplicate-potentially.ngrok-free.dev/login/"
USER = "User_Juan16"
PASSWORD = "Tabogo1609:*"
WAIT_TIME = 10
# ----------------------------------------

# 📁 Crear carpeta de pantallazos si no existe
carpeta_pantallazos = os.path.join(os.getcwd(), "Pantallazos_Casos_Uso")
if not os.path.exists(carpeta_pantallazos):
    os.makedirs(carpeta_pantallazos)

# 🚀 Configurar navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, WAIT_TIME)

try:
    # 1️⃣ Abrir la página de login
    driver.get(URL_LOGIN)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("🌐 Página de login cargada correctamente.")

    # 2️⃣ Ingresar usuario y contraseña
    campo_user = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    campo_pass = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    campo_user.send_keys(USER)
    campo_pass.send_keys(PASSWORD)
    campo_pass.send_keys(Keys.ENTER)
    print("🔐 Credenciales ingresadas y formulario enviado.")

    # 3️⃣ Esperar que cargue la página principal
    wait.until(EC.url_contains("/home"))
    print("✅ Inicio de sesión exitoso, preparando logout...")

    # 4️⃣ Buscar y hacer clic en el botón “Cerrar sesión” o “Logout”
    posibles_selectores = [
        (By.LINK_TEXT, "Cerrar sesión"),
        (By.LINK_TEXT, "Logout"),
        (By.PARTIAL_LINK_TEXT, "Cerrar"),
        (By.CSS_SELECTOR, "button[id*='logout']"),
        (By.CSS_SELECTOR, "a[href*='logout']"),
        (By.CSS_SELECTOR, "button[class*='logout']"),
        (By.XPATH, "//button[contains(text(),'Cerrar')]"),
        (By.XPATH, "//a[contains(text(),'Cerrar')]"),
    ]

    logout_button = None
    for sel in posibles_selectores:
        try:
            logout_button = wait.until(EC.element_to_be_clickable(sel))
            logout_button.click()
            print(f"🖱️ Se hizo clic en el botón de cerrar sesión con selector {sel}")
            break
        except Exception:
            continue

    if not logout_button:
        raise Exception("❌ No se encontró el botón de Cerrar Sesión. Verifica el selector HTML.")

    # 5️⃣ Esperar redirección al login
    wait.until(EC.url_contains("/login"))
    print("🔄 Redirigido al login tras cerrar sesión.")

    # 6️⃣ Tomar un único pantallazo final
    ruta_pantallazo = os.path.join(carpeta_pantallazos, "Caso_Uso3_Logout_Exitoso.png")
    driver.save_screenshot(ruta_pantallazo)
    print(f"📸 Pantallazo guardado en: {ruta_pantallazo}")

except Exception as e:
    print("⚠️ Error durante el proceso de logout:", e)
    ruta_error = os.path.join(carpeta_pantallazos, "Caso_Uso3_Logout_Error.png")
    driver.save_screenshot(ruta_error)
    print(f"📸 Pantallazo de error guardado en: {ruta_error}")

finally:
    time.sleep(2)
    driver.quit()
    print("🔚 Caso de uso de logout finalizado. Navegador cerrado.")
