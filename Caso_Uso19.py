from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import time, os

# 📁 Crear carpeta para los pantallazos
ruta_pantallazos = "pantallazos_Casos_uso"
os.makedirs(ruta_pantallazos, exist_ok=True)

# 🚀 Configurar el navegador
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

try:
    print("🟢 Abriendo página de login...")
    driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/login/")
    driver.maximize_window()

    # 1️⃣ Click en “Regístrate Ahora”
    registrarse_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/signup/']")))
    registrarse_link.click()

    wait.until(EC.url_contains("/signup"))
    time.sleep(2)
    driver.save_screenshot(f"{ruta_pantallazos}/Caso_Registro_1_Formulario.png")
    print("📋 Formulario de registro abierto.")

    # 2️⃣ Llenar los campos del formulario
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("sharon Vargas")
    driver.find_element(By.NAME, "email").send_keys("sharonvargas187@gmail.com")
    driver.find_element(By.NAME, "chat_id").send_keys("5912928976")
    driver.find_element(By.NAME, "password1").send_keys("12345")
    driver.find_element(By.NAME, "password2").send_keys("12345")
    driver.find_element(By.NAME, "name").send_keys("sharon")
    driver.find_element(By.NAME, "last_name").send_keys("Vargas")

    # Fecha actual
    hoy = date.today().strftime("%Y-%m-%d")
    driver.find_element(By.NAME, "membership_date").send_keys(hoy)

    # Seleccionar rol “Cliente”
    select_rol = Select(driver.find_element(By.NAME, "roles"))
    select_rol.select_by_visible_text("Cliente")

    # 🖼️ Pantallazo con los datos llenos
    time.sleep(1)
    driver.save_screenshot(f"{ruta_pantallazos}/Caso_Registro_2_DatosLlenos.png")

    # 3️⃣ Clic en Registrarse
    print("🖱️ Enviando formulario...")
    boton_registrar = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Registrarse']")
    boton_registrar.click()

    # 4️⃣ Esperar redirección o confirmación
    wait.until(EC.any_of(
        EC.url_contains("/login"),
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'/login/')]"))
    ))

    time.sleep(2)
    driver.save_screenshot(f"{ruta_pantallazos}/Caso_Registro_3_Final.png")

    print("✅ Caso de uso completado: Registro de nuevo usuario (pantallazos guardados).")

except Exception as e:
    print("❌ Error durante la ejecución:", e)

finally:
    driver.quit()
