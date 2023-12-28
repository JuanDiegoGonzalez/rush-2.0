# Imports
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# WebDriver config
options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options, executable_path='../driver/chromedriver.exe')
timeout_in_seconds = 5

# Data retrieving
soup = ""
try:
    browser.get("https://www.betclan.com/es/predicciones-de-futbol-de-hoy/")
    WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.ID, 'betclanfilter')))
    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
except TimeoutException:
    print("I give up...")

# Data formatting
data = str(soup).split("betclanfilter")[1]
data = data.split("portlet box blue-sharp")[0]
lines = data.split("\n")

# Matches
text = lines[1].split("title")
countries = []
matches = []
links = []
for i in text[1:]:
    if i.__contains__("bccountry"):
        pass
    elif i.__contains__("bcleaguetime"):
        countries.append({"CountryName": i.split("\"")[1][:-13], "NumMatches": 0})
    else:
        parts = i.split(",")
        matches.append(parts[0][2:-12])
        links.append(parts[5][7:-1])
        countries[-1]["NumMatches"] += 1

# Match stats
actualCountry = 0
countryGame = 0
for i in range(len(countries)):
    soup = ""
    try:
        time.sleep(0.4)
        browser.get(links[i])
        WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.CLASS_NAME, 'dategamego')))
        html = browser.page_source
        soup = BeautifulSoup(html, features="html.parser")
    except TimeoutException:
        print("I give up...")

    # Print Liga
    if countryGame == 0:
        print(countries[actualCountry]["CountryName"])
    countryGame += 1
    if countries[actualCountry]["NumMatches"] == countryGame:
        actualCountry += 1
        countryGame = 0

    equipos = matches[i].split(" vs ")
    equipos.insert(1, "Empate")
    datos = str(soup).split("vote__pct vote__pct")[1:4]
    for j in range(len(datos)):
        print(equipos[j], datos[j].split("%")[0][-2:] + "%")
    print()

browser.quit()
