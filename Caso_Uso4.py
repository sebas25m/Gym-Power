from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# --- CONFIGURACIÓN DE CARPETAS ---
# 📁 Carpeta de descargas de reportes
download_dir = os.path.join(os.getcwd(), "reportes_descargados")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# 📁 Carpeta de pantallazos (como los otros casos)
pantallazos_dir = os.path.join(os.getcwd(), "Pantallazos_Casos_Uso")
if not os.path.exists(pantallazos_dir):
    os.makedirs(pantallazos_dir)

# --- CONFIGURACIÓN DEL NAVEGADOR ---
chrome_options = Options()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Iniciar navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    # --- 1️⃣ ABRIR PÁGINA DE LOGIN ---
    driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/login/")
    print("🌐 Página de login abierta correctamente.")

    # --- 2️⃣ ENCONTRAR CAMPOS DE LOGIN ---
    usuario_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@type,'text') or contains(@name,'user') or contains(@name,'email')]"))
    )
    password_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
    )

    # --- 3️⃣ INGRESAR CREDENCIALES ---
    usuario_input.send_keys("User_Juan16")
    password_input.send_keys("Tabogo1609:*")

    # --- 4️⃣ CLIC EN BOTÓN LOGIN ---
    boton_login = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login') or contains(text(),'Iniciar')]"))
    )
    boton_login.click()
    print("🔐 Credenciales ingresadas correctamente.")

    # --- 5️⃣ ESPERAR CARGA DE PÁGINA PRINCIPAL ---
    time.sleep(4)

    # --- 6️⃣ IR AL MÓDULO DE REPORTES ---
    driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/reportes/")
    print("📊 Página de reportes abierta.")
    time.sleep(3)

    # --- 7️⃣ HACER CLIC EN EL BOTÓN DE DESCARGAR PDF ---
    boton_pdf = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/reportes/pdf/' and contains(@class,'btn-pdf')]"))
    )
    boton_pdf.click()
    print("📄 Clic en 'Descargar PDF' realizado correctamente.")

    # --- 8️⃣ ESPERAR DESCARGA ---
    time.sleep(6)

    # --- 9️⃣ TOMAR UN ÚNICO PANTALLAZO FINAL ---
    ruta_pantallazo = os.path.join(pantallazos_dir, "Caso_Uso4_Reporte_Usuarios.png")
    driver.save_screenshot(ruta_pantallazo)
    print(f"📸 Pantallazo final guardado en: {ruta_pantallazo}")

    # --- 🔟 VALIDAR DESCARGA ---
    archivos = os.listdir(download_dir)
    print("✅ Archivos descargados:", archivos)

except Exception as e:
    print("⚠️ Error durante la ejecución:", e)
    ruta_error = os.path.join(pantallazos_dir, "Caso_Uso4_Reporte_Usuarios_Error.png")
    driver.save_screenshot(ruta_error)
    print(f"📸 Pantallazo de error guardado en: {ruta_error}")

finally:
    driver.quit()
    print("🔚 Caso de uso finalizado. Navegador cerrado.")
