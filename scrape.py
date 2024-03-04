from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# CRC Website for Wait Times
url = "https://live.waitz.io/4vxie66a29ct"
_seen_classes = ["css-1tglk97", "css-1qumdbr"]
path = "/usr/local/bin/geckodriver" # User specific
options = Options()
options.add_argument("--headless")

def get_busy_object():
    """Scrapes the live capacity data using Firefox WebDriver and returns the percent full.
    If the waitz.io site indicates the CRC is closed, a detected close will occur and percent_full will be set to -1."""

    # Use Selenium to scrape the page once it has fully loaded
    driver = webdriver.Firefox(options=options, service=Service(path))
    print("Headless Firefox Loaded")
    driver.get(url)
    valid = True
    # Should change to with ?
    try:
        # Have to do this because they randomize class names
        _wait_till_loaded = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        )
        # Will work so long as structure remains the same
        fitness_center_closed_element = driver.find_elements(By.TAG_NAME, 'p')[0]
        if str(fitness_center_closed_element.get_attribute('innerHTML')).split(" ")[0] == "Closed":
            print("Detected Close")
            valid = False
        fitness_center_busy_element = driver.find_elements(By.TAG_NAME, 'p')[1]
    except Exception as error:
        valid = False
        print("Error: most likely the page never loaded or the page structure changed")
        print(error)
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

    print(integer_busy)
    return integer_busy
