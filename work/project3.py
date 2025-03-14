from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import csv

driver = webdriver.Edge()

queries = ["index", "practical", "test"]

os.makedirs("data", exist_ok=True)

file_counter = 0
csv_file = "data2.csv"

with open(csv_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Query", "File Name", "HTML Content"])

    try:
        for i in range(20):
            for query in queries:
                url = f"https://booking.bbdc.sg/#/booking/{query}"
                driver.get(url)
                time.sleep(3)

                elems = driver.find_elements(By.CLASS_NAME, "row")

                for elem in elems:
                    d = elem.get_attribute("outerHTML")
                    filename = f"data/{query}_{file_counter}.txt"
                    with open(filename, "w", encoding="utf-8") as txt_file:
                        txt_file.write(d)
                    writer.writerow([query, filename, d])
                    file_counter += 1
            
            time.sleep(5)
    
    finally:
        driver.quit()
