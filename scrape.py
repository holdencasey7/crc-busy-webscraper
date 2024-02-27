from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

# CRC Website for Wait Times
url = "https://live.waitz.io/4vxie66a29ct"

def get_busy_object():
    # Use Selenium to scrape the page once it has fully loaded
    driver = webdriver.Firefox()
    driver.get(url)
    valid = True
    try:
        # Have to do this because they randomize class names
        wait_till_loaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        )
        # Will work so long as structure remains the same
        fitness_center_busy_element = driver.find_elements(By.TAG_NAME, 'p')[1]
    except:
        valid = False
        print("Error: most likely the page never loaded or the class name changed")
    finally:
        if valid:
            fitness_center_busy_string = str(fitness_center_busy_element.get_attribute('innerHTML'))

            # Parse the element to get busy description and full percentage
            split_fitness_center_busy_string = fitness_center_busy_string.rsplit(' ', 1)
            percent_busy = split_fitness_center_busy_string[1]
            integer_busy = int(percent_busy[:-1])
        else:
            integer_busy = -1

        driver.quit()
        current_time = datetime.datetime.now()

    # Combine current time and busy into single object
    busy_at_time = {
        "weekday": current_time.weekday(),
        "hour": current_time.hour,
        "minutes": current_time.minute,
        "busy": integer_busy
    }
    print(busy_at_time)
    return busy_at_time
