from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os

ruta_pantallazos = "pantallazos_Casos_uso"
os.makedirs(ruta_pantallazos, exist_ok=True)

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

try:
    print("🟢 Iniciando navegador...")
    driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/login/")
    driver.maximize_window()

    print("🔑 Iniciando sesión...")
    username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    username.send_keys("User_Juan16")
    password.send_keys("Tabogo1609:*")
    driver.save_screenshot(f"{ruta_pantallazos}/Paso1_Login.png")

    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_btn.click()

    print("🏠 Esperando redirección a home...")
    wait.until(EC.url_contains("/home"))
    time.sleep(2)
    driver.save_screenshot(f"{ruta_pantallazos}/Paso2_Home.png")

    print("👥 Abriendo módulo Gestionar Usuarios...")
    gestionar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/listar/']")))
    gestionar_btn.click()

    wait.until(EC.url_contains("/listar"))
    time.sleep(2)
    driver.save_screenshot(f"{ruta_pantallazos}/Paso3_ModuloUsuarios.png")

    print("✏️ Buscando botón Editar...")
    editar_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/editar/')]"))
    )
    editar_href = editar_btn.get_attribute("href")
    print(f"➡️ Se encontró botón Editar: {editar_href}")
    editar_btn.click()

    wait.until(EC.url_contains("/editar/"))
    time.sleep(2)
    driver.save_screenshot(f"{ruta_pantallazos}/Paso4_FormularioEditar.png")

    print("📝 Editando campos...")
    campo_nombre = wait.until(EC.presence_of_element_located((By.NAME, "first_name")))
    campo_apellido = driver.find_element(By.NAME, "last_name")
    campo_email = driver.find_element(By.NAME, "email")

    campo_nombre.clear()
    campo_nombre.send_keys("Juan Editado")

    campo_apellido.clear()
    campo_apellido.send_keys("Selenium")

    campo_email.clear()
    campo_email.send_keys("juan.selenium@prueba.com")

    time.sleep(1)
    driver.save_screenshot(f"{ruta_pantallazos}/Paso5_DatosEditados.png")

    print("💾 Guardando cambios...")
    guardar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    guardar_btn.click()

    wait.until(EC.url_contains("/listar"))
    time.sleep(2)
    driver.save_screenshot(f"{ruta_pantallazos}/Paso6_CambiosGuardados.png")

    print("✅ Caso de uso completado exitosamente")

except Exception as e:
    print("❌ Error durante la ejecución:", e)

finally:
    driver.quit()
