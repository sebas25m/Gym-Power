# Caso_Uso12.py
# 🧩 Caso de uso 12: Restablecer contraseña con correo inválido (sin @)
# 📸 Solo se guarda el pantallazo final con el mensaje de error

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# --- CONFIGURACIÓN DEL DRIVER ---
driver = webdriver.Chrome()
driver.maximize_window()

# --- CARPETA DE PANTALLAZOS ---
carpeta = os.path.join(os.getcwd(), "Pantallazos_Casos_Uso")
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

try:
    # 1️⃣ Ir al módulo de inicio de sesión
    driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/login/")
    print("🌐 Página de login abierta.")
    time.sleep(2)

    # 2️⃣ Clic en el enlace “¿Olvidaste tu contraseña?”
    forgot_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/password_reset/']"))
    )
    forgot_link.click()
    print("🔗 Enlace '¿Olvidaste tu contraseña?' presionado correctamente.")
    time.sleep(2)

    # 3️⃣ Esperar a que aparezca el campo de correo
    correo_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )

    # 4️⃣ Ingresar un correo inválido (sin "@")
    correo_invalido = "usuario_prueba_gmail.com"
    correo_input.send_keys(correo_invalido)
    print(f"🚫 Correo inválido ingresado: {correo_invalido}")
    time.sleep(1)

    # 5️⃣ Enviar el formulario
    correo_input.send_keys(Keys.ENTER)
    print("📤 Intentando enviar formulario con correo inválido...")
    time.sleep(3)

    # 📸 SOLO UN PANTALLAZO FINAL: mensaje de error o validación
    driver.save_screenshot(os.path.join(carpeta, "Caso_Uso11_MensajeError.png"))

    print("⚠️ Caso de uso 12 ejecutado correctamente. Se capturó el mensaje de error final.")

except Exception as e:
    print(f"❌ Error durante el caso de uso 12: {e}")
    driver.save_screenshot(os.path.join(carpeta, "Caso_Uso11_Error.png"))

finally:
    time.sleep(2)
    driver.quit()
    print("🧩 Caso de uso 11 finalizado y navegador cerrado.")
