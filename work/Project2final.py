import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Edge(options=options)

CSV_FILE = "slot_availability.csv"
QUERIES = {
    "theory": "index",
    "practical": "practical",
    "test": "test"
}

os.makedirs("data", exist_ok=True)

def wait_for_manual_login():
    driver.get("https://booking.bbdc.sg/#/login")
    print("Please log in manually, then press Enter to continue...")
    input("Press Enter after logging in...")
    print("Login detected! Starting data scraping...")

def scrape_and_update():
    while True:
        data_dict = {"Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
        
        for category, query in QUERIES.items():
            url = f"https://booking.bbdc.sg/#/booking/{query}"
            driver.get(url)
            time.sleep(3)
            
            slots = driver.find_elements(By.CLASS_NAME, "row")
            available_slots = 0
            available_buttons = []
            
            for slot in slots:
                buttons = slot.find_elements(By.TAG_NAME, "button")
                button_texts = [button.text.strip().lower() for button in buttons]
                
                if "book slot" in button_texts:
                    available_slots += 1
                    available_buttons.append([button.text for button in buttons if "book slot" in button.text.lower()])
            
            print(f"{category.capitalize()} - Available Slots: {available_slots}")
            print(f"Available Buttons: {available_buttons}")
            
            data_dict[f"{category}_available_slots"] = available_slots
            data_dict[f"{category}_available_buttons"] = available_buttons
        
        df = pd.DataFrame([data_dict])
        if os.path.exists(CSV_FILE):
            df.to_csv(CSV_FILE, mode="a", index=False, header=False)
        else:
            df.to_csv(CSV_FILE, index=False)
        
        print("Updated slot availability in CSV.")
        time.sleep(30)

try:
    wait_for_manual_login()
    scrape_and_update()
finally:
    driver.quit()
