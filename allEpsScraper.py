from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

table_xpath = '/html/body/div[4]/div[3]/div[2]/main/div[3]/div[1]/div[1]/table[1]'
episodes_xpath = '//*[@id="gallery-0"]'

# season = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen', 'Twenty', 'Twenty-One', 'Twenty-Two', 'Twenty-Three', 'Twenty-Four', 'Twenty-Five', 'Twenty-Six']
season = ['Seventeen', 'Eighteen', 'Nineteen', 'Twenty', 'Twenty-One', 'Twenty-Two', 'Twenty-Three', 'Twenty-Four', 'Twenty-Five', 'Twenty-Six']
time.sleep(2)
driver = webdriver.Firefox()

# Scrape every season
for sn, s in enumerate(season):
    print(f"Scraping season {s}")
    url = f"https://southpark.fandom.com/wiki/Portal:Scripts/Season_{s}"
    driver.get(url)
    time.sleep(3)
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
        print(f"Scraping Episode {i}")
        driver.get(url)
        time.sleep(7)
        episodes = driver.find_element(By.XPATH, episodes_xpath)
        eps = episodes.find_elements(By.CLASS_NAME, "link-internal")
        eps[i].click()
        time.sleep(7)

        # Scrapes episode
        ep_script = ""
        try:
            table = driver.find_element(By.XPATH, table_xpath)
        except Exception as e:
            print(f"Season {s} episode i failed")
            continue
        for row in table.find_elements(By.TAG_NAME, 'tr'):
            for k, col in enumerate(row.find_elements(By.TAG_NAME, 'td')):
                if len(row.find_elements(By.TAG_NAME, 'td')) == 1:
                    ep_script += col.text + "\n"
                else:
                    if k == 0:
                        if col.text == "":
                            brackets = True
                        else:
                            ep_script += col.text.upper() + "\n"
                    elif k == 1:
                        if brackets:
                            ep_script += f"[{col.text}]\n"
                            brackets = False
                        else:
                            ep_script += col.text + "\n"

        # text_file = open(f"S{str(sn+1).zfill(2)}E{str(i+1).zfill(2)}.txt", "w")
        text_file = open(f"S{str(sn+17).zfill(2)}E{str(i+1).zfill(2)}.txt", "w")
        text_file.write(ep_script)
        text_file.close()


