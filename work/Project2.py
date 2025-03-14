import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

LOGIN_URL = "https://booking.bbdc.sg/login"
BOOKING_URLS = {
    "theory": "https://booking.bbdc.sg/#/booking/index",
    "practical": "https://booking.bbdc.sg/#/booking/practical",
    "test": "https://booking.bbdc.sg/#/booking/test"
}

# Your session headers (add User-Agent or other required headers to prevent blocking)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Your login credentials (you will need to manually log in for security)
USERNAME = "697M02011996"
PASSWORD = "649396"

# Create a session to maintain login state
session = requests.Session()

# Start by logging in to the website (if necessary)
def login():
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }

    # Send a POST request to log in
    response = session.post(LOGIN_URL, data=login_data, headers=headers)
    if response.status_code == 200:
        print("Login successful")
    else:
        print("Login failed!")
        return False
    return True

# Scrape the slot availability data and save it to a CSV
def scrape_and_save():
    all_data = []
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Capture timestamp

    for category, url in BOOKING_URLS.items():
        response = session.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data for {category}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape the available slots (You need to inspect the page and find the relevant HTML structure)
        slots = soup.find_all("div", class_="row")  # Modify this selector based on actual structure

        for slot in slots:
            details = slot.get_text(strip=True).split("\n")
            if len(details) >= 2:
                slot_data = {
                    "Timestamp": timestamp,
                    "Category": category.capitalize(),
                    "Date": details[0],
                    "Time": details[1],
                    "Instructor": details[2] if len(details) > 2 else "N/A",
                    "Status": "Booked" if "booked" in details[-1].lower() else "Available"
                }
                all_data.append(slot_data)

    # Save to CSV file
    df = pd.DataFrame(all_data)
    df.to_csv("slot_details.csv", index=False)
    print(f"✅ Updated full slot details in CSV.")

# Run the process
if login():
    scrape_and_save()
