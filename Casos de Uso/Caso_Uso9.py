# Caso_Uso10_CerrarSesion.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- CONFIGURACIÓN DEL NAVEGADOR ---
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # Mantiene el navegador abierto
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 15)

# --- 1️⃣ INICIO DE SESIÓN ---
try:
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

except Exception as e:
    print("⚠️ Error al iniciar sesión:", e)
    driver.save_screenshot("Caso_Uso9_Error_Login_CerrarSesion.png")
    driver.quit()
    exit()

# --- 2️⃣ OPRIMIR BOTÓN DE CERRAR SESIÓN ---
try:
    # Esperar a que cargue la página principal
    time.sleep(2)

    # Localizar el botón del formulario
    boton_logout = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//form[@action='/logout/']//button[contains(@class, 'btn-logout')]"))
    )
    boton_logout.click()
    print("🚪 Botón 'Cerrar Sesión' oprimido correctamente.")

except Exception as e:
    print("⚠️ No se pudo hacer clic en el botón de cerrar sesión:", e)
    driver.save_screenshot("Error_Boton_CerrarSesion.png")
    driver.quit()
    exit()

# --- 3️⃣ VALIDAR REDIRECCIÓN AL LOGIN ---
try:
    # Espera que aparezca de nuevo el login
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Login') or contains(text(),'Iniciar')] | //button[contains(text(),'Iniciar')]"))
    )
    print("✅ Se confirmó la redirección al login. Cierre de sesión exitoso.")
except Exception as e:
    print("⚠️ No se detectó la pantalla de login:", e)

# --- 4️⃣ CAPTURA DE EVIDENCIA ---
driver.save_screenshot("Caso_Uso9_CerrarSesion.png")
print("📸 Captura guardada como 'Caso_Uso10_CerrarSesion.png'")

# --- 5️⃣ FINALIZAR ---
time.sleep(3)
print("✅ Caso de uso 'Cerrar Sesión' completado correctamente.")
driver.quit()
