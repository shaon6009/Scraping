import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup WebDriver
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Edge(options=options)

# Category mapping
QUERIES = {
    "theory": "index",
    "practical": "practical",
    "test": "test"
}

# Get user input
print("Welcome to BBDC Slot Booker!")
category_input = input("What slot do you want to book? (theory/practical/test): ").strip().lower()

if category_input != "practical":
    print("This version supports only 'practical' for now.")
    driver.quit()
    exit()

booking_date = input("Enter preferred date (YYYY-MM-DD): ").strip()
booking_time = input("Enter preferred time (e.g., 09:00 AM): ").strip()

# Manual login
def wait_for_manual_login():
    driver.get("https://booking.bbdc.sg/#/login")
    print("Please log in manually, then press Enter to continue...")
    input("Press Enter after logging in...")
    print("Login detected! Starting automation...")

# Booking logic
def attempt_practical_booking():
    driver.get("https://booking.bbdc.sg/#/booking/practical")
    time.sleep(3)

    print("Checking for available 'practical' slots...")

    try:
        # Wait for all buttons to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button"))
        )

        # Check all buttons and click the one with "Book Slot"
        buttons = driver.find_elements(By.CSS_SELECTOR, "button")
        clicked = False
        for btn in buttons:
            if btn.text.strip().lower() == "book slot":
                print("✅ Book Slot button found!")
                btn.click()
                clicked = True
                break

        if not clicked:
            print("No Book Slot button available. Retrying in 30 seconds...")
            return False

        # Wait for next page to load
        time.sleep(2)

        # Select "Book Without Instructor"
        no_instr_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Book Without Instructor')]")
        no_instr_btn.click()
        print("👉 Selected 'Book Without Instructor'")
        time.sleep(2)

        # Select date
        calendar_btn = driver.find_element(By.XPATH, f"//td[@aria-label='{booking_date}']")
        calendar_btn.click()
        print(f"📅 Selected date: {booking_date}")
        time.sleep(2)

        # Select time
        time_slots = driver.find_elements(By.XPATH, f"//div[contains(text(), '{booking_time}')]")
        if not time_slots:
            print(f"❌ No time slot found for {booking_time}. Retrying...")
            return False
        time_slots[0].click()
        print(f"⏰ Selected time slot: {booking_time}")
        time.sleep(1)

        # Click "Next"
        next_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
        next_btn.click()
        print("➡️ Pressed Next")
        time.sleep(2)

        # Confirm Page: Click Confirm
        confirm_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm')]")
        confirm_btn.click()
        print("✅ Pressed Confirm")
        time.sleep(2)

        # CAPTCHA
        print("⚠️ CAPTCHA detected. Please solve it manually.")
        input("After solving CAPTCHA and confirming booking, press Enter to continue...")

        print("🎉 Booking attempt complete! Exiting.")
        return True

    except Exception as e:
        print(f"⚠️ Error: {e}")
        return False

# Run the bot
try:
    wait_for_manual_login()
    success = False
    while not success:
        success = attempt_practical_booking()
        if not success:
            print("🔁 Retrying in 30 seconds...\n")
            time.sleep(30)
finally:
    driver.quit()
