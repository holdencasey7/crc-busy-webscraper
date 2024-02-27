from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

url = "https://live.waitz.io/4vxie66a29ct"
fitness_center_class_name = "css-1tglk97"

driver = webdriver.Firefox()
driver.get(url)
try:
    fitness_center_busy_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, fitness_center_class_name))
    )
except:
    print("Error: most likely the page never loaded or the class name changed")
finally:
    current_time = datetime.datetime.now()

fitness_center_busy_string = fitness_center_busy_element.get_attribute('innerHTML')
print(fitness_center_busy_string)
print(current_time)
driver.quit()