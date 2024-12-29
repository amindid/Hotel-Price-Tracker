import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv

def scrape_booking(city, checkin, checkout):
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.booking.com/searchresults.html?ss={city}&checkin={checkin}&checkout={checkout}")
    
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
            # review_score = review_score.split()[1] or "N/A"
            # review_count = review_count.split()[1] or "N/A"
            # review_score = review_score.split()
            # review_count = hotel_element.find_element(By.XPATH, ".//div[@data-testid='review-score']/span[2]").text if hotel_element.find_elements(By.XPATH, ".//div[@data-testid='review-score']/span[2]") else "N/A"
            
            # Extract price
            price = hotel_element.find_element(By.XPATH, ".//span[@data-testid='price-and-discounted-price']").text if hotel_element.find_elements(By.XPATH, ".//span[@data-testid='price-and-discounted-price']") else "N/A"
            
            # Extract amenities
            # amenities = [amenity.text for amenity in hotel_element.find_elements(By.XPATH, ".//div[@data-testid='amenities']")]

            # Add the extracted data to the list
            hotels.append({
                "name": hotel_name,
                "location": location,
                "price": price,
                "review_score": review_details[0] or "N/A",
                "review_count": review_details[3] or "N/A",
                # "amenities": amenities
            })

        except Exception as e:
            print(f"Error extracting data for a hotel: {e}")
            continue  # Skip hotels with issues

    driver.quit()

    # Save hotels to a CSV file
    with open(f"{city}_hotels_overview.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "location", "price", "review_score", "review_count"])
        # writer = csv.DictWriter(file, fieldnames=["name", "location", "review_score", "review_count", "price", "amenities"])
        writer.writeheader()
        for hotel in hotels:
            writer.writerow({
                "name": hotel["name"],
                "location": hotel["location"],
                "price": hotel["price"],
                "review_score": hotel["review_score"],
                "review_count": hotel["review_count"],
            })

    print(f"Scraped {len(hotels)} hotels from Booking.com for {city}.")

# Example usage
checkin = "2025-01-01"
checkout = "2025-01-02"
city = "essaouira"
scrape_booking(city, checkin, checkout)
