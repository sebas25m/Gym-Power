# Caso_Uso7_VolverHome.py - Volver al Home desde Reportes
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
chrome_options.add_experimental_option("detach", True)  # Mantiene el navegador abierto al final
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 15)

# --- 1. ABRIR LOGIN ---
driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/login/")

# --- 2. INICIAR SESIÓN ---
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
    print("✅ Sesión iniciada correctamente.")
except Exception as e:
    print("⚠️ Error al iniciar sesión:", e)
    driver.save_screenshot("Error_Login.png")
    driver.quit()
    exit()

# --- 3. IR A LA PÁGINA DE REPORTES ---
time.sleep(3)
driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/reportes/")
print("📂 Página de reportes abierta correctamente.")

# --- 4. HACER CLIC EN “Volver al Home” ---
try:
    # Ajusta el selector según el HTML del botón
    boton_home = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Home') or contains(text(),'Volver')]"))
    )
    boton_home.click()
    print("🏠 Clic en 'Volver al Home' realizado correctamente.")
except Exception as e:
    print("⚠️ No se encontró el botón 'Volver al Home':", e)
    driver.save_screenshot("Error_BotonHome.png")
    driver.quit()
    exit()

# --- 5. VERIFICAR QUE SE REDIRECCIONÓ AL HOME ---
time.sleep(3)
current_url = driver.current_url

if "home" in current_url.lower() or "inicio" in current_url.lower():
    print("✅ Redirección exitosa: el usuario volvió al Home.")
else:
    print("⚠️ No se detectó redirección al Home. URL actual:", current_url)

# --- 6. TOMAR CAPTURA ---
driver.save_screenshot("Caso_Uso7_VolverHome.png")
print("📸 Captura guardada como 'Caso_Uso7_VolverHome.png'")

# --- 7. FINALIZAR ---
time.sleep(3)
print("✅ Caso de uso 'Volver al Home' completado con éxito.")
