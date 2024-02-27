from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import json
import sqlite3

# CRC Website for Wait Times
url = "https://live.waitz.io/4vxie66a29ct"
fitness_center_class_name = "css-1tglk97"

def get_busy_object():
    # Use Selenium to scrape the page once it has fully loaded
    driver = webdriver.Firefox()
    driver.get(url)
    try:
        fitness_center_busy_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, fitness_center_class_name))
        )
    except:
        print("Error: most likely the page never loaded or the class name changed")
    finally:
        fitness_center_busy_string = str(fitness_center_busy_element.get_attribute('innerHTML'))
        driver.quit()
        current_time = datetime.datetime.now()

    # Parse the element to get busy description and full percentage
    split_fitness_center_busy_string = fitness_center_busy_string.rsplit(' ', 1)
    percent_busy = split_fitness_center_busy_string[1]
    integer_busy = int(percent_busy[:-1])

    # Combine current time and busy into single object
    busy_at_time = {
        "weekday": current_time.weekday(),
        "hour": current_time.hour,
        "minutes": current_time.minute,
        "busy": integer_busy
    }
    
    return busy_at_time

