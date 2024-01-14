from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def auth(driver):
    result_login = login(driver)
    if not result_login:
        return False
    
    return True

def login(driver):
    try:
        driver.get("http://192.168.1.2:8000/auth/login")
        input_username = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/form/input[1]"))
        )
        input_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/form/input[2]"))
        )

        login = 'test_user'
        password = 'test_pass'

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
        
        print("Попытка выполнить click()")
        button.click()
        print("click() выполнен успешно")

        wait = WebDriverWait(driver, 10)
        li_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/main/ul/li")))
        if "Вы успешно аутентифицированы." in li_element.text:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
