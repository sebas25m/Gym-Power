# Caso_Uso9_EnviarNotificacion_Formulario.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import os

# Carpeta para guardar el pantallazo
carpeta_actual = os.getcwd()
ruta_pantallazo = os.path.join(carpeta_actual, "Caso_Uso8_EnviarNotificacion.png")

# Configuración del navegador
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 15)

try:
    # 1️⃣ Abrir login
    driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/login/")
    print("🌐 Página de login abierta.")

    usuario_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    contrasena_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    usuario_input.send_keys("User_Juan16")
    contrasena_input.send_keys("Tabogo1609:*")

    boton_login = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Iniciar') or contains(text(),'Login')]"))
    )
    boton_login.click()
    print("✅ Sesión iniciada correctamente.")

    # 2️⃣ Entrar al módulo de notificaciones
    boton_notificacion = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/notificaciones/') and contains(text(),'Enviar Notificación')]"))
    )
    boton_notificacion.click()
    print("📢 Se ingresó a 'Enviar Notificación'.")

    # 3️⃣ Llenar el formulario
    destinatario_select = wait.until(EC.presence_of_element_located((By.NAME, "destinatario")))
    Select(destinatario_select).select_by_visible_text("User_Juan16")

    titulo_input = wait.until(EC.presence_of_element_located((By.NAME, "titulo")))
    titulo_input.send_keys("Pago de mensualidad")

    descripcion_input = wait.until(EC.presence_of_element_located((By.NAME, "descripcion")))
    descripcion_input.send_keys("El próximo pago se debe realizar 5 días antes de finalizar el mes.")

    fecha_input = wait.until(EC.presence_of_element_located((By.NAME, "fecha_envio")))
    fecha_actual = datetime.now().strftime("%Y-%m-%dT%H:%M")
    # Asignar fecha/hora como si se seleccionara en el calendario
    driver.execute_script("arguments[0].value = arguments[1];", fecha_input, fecha_actual)

    print("📝 Formulario completado correctamente.")

    # 4️⃣ Guardar
    boton_guardar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(),'Guardar')]"))
    )
    boton_guardar.click()
    print("💾 Botón 'Guardar' presionado correctamente.")

    # Esperar un momento para que la acción se procese
    time.sleep(2)

except Exception as e:
    print("⚠️ Error durante el caso de uso:", e)

finally:
    # 5️⃣ Tomar pantallazo final
    driver.save_screenshot(ruta_pantallazo)
    print(f"📸 Pantallazo guardado en: {ruta_pantallazo}")

    # 6️⃣ Finalizar
    time.sleep(2)
    driver.quit()
    print("✅ Caso de uso completado correctamente.")
