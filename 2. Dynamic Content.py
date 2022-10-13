from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup

By.CL
def format_price(price):
    return float(price.split("$")[1].replace(",", ""))


def get_5_stars_percentage(item):
    ratings = item.find_element(By.XPATH, ".//div[@class='s-item__reviews']/a")
    ratings_link = ratings.get_attribute("href")
    ratings_response = requests.get(ratings_link)
    ratings_source_code = ratings_response.text
    ratings_soup = BeautifulSoup(ratings_source_code, "html.parser")
    five_stars_elem = ratings_soup.find("li", {"class": "review--item"})
    nb_five_stars = int(five_stars_elem.find("span").text)

    stars_elems = ratings_soup.find_all("li", {"class": "review--item"})
    nb_stars = [int(star_elem.find("span").text) for star_elem in stars_elems]
    total_nb_stars = sum(nb_stars)
    percentage_five_stars = round(nb_five_stars / total_nb_stars, 2) * 100
    return percentage_five_stars


def check_item_is_a_bid(item):
    try:
        item.find_element(By.XPATH, ".//span[@class='s-item__bids s-item__bidCount']")
        return True
    except:
        return False


def buy_item(item):
    link = item.find_element(By.XPATH, ".//a[@class='s-item__link']")
    link.click()
    # Buy actions


if __name__ == "__main__":
    driver_path = "./chromedriver.exe"
    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    options = webdriver.ChromeOptions()
    options.binary_location = brave_path
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    keywords = "It Stephen King"
    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={}&_sacat=0&LH_TitleDesc=0&_odkw={}".format(keywords, keywords)
    driver.get(url)

    items = driver.find_elements(By.XPATH, "//li[@class='s-item s-item__pl-on-bottom s-item--watch-at-corner']")
    items_to_buy = []
    for item in items:
        price_element = item.find_element(By.XPATH, ".//span[@class='s-item__price']")
        price = format_price(price_element.text)

        if price < 30:
            try:
                percentage_5_stars = get_5_stars_percentage(item)
                if percentage_5_stars > 40:
                    is_a_bid = check_item_is_a_bid(item)
                    if not is_a_bid:
                        items_to_buy.append(item)
                        item.send_keys(Keys.CONTROL + Keys.RETURN)
                        WebDriverWait(driver, 10)
                        WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.ID, "btn_result")))
            except:
                pass

    buy_item(items_to_buy[0])
    driver.page_source
    soup = BeautifulSoup(driver.page_source, "html.parser")
    reviews = soup.find("div", {"class": "s-item__reviews"})
    driver.quit()
