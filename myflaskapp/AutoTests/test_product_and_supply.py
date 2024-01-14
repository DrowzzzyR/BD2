from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def product_and_supply(driver):
    if not product_and_supply_create(driver=driver):
        return False
    return True

def product_and_supply_create(driver):
    try:
        driver.find_element(By.XPATH, "/html/body/header/nav/a[1]").click()

        Product_Name = "agusha"
        Description = "nyama-nyama"
        Price = "100500"
        Product_ID = "1"
        Quantity = "333"
        data = {
            'Product_Name': Product_Name,
            'Description': Description,
            'Price': Price,
            'Product_ID': Product_ID,
            'Quantity': Quantity
        }

        input_Product_Name = driver.find_element(By.XPATH, "/html/body/form[1]/input[1]")
        input_desc = driver.find_element(By.XPATH, "/html/body/form[1]/textarea")
        input_price = driver.find_element(By.XPATH, "/html/body/form[1]/input[2]")

        input_Product_Name.send_keys(data['Product_Name'])
        input_desc.send_keys(data['Description'])
        input_price.send_keys(data['Price'])

        driver.find_element(By.XPATH, "/html/body/form[1]/button").click()

        wait = WebDriverWait(driver, 10)
        li_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/ul/li")))
        if "Product added successfully" in li_element.text:
            driver.get("http://192.168.1.2:8000/dashboard")
            input_Product_ID = driver.find_element(By.XPATH, "/html/body/form[2]/input[1]")
            input_quantity = driver.find_element(By.XPATH, "/html/body/form[2]/input[2]")
            input_Product_ID.send_keys(data['Product_ID'])
            input_quantity.send_keys(data['Quantity'])
            date_field = driver.find_element(By.XPATH, "/html/body/form[2]/input[3]")  
            date_value = "01-09-1939"  
            date_field.send_keys(date_value)
            driver.find_element(By.XPATH, "/html/body/form[2]/button").click()
            wait = WebDriverWait(driver, 10)
            li_element1 = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/ul/li")))
            if "Supply added successfully" in li_element1.text:
                return True
            else:
                return False
        else:
            return False
    except:
        return False