from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import json

driver = webdriver.Firefox(service=Service('/snap/bin/geckodriver'))
driver.implicitly_wait(10)
driver.get("https://changeofmajor.uci.edu/school-of-information-and-computer-sciences/#cgs")

with open('departments_requirements.json', 'w') as file:
    json.dump([
        {
            'department_name': table.find_element(By.CSS_SELECTOR, "tbody tr:first-child th.dept-name").text,
            'requirements': {cells[0].text: cells[1].text for cells in [row.find_elements(By.TAG_NAME, "td") for row in table.find_elements(By.CSS_SELECTOR, "tbody tr:nth-child(n+3)")] }        } for table in driver.find_elements(By.CSS_SELECTOR, "table")
    ], file, indent=4)

driver.quit()