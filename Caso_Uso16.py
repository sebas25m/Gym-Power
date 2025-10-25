# Caso_Uso_Eliminar_Notificacion.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# --- 📁 Carpeta de pantallazos ---
screenshot_dir = os.path.join(os.getcwd(), "pantallazos_casos_uso")
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

def screenshot(filename):
    """Guarda pantallazos en la carpeta pantallazos_casos_uso."""
    path = os.path.join(screenshot_dir, filename)
    driver.save_screenshot(path)
    return path

# --- 🚀 Configurar navegador ---
chrome_options = Options()
chrome_options.add_experimental_option("detach", False)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    # --- 1️⃣ Abrir la página de login ---
    driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/login/")

    # --- 2️⃣ Iniciar sesión ---
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
    print("✅ Sesión iniciada correctamente.")

    # --- 3️⃣ Ir al módulo de notificaciones ---
    time.sleep(3)
    driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/notificaciones/")
    print("📨 Módulo de notificaciones abierto.")

    # --- 4️⃣ Buscar la notificación “Pago de mensualidad” ---
    notif_xpath = "//*[contains(text(),'Pago de mensualidad')]"
    wait.until(EC.presence_of_element_located((By.XPATH, notif_xpath)))
    print("🔍 Notificación encontrada: 'Pago de mensualidad'")

    # --- 5️⃣ Buscar el botón “Eliminar” en la misma fila ---
    fila_notif = wait.until(
        EC.presence_of_element_located((By.XPATH, "//tr[.//*[contains(text(),'Pago de mensualidad')]]"))
    )
    btn_eliminar = fila_notif.find_element(By.XPATH, ".//a[contains(@href,'/notificaciones/delete') and contains(@class,'btn-delete')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", btn_eliminar)
    time.sleep(1)
    btn_eliminar.click()
    print("🗑️ Clic en 'Eliminar' ejecutado.")

    # --- 6️⃣ Confirmar alerta ---
    try:
        time.sleep(2)
        alert = wait.until(EC.alert_is_present())
        print("⚠️ Confirmación detectada:", alert.text)
        alert.accept()
        print("✅ Confirmación aceptada.")
    except:
        print("⚠️ No se detectó alerta de confirmación, continuando...")

    # --- 7️⃣ Verificar que ya no exista ---
    time.sleep(3)
    notifs = driver.find_elements(By.XPATH, notif_xpath)
    if len(notifs) == 0:
        print("✅ Notificación 'Pago de mensualidad' eliminada correctamente.")
        path = screenshot("Caso_Uso_Eliminar_Notificacion_OK.png")
    else:
        print("⚠️ La notificación aún aparece.")
        path = screenshot("Caso_Uso_Eliminar_Notificacion_ERROR.png")

    print("📸 Pantallazo guardado en:", path)

except Exception as e:
    print("⚠️ Error en el caso de uso:", e)
    path = screenshot("Caso_Uso_Eliminar_Notificacion_ERROR.png")
    print("📸 Pantallazo de error guardado en:", path)

finally:
    time.sleep(2)
    driver.quit()
    print("🔚 Prueba finalizada.")
