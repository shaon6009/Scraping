import time
import os
import easyocr
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

reader = easyocr.Reader(['en'])
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Edge(options=options)

USERNAME = "697M02011996"
PASSWORD = "649396"
CSV_FILE = "slot_availability.csv"
QUERIES = {
    "theory": "index",
    "practical": "practical",
    "test": "test"
}

os.makedirs("data", exist_ok=True)

def login():
    driver.get("https://booking.bbdc.sg/#/login")
    wait = WebDriverWait(driver, 10)
    try:
        user_input = wait.until(EC.presence_of_element_located((By.ID, "loginId")))
        pass_input = driver.find_element(By.ID, "password")
        user_input.send_keys(USERNAME)
        pass_input.send_keys(PASSWORD)
        captcha_img = driver.find_element(By.ID, "captchaImage")
        captcha_img.screenshot("captcha.png")
        captcha_text = solve_captcha("captcha.png")
        print(f"CAPTCHA Solved: {captcha_text}")
        captcha_input = driver.find_element(By.ID, "captchaInput")
        captcha_input.send_keys(captcha_text)
        captcha_input.send_keys(Keys.RETURN)
        time.sleep(5)
        print("Login successful!")
    except Exception as e:
        print(f"Login failed: {e}")

def solve_captcha(image_path):
    result = reader.readtext(image_path, detail=0)
    return result[0] if result else ""

def scrape_and_update():
    while True:
        data_dict = {"Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
        for category, query in QUERIES.items():
            url = f"https://booking.bbdc.sg/#/booking/{query}"
            driver.get(url)
            time.sleep(3)
            elems = driver.find_elements(By.CLASS_NAME, "row")
            total_slots = len(elems)
            available_slots = 0
            for elem in elems:
                text = elem.text.lower()
                if "booked" in text:
                    continue
                elif "completed" in text:
                    continue
                else:
                    available_slots += 1
            print(f"{category.capitalize()} - Total: {total_slots}, Available: {available_slots}")
            data_dict[f"{category}_total_slots"] = total_slots
            data_dict[f"{category}_available_slots"] = available_slots
            data_dict[f"{category}_status"] = "Available" if available_slots > 0 else "Not Available"
        df = pd.DataFrame([data_dict])
        if os.path.exists(CSV_FILE):
            df.to_csv(CSV_FILE, mode="a", index=False, header=False)
        else:
            df.to_csv(CSV_FILE, index=False)
        print("Updated slot availability in CSV.")
        time.sleep(60)

try:
    login()
    scrape_and_update()
finally:
    driver.quit()
