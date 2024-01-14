from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def register(driver):
    if not register(driver=driver):
        return False
    return True

def register(driver):
    try:
        driver.get("http://127.0.0.1:5000/auth/register")
        input_username = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/form/input[1]"))
        )
        input_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/form/input[2]"))
        )

        login = '33344'
        password = '33344'

        data = {
            'login': login,
            'password': password,
        }
        print(data)

        input_username.send_keys(data['login'])
        input_password.send_keys(data['password'])

        button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/form/button"))
        )
        
        button.click()

        wait = WebDriverWait(driver, 10)
        li_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/ul/li")))
        if "Регистрация успешно завершена." in li_element.text:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return False