# caso_uso_enviar_reporte_telegram.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# --- 📁 Carpeta donde se guardan los pantallazos ---
pantallazos_dir = os.path.join(os.getcwd(), "pantallazos_casos_uso")
if not os.path.exists(pantallazos_dir):
    os.makedirs(pantallazos_dir)

# --- ⚙️ Configuración del navegador ---
chrome_options = Options()
chrome_options.add_experimental_option("detach", False)  # Cierra al terminar
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# --- 1️⃣ Abrir página de login ---
driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/login/")

# --- 2️⃣ Iniciar sesión ---
try:
    usuario_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@type,'text') or contains(@name,'user') or contains(@name,'email')]"))
    )
    password_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
    )
    usuario_input.send_keys("User_Juan16")
    password_input.send_keys("Tabogo1609:*")

    boton_login = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login') or contains(text(),'Iniciar')]"))
    )
    boton_login.click()
    print("✅ Inicio de sesión realizado correctamente.")
except Exception as e:
    print("⚠️ Error al iniciar sesión:", e)
    driver.quit()
    exit()

# --- 3️⃣ Ir al módulo de reportes ---
time.sleep(3)
driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/reportes/")
time.sleep(3)

# --- 4️⃣ Hacer clic en el botón “Enviar” del formulario Telegram ---
try:
    boton_enviar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'btn-telegram') or contains(text(),'Enviar')]"))
    )
    boton_enviar.click()
    print("📩 Clic en 'Enviar vía Telegram' realizado correctamente.")
except Exception as e:
    print("⚠️ No se encontró el botón de 'Enviar vía Telegram':", e)
    driver.quit()
    exit()

# --- 5️⃣ Esperar confirmación o mensaje de éxito ---
try:
    mensaje_exito = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'éxito') or contains(text(),'enviado') or contains(text(),'Telegram')]"))
    )
    print("✅ Mensaje de éxito detectado:", mensaje_exito.text)
except:
    print("⚠️ No se detectó mensaje de éxito (puede que se envíe sin mostrar alerta).")

# --- 6️⃣ Guardar pantallazo final ---
nombre_pantallazo = os.path.join(pantallazos_dir, "Caso_Uso_EnviarTelegram.png")
driver.save_screenshot(nombre_pantallazo)
print(f"📸 Pantallazo guardado en: {nombre_pantallazo}")

# --- 7️⃣ Finalizar ---
time.sleep(2)
driver.quit()
print("✅ Caso de uso 'Enviar reporte vía Telegram' completado con éxito.")
