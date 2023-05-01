from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

table_xpath = '/html/body/div[4]/div[3]/div[2]/main/div[3]/div[1]/div[1]/table[1]'
episodes_xpath = '//*[@id="gallery-0"]'

season = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen', 'Twenty', 'Twenty-One', 'Twenty-Two', 'Twenty-Three', 'Twenty-Four', 'Twenty-Five', 'Twenty-Six']

driver = webdriver.Firefox()

# Scrape every season
for s in season:
    url = f"https://southpark.fandom.com/wiki/Portal:Scripts/Season_{s}"
    driver.get(url)
    time.sleep(1)
    # Accept cookies
    try:
        accept_cookies = driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div[2]/div[2]')
        accept_cookies.click()
    except Exception as e:
        print("No cookies to accepts")

    # Find list of episodes.
    episodes = driver.find_element(By.XPATH, episodes_xpath)
    eps = episodes.find_elements(By.CLASS_NAME, "link-internal")
    # Click every episode.
    for i in range(len(eps)):
        driver.get(url)
        time.sleep(3)
        episodes = driver.find_element(By.XPATH, episodes_xpath)
        eps = episodes.find_elements(By.CLASS_NAME, "link-internal")
        eps[i].click()
        time.sleep(10)


