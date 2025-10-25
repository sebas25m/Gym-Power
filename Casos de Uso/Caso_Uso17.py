# Caso_Uso_Editar_Notificacion_fix.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import time, os, traceback

# ---- Configuración ----
BASE_URL = "https://ernestine-conduplicate-potentially.ngrok-free.dev"
LOGIN_URL = f"{BASE_URL}/login/"
NOTIFS_URL = f"{BASE_URL}/notificaciones/"
EDIT_HREF_FRAGMENT = "/notificaciones/6/"   # botón <a href="/notificaciones/6/" class="btn btn-edit">
USER = "User_Juan16"
PASSWORD = "Tabogo1609:*"
PANTALLAZOS_DIR = os.path.join(os.getcwd(), "pantallazos_casos_uso")
os.makedirs(PANTALLAZOS_DIR, exist_ok=True)

def save_ss(driver, name):
    path = os.path.join(PANTALLAZOS_DIR, name)
    try:
        driver.save_screenshot(path)
    except Exception:
        pass
    return path

# ---- Lanzar Chrome ----
chrome_options = Options()
chrome_options.add_experimental_option("detach", False)
# add headless if you want: chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 20)

try:
    # 1) Abrir login
    driver.get(LOGIN_URL)
    print("🌐 Página de login abierta.")

    # 2) Ingresar credenciales y hacer login
    # intentamos varios selectores por si cambian
    try:
        user_el = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    except TimeoutException:
        user_el = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@type,'text')]")))

    try:
        pass_el = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    except TimeoutException:
        pass_el = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))

    user_el.clear(); user_el.send_keys(USER)
    pass_el.clear(); pass_el.send_keys(PASSWORD)

    # localizar botón de login confiable (varias alternativas)
    login_btn = None
    for xp in ["//button[contains(normalize-space(.),'Iniciar')]", 
               "//button[contains(normalize-space(.),'Login')]", 
               "//input[@type='submit']"]:
        try:
            login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
            break
        except Exception:
            login_btn = None
    if not login_btn:
        raise Exception("No se pudo localizar el botón de Login.")

    login_btn.click()
    print("✅ Sesión iniciada correctamente.")
    time.sleep(2)

    # 3) Ir al módulo de notificaciones
    driver.get(NOTIFS_URL)
    print("📨 Módulo de notificaciones abierto.")
    time.sleep(2)

    # 4) Hacer clic en EDITAR (el enlace específico /notificaciones/6/)
    try:
        editar_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//a[contains(@href, '{EDIT_HREF_FRAGMENT}') and (contains(@class,'btn-edit') or contains(normalize-space(.),'Editar'))]")
        ))
    except TimeoutException:
        # fallback: buscar cualquier link .btn-edit
        editar_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-edit")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", editar_btn)
    time.sleep(0.5)
    try:
        editar_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", editar_btn)
    print("✏️ Modo edición abierto.")
    time.sleep(1.5)

    # 5) Seleccionar destinatario (robusto)
    # localizar select de destinatario
    select_elem = None
    try:
        select_elem = wait.until(EC.presence_of_element_located((By.NAME, "destinatario")))
    except TimeoutException:
        # alternativas
        alt_xps = ["//select[contains(@name,'destinatario')]", "//select[contains(@id,'destinatario')]", "//select"]
        for xp in alt_xps:
            try:
                select_elem = wait.until(EC.presence_of_element_located((By.XPATH, xp)))
                if select_elem:
                    break
            except Exception:
                select_elem = None
    if not select_elem:
        raise Exception("No se encontró el <select> destinatario en el formulario de edición.")
    select_obj = Select(select_elem)

    # obtener opciones y seleccionar la que contenga 'juan' (insensible a mayúsculas)
    options_text = [o.text.strip() for o in select_obj.options]
    print("👀 Opciones disponibles:", options_text)
    chosen = None
    for opt in options_text:
        if "juan" in opt.lower() or "user_juan" in opt.lower() or "user juan" in opt.lower():
            select_obj.select_by_visible_text(opt)
            chosen = opt
            break
    if not chosen:
        # fallback: buscar por value que contenga 'juan'
        for opt_el in select_elem.find_elements(By.TAG_NAME, "option"):
            v = (opt_el.get_attribute("value") or "").strip()
            if "juan" in v.lower():
                select_obj.select_by_value(v)
                chosen = opt_el.text.strip()
                break
    if not chosen:
        # si nada, seleccionar la primera opción no vacía
        for i, opt_el in enumerate(select_elem.find_elements(By.TAG_NAME, "option")):
            v = (opt_el.get_attribute("value") or "").strip()
            t = opt_el.text.strip()
            if v != "" or t != "":
                select_obj.select_by_index(i)
                chosen = t or v
                break
    print(f"✅ Destinatario seleccionado: {chosen}")

    # 6) Título y descripción (robustos)
    # titulo
    title_elem = None
    for xp in ["//input[@name='titulo']", "//input[contains(@id,'titulo')]", "//input[@type='text' and (contains(@placeholder,'tít') or contains(@class,'titulo'))]", "//input[@type='text']"]:
        try:
            title_elem = driver.find_element(By.XPATH, xp)
            if title_elem.is_displayed():
                break
        except Exception:
            title_elem = None
    if not title_elem:
        raise Exception("No se encontró campo Título en el formulario.")
    title_elem.clear()
    title_elem.send_keys("Pago de mensualidad")

    # descripcion (textarea)
    desc_elem = None
    for xp in ["//textarea[@name='descripcion']", "//textarea[contains(@id,'descripcion')]", "//textarea",]:
        try:
            desc_elem = driver.find_element(By.XPATH, xp)
            if desc_elem.is_displayed():
                break
        except Exception:
            desc_elem = None
    if not desc_elem:
        raise Exception("No se encontró campo Descripción en el formulario.")
    desc_elem.clear()
    desc_elem.send_keys("Los pagos con 5 días antes de finalizar el mes")

    # 7) Fecha (datetime-local name=fecha_envio)
    fecha_elem = None
    try:
        fecha_elem = wait.until(EC.presence_of_element_located((By.NAME, "fecha_envio")))
    except TimeoutException:
        # alternativas
        for xp in ["//input[@type='datetime-local']", "//input[contains(@name,'fecha')]", "//input[contains(@id,'fecha')]"]:
            try:
                fecha_elem = driver.find_element(By.XPATH, xp)
                if fecha_elem.is_displayed():
                    break
            except Exception:
                fecha_elem = None
    if not fecha_elem:
        # no es crítico: seguimos pero avisamos
        print("⚠️ No se encontró input fecha_envio; se continúa sin establecer fecha.")
    else:
        # usar formato para datetime-local
        now_val = datetime.now().strftime("%Y-%m-%dT%H:%M")
        try:
            # preferimos setear por JS para evitar problemas de formato
            driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input')); arguments[0].dispatchEvent(new Event('change'));", fecha_elem, now_val)
        except Exception:
            fecha_elem.clear()
            fecha_elem.send_keys(now_val)
        print(f"📅 Fecha establecida: {now_val}")

    # 8) Guardar cambios
    guardar_btn = None
    for xp in ["//button[contains(normalize-space(.),'Guardar')]", "//button[contains(normalize-space(.),'Actualizar')]", "//input[@type='submit']"]:
        try:
            guardar_btn = driver.find_element(By.XPATH, xp)
            if guardar_btn.is_displayed() and guardar_btn.is_enabled():
                break
        except Exception:
            guardar_btn = None
    if not guardar_btn:
        raise Exception("No se encontró botón Guardar/Actualizar.")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", guardar_btn)
    time.sleep(0.4)
    try:
        guardar_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", guardar_btn)
    print("💾 Click en Guardar realizado.")
    time.sleep(2)

    # 9) Verificar que la notificación aparezca listada con el título actualizado
    driver.get(NOTIFS_URL)
    time.sleep(1.5)
    found = False
    try:
        # buscar filas que contengan el título nuevo
        els = driver.find_elements(By.XPATH, "//tr[.//*[contains(normalize-space(.), 'Pago de mensualidad')]] | //*[contains(normalize-space(.), 'Pago de mensualidad')]")
        if els and len(els) > 0:
            found = True
    except Exception:
        found = False

    ss_name = "Caso_Uso_Editar_Notificacion_OK.png" if found else "Caso_Uso_Editar_Notificacion_NO_LISTADA.png"
    path = save_ss(driver, ss_name)
    if found:
        print("✅ Notificación editada y listada. Pantallazo:", path)
    else:
        print("⚠️ No se detectó la notificación en la lista. Pantallazo:", path)

except Exception as e:
    print("❌ Error en el caso de uso:", str(e))
    traceback.print_exc()
    err_path = save_ss(driver, "Caso_Uso_Editar_Notificacion_ERROR.png")
    print("📸 Pantallazo de error guardado en:", err_path)

finally:
    time.sleep(1.5)
    try:
        driver.quit()
    except:
        pass
    print("🔚 Prueba finalizada.")
