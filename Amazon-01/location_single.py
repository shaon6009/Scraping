from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Edge()
query= "laptop"
driver.get("https://www.amazon.in/s?k=laptop&crid=3G8Q4FS48CVI&sprefix={query}%2Caps%2C303&ref=nb_sb_noss_2")

elem= driver.find_element(By.CLASS_NAME, "puisg-col-inner")
print(elem.text)

time.sleep(5)
driver.close()