
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import numpy as np

# Driver setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://store.steampowered.com/")
driver.implicitly_wait(5)
driver.maximize_window()

cookies = WebDriverWait(driver,20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#rejectAllButton')))
cookies.click()
# Changing the language Polish -> English
lang = WebDriverWait(driver,20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'span#language_pulldown')))
lang.click()
english = WebDriverWait(driver,20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '[href="?l=english"]')))
english.click()
time.sleep(5)
bestsellers1 = WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#tab_topsellers_content_trigger')))
bestsellers1.click()
bestsellers2 = WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="tab_topsellers_content"]/div[2]/span[1]/a[2]')))
bestsellers2.click()


def scroll_down():
    """Scroll down to the end of the page"""
    ActionChains(driver).send_keys(Keys.END).perform()

# Loading more page content, range may vary if additional filters are added to the page's search
for _ in range(200):
    scroll_down()
    time.sleep(2)

game_rows = driver.find_elements(By.CSS_SELECTOR, 'a.search_result_row.ds_collapse_flag')
titles = []
dates = []
prices = []
for row in game_rows:
    title_element = row.find_element(By.CSS_SELECTOR, 'span.title')
    date_element = row.find_element(By.CSS_SELECTOR, 'div.col.search_released.responsive_secondrow')
    try:
        price_element = row.find_element(By.CSS_SELECTOR, 'div.discount_final_price')
    except NoSuchElementException:
        None

    title = title_element.text if title_element else np.NaN
    release_date = date_element.text if date_element else np.NaN
    price = price_element.text if price_element else np.NaN

    titles.append(title)
    dates.append(release_date)
    prices.append(price)

# Check if all items have been imported equally
if len(titles) == len(dates) == len(prices):

    steam_games = pd.DataFrame({'title':titles,
                                'release_date':dates,
                                'current_price':prices})
    print(f"Scraped games count: {steam_games.shape[0]}")
    steam_games.to_csv('steam_games.csv')
