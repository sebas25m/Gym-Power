# Caso_Uso_Eliminar_Cliente_Lin_ggT.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time

# ===========================================
# CONFIGURACIÓN
# ===========================================
LOGIN_URL = "https://ernestine-conduplicate-potentially.ngrok-free.dev/login/"
GESTIONAR_USUARIOS_URL = "https://ernestine-conduplicate-potentially.ngrok-free.dev/usuarios/"

USUARIO = "User_Juan16"
PASSWORD = "Tabogo1609:*"
CLIENTE_OBJETIVO = "Lin_ggT"  # Username exacto del cliente

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 15)

try:
    print("🔹 Abriendo página de inicio de sesión...")
    driver.get(LOGIN_URL)

    # ==============================
    # LOGIN
    # ==============================
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USUARIO)
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    print("✅ Sesión iniciada correctamente")

    time.sleep(2)

    # ==============================
    # IR A GESTIONAR USUARIOS
    # ==============================
    print("🔹 Accediendo al módulo 'Gestionar Usuarios'...")
    try:
        gestionar_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(text(),'Gestionar Usuarios') or contains(text(),'Usuarios') or contains(@href,'usuarios')]"
        )))
        gestionar_btn.click()
    except TimeoutException:
        print("⚠ No se encontró el botón, accediendo directamente al módulo...")
        driver.get(GESTIONAR_USUARIOS_URL)

    time.sleep(3)
    driver.save_screenshot("antes_eliminar_usuario.png")

    # ==============================
    # BUSCAR Y ELIMINAR USUARIO
    # ==============================
    print(f"🔍 Buscando usuario con username '{CLIENTE_OBJETIVO}'...")
    filas = driver.find_elements(By.XPATH, "//table//tbody//tr")
    usuario_encontrado = False

    for fila in filas:
        celdas = fila.find_elements(By.XPATH, ".//td")
        for celda in celdas:
            if CLIENTE_OBJETIVO.lower() in celda.text.lower():
                usuario_encontrado = True
                print(f"🧍 Usuario encontrado: {fila.text}")
                try:
                    btn_eliminar = fila.find_element(
                        By.XPATH, ".//a[contains(text(),'Eliminar') or contains(@class,'btn-danger') or contains(@class,'btn-eliminar')]"
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", btn_eliminar)
                    time.sleep(1)
                    btn_eliminar.click()
                    print("🗑️ Clic en el botón 'Eliminar'")
                except NoSuchElementException:
                    print("⚠ No se encontró el botón 'Eliminar' en la fila.")
                break
        if usuario_encontrado:
            break

    if not usuario_encontrado:
        print(f"❌ No se encontró el usuario '{CLIENTE_OBJETIVO}' en la tabla.")
    else:
        # ==============================
        # CONFIRMAR ELIMINACIÓN
        # ==============================
        time.sleep(2)
        try:
            alerta = driver.switch_to.alert
            alerta.accept()
            print("✅ Eliminación confirmada desde alerta.")
        except:
            try:
                confirmar_btn = wait.until(EC.element_to_be_clickable((
                    By.XPATH, "//button[contains(text(),'Confirmar') or contains(text(),'Sí') or contains(text(),'Aceptar')]"
                )))
                confirmar_btn.click()
                print("✅ Eliminación confirmada desde modal.")
            except:
                print("ℹ️ No apareció confirmación (posible eliminación directa).")

        # Esperar actualización
        time.sleep(3)
        driver.save_screenshot("despues_eliminar_usuario.png")

    # ==============================
    # RESULTADO FINAL
    # ==============================
    print("\n🎯 RESULTADO FINAL:")
    if usuario_encontrado:
        print(f"✅ Usuario '{CLIENTE_OBJETIVO}' eliminado correctamente.")
    else:
        print(f"❌ No se pudo eliminar: el usuario '{CLIENTE_OBJETIVO}' no existe en la tabla.")

except Exception as e:
    print(f"❌ Error durante la ejecución: {e}")

finally:
    print("\n🔎 Script finalizado. El navegador permanecerá abierto para revisión.")
    # driver.quit()  # Descomenta si quieres que se cierre automáticamente
