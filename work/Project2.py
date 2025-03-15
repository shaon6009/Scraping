import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BOOKING_URLS = {
    "theory": "https://booking.bbdc.sg/#/booking/index",
    "practical": "https://booking.bbdc.sg/#/booking/practical",
    "test": "https://booking.bbdc.sg/#/booking/test"
}

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

def scrape_and_save():
    all_data = []
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    for category, url in BOOKING_URLS.items():
        response = session.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data for {category}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        slots = soup.find_all("div", class_="row")

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

    df = pd.DataFrame(all_data)
    df.to_csv("slot_details.csv", index=False)
    print(f"✅ Updated full slot details in CSV.")

scrape_and_save()
