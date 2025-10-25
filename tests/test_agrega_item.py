import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def login_in_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    yield driver
    driver.quit()


def test_agrega_item(login_in_driver):
    driver = login_in_driver

    WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))

    productos = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )

    productos[0].find_element(By.TAG_NAME, "button").click()

    badge = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )

    assert badge.text == "1", f"Se esperaba 1 ítem en el carrito, pero apareció {badge.text}"
    print("✅ Test OK: el producto se agregó correctamente al carrito.")
