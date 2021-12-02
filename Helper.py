from selenium import webdriver
from selenium.webdriver.common.by import By


from selenium.webdriver.chrome.options import Options
import time



def get_login_token():
    print("GETTING LOGIN TOKEN...")
    options = Options()
    options.headless = True
    login_token = ""
    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
    driver.get("https://maverikstudio.vn/account/login")
    time.sleep(2)
    ele_wait = driver.find_element(By.NAME, "g-recaptcha-response")
    login_token = ele_wait.get_attribute("value")
    driver.close()
    return login_token