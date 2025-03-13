from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Edge()
query = "laptop"
file = 0

for i in range(20):
    driver.get(f"https://www.amazon.in/s?k={query}")
    elems = driver.find_elements(By.CLASS_NAME, "puisg-col-inner")
    
    print(f"{len(elems)} items found")
    
    for elem in elems:
        d = elem.get_attribute("outerHTML")
        with open(f"data/{query}_{file}.txt", "w", encoding="utf-8") as f:
            f.write(d)
        print(elem.text)
        file += 1
    
    time.sleep(5)

driver.close()