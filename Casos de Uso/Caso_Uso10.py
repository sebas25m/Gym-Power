# Caso_Uso8.py
# 🧩 Caso de uso: Olvidé mi contraseña - Proyecto GYM

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import os

# --- CONFIGURACIÓN DEL DRIVER ---
driver = webdriver.Chrome()
driver.maximize_window()

# --- CREAR CARPETA DE PANTALLAZOS ---
carpeta = "Pantallazos_Casos_Uso"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

try:
    # 1️⃣ Ir a la página de login
    driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/login/")
    print("🌐 Página de login abierta.")
    time.sleep(2)

    # 📸 Pantallazo 1: Página de inicio de sesión
    driver.save_screenshot(f"{carpeta}/Caso_Uso10_Pantallazo1_Login.png")

    # 2️⃣ Hacer clic en el enlace "¿Olvidaste tu contraseña?"
    forgot_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/password_reset/']"))
    )
    forgot_link.click()
    print("🔗 Enlace '¿Olvidaste tu contraseña?' presionado correctamente.")
    time.sleep(2)

    # 📸 Pantallazo 2: Formulario de restablecer contraseña
    driver.save_screenshot(f"{carpeta}/Caso_Uso10_Pantallazo2_Formulario.png")

    # 3️⃣ Esperar que se cargue el campo de correo
    correo_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )

    # 4️⃣ Ingresar correo válido con "@"
    correo_valido = "usuario_prueba@gmail.com"
    correo_input.send_keys(correo_valido)
    print(f"📧 Correo ingresado: {correo_valido}")
    time.sleep(1)

    # 📸 Pantallazo 3: Correo ingresado
    driver.save_screenshot(f"{carpeta}/Caso_Uso10_Pantallazo3_CorreoIngresado.png")

    # 5️⃣ Enviar formulario (Enter)
    correo_input.send_keys(Keys.ENTER)
    print("📤 Formulario enviado para restablecer contraseña.")
    time.sleep(3)

    # 📸 Pantallazo 4: Confirmación de envío
    driver.save_screenshot(f"{carpeta}/Caso_Uso10_Pantallazo4_Confirmacion.png")

    print("✅ Se realizó la solicitud de restablecimiento correctamente.")

except Exception as e:
    print(f"⚠️ Error durante el caso de uso: {e}")
    # 📸 Pantallazo de error
    driver.save_screenshot(f"{carpeta}/Caso_Uso10_Error.png")

finally:
    time.sleep(2)
    driver.quit()
    print("🧩 Caso de uso finalizado y navegador cerrado.")
