from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

links = {'S02E08': 'https://southpark.fandom.com/wiki/Summer_Sucks/Script',
         'S02E10': 'https://southpark.fandom.com/wiki/Chickenpox/Script',
         'S02E12': 'https://southpark.fandom.com/wiki/Clubhouses/Script',
         'S03E06': 'https://southpark.fandom.com/wiki/Sexual_Harassment_Panda/Script',
         'S04E02': 'https://southpark.fandom.com/wiki/Cartman%27s_Silly_Hate_Crime_2000/Script',
         'S05E09': 'https://southpark.fandom.com/wiki/Osama_bin_Laden_Has_Farty_Pants/Script',
         'S07E14': 'https://southpark.fandom.com/wiki/Raisins/Script',
         'S09E10': 'https://southpark.fandom.com/wiki/Follow_That_Egg!/Script',
         'S10E06': 'https://southpark.fandom.com/wiki/ManBearPig/Script',
         '': '',
         '': '',
         '': ''
        }