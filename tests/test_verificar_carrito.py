from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_ver_carrito(login_in_driver):
    driver = login_in_driver

    
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )

    
    productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(productos) > 1, "No se encontraron productos en la página"

    
    for i in range(2):  # agregar los dos primeros productos
        boton = productos[i].find_element(By.TAG_NAME, "button")
        driver.execute_script("arguments[0].scrollIntoView(true);", boton)
        driver.execute_script("arguments[0].click();", boton)
        time.sleep(0.5)

    
    badge = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert badge.text == "2", f"Se esperaba 2 en el carrito, se encontró {badge.text}"

    
    carrito_icono = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    driver.execute_script("arguments[0].click();", carrito_icono)

    
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )

    
    titulo = driver.find_element(By.CLASS_NAME, "title").text
    assert "YOUR CART" in titulo.upper()

    
    items_carrito = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    nombres = [item.text for item in items_carrito]

    print("\n🛒 Productos en el carrito:")
    for n in nombres:
        print("-", n)

    assert len(nombres) == 2, f"El carrito no contiene los 2 productos esperados (encontrados: {len(nombres)})"
    print("✅ Test OK: el carrito contiene los productos agregados.")

