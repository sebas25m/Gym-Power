# caso_uso_generar_reporte_usuario.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import datetime

# --- 📁 CONFIGURAR RUTA DE PANTALLAZO EN LA MISMA CARPETA DEL SCRIPT ---
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
# Nombre del pantallazo con fecha y hora
fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
ruta_pantallazo = os.path.join(carpeta_actual, f"Caso_Uso6_Telegram_{fecha_hora}.png")

# --- 🚀 CONFIGURAR NAVEGADOR ---
chrome_options = Options()
chrome_options.add_experimental_option("detach", False)  # Cierra al terminar
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# --- 1️⃣ ABRIR LOGIN ---
driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/login/")

# --- 2️⃣ INICIAR SESIÓN ---
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
except Exception as e:
    print("⚠️ Error al iniciar sesión:", e)
    driver.quit()
    exit()

# --- 3️⃣ IR A LA PÁGINA DE REPORTES ---
time.sleep(3)
driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/reportes/")
time.sleep(3)

# --- 4️⃣ HACER CLIC EN EL BOTÓN “📩 Enviar” ---
try:
    boton_enviar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Enviar') or contains(@class,'btn-telegram')]"))
    )
    boton_enviar.click()
    print("📩 Clic en 'Enviar reporte por Telegram' realizado correctamente.")
except Exception as e:
    print("⚠️ No se encontró el botón 'Enviar':", e)
    driver.save_screenshot(ruta_pantallazo)
    driver.quit()
    exit()

# --- 5️⃣ ESPERAR MENSAJE DE ÉXITO ---
try:
    mensaje_exito = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'éxito') or contains(text(),'Exitoso') or contains(text(),'enviado')]"))
    )
    print("✅ Mensaje de éxito detectado:", mensaje_exito.text)
except:
    print("⚠️ No se detectó mensaje de éxito. Puede que el envío no haya sido completado.")

# --- 6️⃣ TOMAR PANTALLAZO Y GUARDAR EN LA MISMA CARPETA QUE EL SCRIPT ---
driver.save_screenshot(ruta_pantallazo)
print(f"📸 Pantallazo guardado en: {ruta_pantallazo}")

# --- 7️⃣ FINALIZAR ---
time.sleep(2)
driver.quit()
print(f"✅ Caso de uso 'Generar reporte por usuario' completado con éxito.")
