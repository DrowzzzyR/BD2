import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from test_auth import auth
from test_register import register
from test_product_and_supply import product_and_supply
def test_main():
   options = webdriver.ChromeOptions()
   options.add_experimental_option("excludeSwitches", ["enable-logging"])
   options.add_argument("--no-sandbox")
   
   driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

   driver.maximize_window()
   driver.implicitly_wait(60)
   
   driver.get("http://192.168.1.3:8000/")

   result_register = register(driver=driver)
   assert result_register == True, "Ошибка регистрации."
   result_auth = auth(driver=driver)
   assert result_auth == True, "Ошибка аутентификации."
   result_product_and_supply = product_and_supply(driver=driver)
   assert result_product_and_supply == True, "Ошибка при добавлении продукта/поставки."

   driver.close()
   driver.quit()
