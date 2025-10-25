from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import random
import time

# Configuración del driver
driver = webdriver.Chrome()  # Asegúrate de tener chromedriver en tu PATH
driver.maximize_window()

# 1. Abrir la página de login
driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/login/")

# 2. Espera hasta que los campos estén presentes
wait = WebDriverWait(driver, 10)

# Ajusta los selectores según lo que tenga la página real
username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

# 3. Iniciar sesión
username_input.send_keys("User_Juan16")
password_input.send_keys("Tabogo1609:*")
login_button.click()

# Esperar a que la página principal cargue
time.sleep(3)

# 4. Ir al módulo de crear clase (ajusta la URL si es diferente)
driver.get("https://ernestine-conduplicate-potentially.ngrok-free.dev/create_class")
time.sleep(2)

# 5. Llenar formulario con datos random
nombre_clase = wait.until(EC.presence_of_element_located((By.NAME, "nombre_clase")))
descripcion = driver.find_element(By.NAME, "descripcion")
fecha = driver.find_element(By.NAME, "fecha")
hora = driver.find_element(By.NAME, "hora")

nombre_clase.send_keys(f"Clase_{random.randint(100,999)}")
descripcion.send_keys("Clase de prueba automatizada")
fecha.send_keys("2025-10-25")
hora.send_keys("15:30")

# Seleccionar tipo de clase si existe
try:
    tipo_select = Select(driver.find_element(By.NAME, "tipo_clase"))
    tipo_select.select_by_index(random.randint(1, len(tipo_select.options)-1))
except:
    print("No se encontró el select de tipo_clase, se omite.")

# Esperar a que aparezca el select de entrenador
try:
    entrenador_select = wait.until(EC.presence_of_element_located((By.NAME, "entrenador")))
    # Tomar pantallazo en el momento de escoger entrenador
    driver.save_screenshot("pantallazo_entrenador.png")
    print("Pantallazo guardado como 'pantallazo_entrenador.png'")
except:
    print("No se encontró el select de entrenador.")

# Cerrar navegador
driver.quit()
