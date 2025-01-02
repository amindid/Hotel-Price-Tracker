import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def scrape_booking(city, checkin, checkout, nb_adults, nb_rooms, nb_children):
    driver = webdriver.Chrome()
    driver.get(f"https://www.booking.com/searchresults.html?ss={city}&checkin={checkin}&checkout={checkout}&group_adults={nb_adults}&no_rooms={nb_rooms}&group_children={nb_children}")
    # wait for the sign in dismiss button to appear
    close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Dismiss sign-in')]"))
    )
    # Click the close button
    close_button.click()
    hotels = []  # List to store hotel information

    scroll_height = 0
    while True:
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")
        scroll_height += 300
        time.sleep(0.05)
        current_height = driver.execute_script("return window.pageYOffset;")
        total_height = driver.execute_script("return document.body.scrollHeight;")
        
        try:
            # Click on "Load more results" if the button exists
            load_more_button = driver.find_element(By.XPATH, "//*[span[text()='Load more results']]")
            load_more_button.click()
            time.sleep(2)
        except Exception:
            if current_height + 1300 >= total_height:
                break
            else:
                continue

    # Extract information from property cards
    hotel_elements = driver.find_elements(By.XPATH, "//div[@data-testid='property-card']")
    for hotel_element in hotel_elements:
        try:
            # Extract hotel name
            hotel_name = hotel_element.find_element(By.XPATH, ".//div[@data-testid='title']").text
            
            # Extract location
            location = hotel_element.find_element(By.XPATH, ".//span[@data-testid='address']").text
            
            # Extract review score and count
            review_info = hotel_element.find_element(By.XPATH, ".//div[@data-testid='review-score']").text if hotel_element.find_elements(By.XPATH, ".//div[@data-testid='review-score']") else "N/A"
            review_details = review_info.split('\n')
            
            # Extract price
            price = hotel_element.find_element(By.XPATH, ".//span[@data-testid='price-and-discounted-price']").text if hotel_element.find_elements(By.XPATH, ".//span[@data-testid='price-and-discounted-price']") else "N/A"
            
            # Extract details
            details = hotel_element.find_element(By.XPATH, ".//div[@data-testid='recommended-units']").text if hotel_element.find_elements(By.XPATH, ".//div[@data-testid='recommended-units']") else "N/A"
            details = details.split("\n")
            # Add the extracted data to the list
            hotels.append({
                "name": hotel_name,
                "location": location,
                "price": price,
                "review_score": review_info if review_info == "N/A" else review_details[0],
                "review_count": review_info if review_info == "N/A" else review_details[3],
                "details": details if len(details) != 0 else "N/A"
            })

        except Exception as e:
            print(f"Error extracting data for a hotel: {e}")
            continue  # Skip hotels with issues

    driver.quit()
    with open('../frontend/hotel-tracker/public/hotels_list.json', 'w', encoding='utf-8') as json_file:
        json.dump(hotels, json_file, ensure_ascii=False, indent=4)

    print(f"Scraped {len(hotels)} hotels from Booking.com for {city}.")

# Example usage
checkin = "2025-01-05"
checkout = "2025-01-06"
city = "essaouira"
nb_adults = "2"
nb_children = "0"
nb_rooms = "1"
scrape_booking(city, checkin, checkout, nb_adults, nb_rooms, nb_children)
