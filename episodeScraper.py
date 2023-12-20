from selenium import webdriver
from selenium.webdriver.common.by import By
import time

urls = {'S02E08': 'https://southpark.fandom.com/wiki/Summer_Sucks/Script',
         'S02E10': 'https://southpark.fandom.com/wiki/Chickenpox/Script',
         'S02E12': 'https://southpark.fandom.com/wiki/Clubhouses/Script',
         'S03E06': 'https://southpark.fandom.com/wiki/Sexual_Harassment_Panda/Script',
         'S04E02': 'https://southpark.fandom.com/wiki/Cartman%27s_Silly_Hate_Crime_2000/Script',
         'S05E09': 'https://southpark.fandom.com/wiki/Osama_bin_Laden_Has_Farty_Pants/Script',
         'S07E14': 'https://southpark.fandom.com/wiki/Raisins/Script',
         'S09E10': 'https://southpark.fandom.com/wiki/Follow_That_Egg!/Script',
         'S10E06': 'https://southpark.fandom.com/wiki/ManBearPig/Script',
         'S12E13': 'https://southpark.fandom.com/wiki/Elementary_School_Musical/Script',
         'S13E02': 'https://southpark.fandom.com/wiki/The_Coon/Script',
         'S13E12': 'https://southpark.fandom.com/wiki/The_F_Word/Script',
         'S14E06': 'https://southpark.fandom.com/wiki/201/Script',
         'S14E09': 'https://southpark.fandom.com/wiki/It%27s_a_Jersey_Thing/Script',
         'S15E03': 'https://southpark.fandom.com/wiki/Royal_Pudding/Script',
         'S20E19': 'https://southpark.fandom.com/wiki/Not_Funny/Script',
         'S21E07': 'https://southpark.fandom.com/wiki/Doubling_Down/Script',
         'S22E03': 'https://southpark.fandom.com/wiki/The_Problem_with_a_Poo/Script'}

driver = webdriver.Firefox()
time.sleep(3)
for episode in urls.keys():
    driver.get(urls[episode])
    # Accept cookies
    try:
        accept_cookies = driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div[2]/div[2]')
        accept_cookies.click()
    except Exception as e:
        print("No cookies to accepts")
    # Scrapes episode
    ep_script = ""
    try:
        table = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div[2]/main/div[3]/div[1]/div[1]/table[1]')
    except Exception as e:
        print(f"{episode} failed")
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
    text_file = open(f"{episode}.txt", "w")
    text_file.write(ep_script)
    text_file.close()
