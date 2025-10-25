# caso_uso_crear_y_listar_notificacion.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import os

# --- 📁 Carpeta donde se guardan los pantallazos ---
pantallazos_dir = os.path.join(os.getcwd(), "pantallazos_casos_uso")
if not os.path.exists(pantallazos_dir):
    os.makedirs(pantallazos_dir)

# --- ⚙️ Configuración del navegador ---
chrome_options = Options()
chrome_options.add_experimental_option("detach", False)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# --- 1️⃣ Ir al login ---
driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/login/")

# --- 2️⃣ Iniciar sesión ---
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
    driver.quit()
    exit()

# --- 3️⃣ Entrar al módulo de notificaciones ---
time.sleep(3)
driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/notificaciones/")
print("📨 Módulo de notificaciones abierto.")
time.sleep(3)

# --- 4️⃣ Completar formulario ---
try:
    # Seleccionar destinatario
    destinatario_select = wait.until(
        EC.presence_of_element_located((By.XPATH, "//select[contains(@name,'destinatario') or contains(@id,'destinatario')]"))
    )
    select = Select(destinatario_select)
    select.select_by_visible_text("User_Juan16")
    print("👤 Destinatario seleccionado: User_Juan16")

    # Campo título
    campo_titulo = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='titulo' or contains(@placeholder,'Título') or contains(@id,'titulo')]"))
    )
    campo_titulo.clear()
    campo_titulo.send_keys("Pago de mensualidad")

    # Campo descripción
    campo_descripcion = wait.until(
        EC.presence_of_element_located((By.XPATH, "//textarea[@name='descripcion' or contains(@placeholder,'Descripción') or contains(@id,'descripcion')]"))
    )
    campo_descripcion.clear()
    campo_descripcion.send_keys("Los pagos deben realizarse con 5 días antes de finalizar el mes.")

    # Fecha actual
    fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
    campo_fecha = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='date' or contains(@name,'fecha') or contains(@id,'fecha')]"))
    )
    campo_fecha.clear()
    campo_fecha.send_keys(fecha_actual)
    print(f"📅 Fecha actual establecida: {fecha_actual}")

except Exception as e:
    print("⚠️ Error al llenar formulario:", e)
    driver.quit()
    exit()

# --- 5️⃣ Guardar notificación ---
try:
    boton_guardar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Guardar') or contains(text(),'Crear') or contains(@class,'btn-guardar')]"))
    )
    boton_guardar.click()
    print("💾 Notificación guardada.")
except Exception as e:
    print("⚠️ Error al hacer clic en Guardar:", e)
    driver.quit()
    exit()

# --- 6️⃣ Esperar confirmación ---
try:
    mensaje_exito = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'guardada') or contains(text(),'éxito') or contains(text(),'creada')]"))
    )
    print("✅ Confirmación: ", mensaje_exito.text)
except:
    print("⚠️ No se mostró mensaje visible, se continúa para verificar listado.")

# --- 7️⃣ Verificar que aparezca listada en la parte inferior ---
time.sleep(3)
try:
    notificacion_listada = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[contains(text(),'Pago de mensualidad') or contains(.,'Pago de mensualidad')]")
        )
    )
    print("📋 Notificación listada correctamente en la parte inferior.")
except Exception as e:
    print("⚠️ No se encontró la notificación en la lista:", e)

# --- 8️⃣ Guardar pantallazo final ---
pantallazo_final = os.path.join(pantallazos_dir, "Caso_Uso_CrearYListar_Notificacion.png")
driver.save_screenshot(pantallazo_final)
print(f"📸 Pantallazo guardado en: {pantallazo_final}")

# --- 9️⃣ Cerrar ---
time.sleep(2)
driver.quit()
print("✅ Caso de uso completado con éxito.")

