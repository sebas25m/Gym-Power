from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# --- CONFIGURACIÓN ---
URL = "https://ernestine-conduplicate-potentially.ngrok-free.dev/login/"

# 📁 Crear carpeta de pantallazos si no existe
carpeta_pantallazos = os.path.join(os.getcwd(), "Pantallazos_Casos_Uso")
if not os.path.exists(carpeta_pantallazos):
    os.makedirs(carpeta_pantallazos)

# 🧠 Configurar el navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

try:
    # 1️⃣ Abrir la página
    driver.get(URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("🌐 Página cargada correctamente.")

    # 2️⃣ Localizar los campos de usuario y contraseña
    campo_usuario = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'], input[type='email']"))
    )
    campo_password = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
    )

    # 3️⃣ Dejar los campos vacíos y presionar Enter
    campo_usuario.clear()
    campo_password.clear()
    campo_password.send_keys(Keys.ENTER)
    print("🚫 Formulario enviado con campos vacíos...")

    # 4️⃣ Esperar mensaje de error o validación
    time.sleep(2)

    # 📸 Guardar pantallazo SOLO en la carpeta de casos de uso
    ruta_pantallazo = os.path.join(carpeta_pantallazos, "Caso_Uso1_MensajeError.png")
    driver.save_screenshot(ruta_pantallazo)
    print(f"📸 Pantallazo guardado en: {carpeta_pantallazos}")

    # 5️⃣ Buscar mensaje de error (si existe)
    try:
        mensaje_error = driver.find_element(
            By.XPATH, "//*[contains(text(),'correo') or contains(text(),'usuario') or contains(text(),'contraseña') or contains(text(),'vacío')]"
        )
        print("✅ Se detectó mensaje de error en pantalla:")
        print("→", mensaje_error.text)
    except:
        print("⚠️ No se encontró un mensaje de error visible. Verifica si el sitio lo muestra de otra forma.")

finally:
    time.sleep(3)
    driver.quit()
    print("🧩 Caso de uso 1 finalizado y navegador cerrado.")
