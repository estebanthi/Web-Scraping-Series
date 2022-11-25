import requests
from bs4 import BeautifulSoup
import yaml

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_with_requests():
    url = "https://www.pianostreet.com/amember/login"
    data = {
        "amember_login": yaml.safe_load(open("config.yml"))["user"],
        "amember_pass": yaml.safe_load(open("config.yml"))["pass"],
    }

    with requests.Session() as s:
        r = s.post(url, data=data, allow_redirects=False)
        print(r.status_code)

        r = s.get("https://www.pianostreet.com/amember/profile")
        soup = BeautifulSoup(r.content, "html.parser")
        print(soup.find("div", {"class": "am-form"}).text)


def login_with_selenium():
    driver_path = "./chromedriver.exe"
    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    options = webdriver.ChromeOptions()
    options.binary_location = brave_path
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    driver.get("https://www.pianostreet.com/amember/login")
    driver.find_element(By.NAME, "amember_login").send_keys(yaml.safe_load(open("config.yml"))["user"])
    driver.find_element(By.NAME, "amember_pass").send_keys(yaml.safe_load(open("config.yml"))["pass"])
    driver.find_element(By.NAME, "login").submit()

    WebDriverWait(driver, 10).until(EC.url_contains("https://www.pianostreet.com/amember/member"))
    driver.get("https://www.pianostreet.com/amember/profile")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "am-form")))
    print(driver.find_element(By.CLASS_NAME, "am-form").text)

    name = driver.find_element(By.ID, "name_f").get_attribute("value")
    print(name)


if __name__ == "__main__":
    login_with_requests()
    login_with_selenium()
