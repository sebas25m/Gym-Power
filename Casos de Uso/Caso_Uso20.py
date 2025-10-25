from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time

# 📁 Carpeta de pantallazos
ruta_pantallazos = "pantallazos_Casos_uso"
os.makedirs(ruta_pantallazos, exist_ok=True)

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

try:
    print("🟢 Iniciando sesión como cliente...")
    driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/login/")
    driver.maximize_window()

    # ✅ CAMBIA ESTAS CREDENCIALES SI TU CLIENTE TIENE OTRAS
    usuario = "User_Juan16"
    clave = "Tabogo1609:*"

    # --- LOGIN ---
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(usuario)
    driver.find_element(By.NAME, "password").send_keys(clave)

    # Botón login (detecta input o button)
    try:
        boton_login = driver.find_element(By.XPATH, "//input[@type='submit']")
    except:
        boton_login = driver.find_element(By.XPATH, "//button[contains(text(),'Login') or contains(text(),'Iniciar') or contains(text(),'Entrar')]")
    boton_login.click()

    # Esperar que cargue home
    wait.until(EC.url_contains("/home"))
    driver.save_screenshot(f"{ruta_pantallazos}/Eliminar_01_Login_Exitoso.png")
    print("✅ Inicio de sesión correcto.")

    # --- GESTIONAR USUARIOS ---
    print("📂 Ingresando al módulo 'Gestionar Usuarios'...")
    gestionar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/listar')]")))
    gestionar_btn.click()
    wait.until(EC.url_contains("/listar"))
    driver.save_screenshot(f"{ruta_pantallazos}/Eliminar_02_ModuloUsuarios.png")

    # --- BUSCAR USUARIO SHARON ---
    print("🔍 Buscando usuario 'sharon_vargas'...")
    filas = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr")))
    usuario_objetivo = None

    for fila in filas:
        if "sharon_vargas" in fila.text:
            usuario_objetivo = fila
            break

    if not usuario_objetivo:
        print("⚠️ No se encontró el usuario 'sharon_vargas'.")
        driver.save_screenshot(f"{ruta_pantallazos}/Eliminar_UsuarioNoEncontrado.png")
    else:
        print("🗑️ Usuario encontrado, procediendo a eliminar...")
        usuario_objetivo.location_once_scrolled_into_view
        driver.save_screenshot(f"{ruta_pantallazos}/Eliminar_03_UsuarioEncontrado.png")

        # Click en eliminar
        eliminar_btn = usuario_objetivo.find_element(By.XPATH, ".//a[contains(text(),'Eliminar') or contains(@class,'btn-eliminar')]")
        eliminar_btn.click()
        time.sleep(2)

        # Confirmar alerta si aparece
        try:
            alert = wait.until(EC.alert_is_present())
            alert.accept()
            print("⚠️ Alerta de eliminación confirmada.")
        except:
            print("ℹ️ No apareció alerta, eliminación directa.")

        time.sleep(2)
        driver.save_screenshot(f"{ruta_pantallazos}/Eliminar_04_UsuarioEliminado.png")
        print("✅ Usuario eliminado correctamente.")

except Exception as e:
    print("❌ Error durante la ejecución:", e)
    driver.save_screenshot(f"{ruta_pantallazos}/Eliminar_Error.png")

finally:
    driver.quit()
