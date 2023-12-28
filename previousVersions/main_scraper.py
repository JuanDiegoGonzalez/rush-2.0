import codecs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Data retrieving
options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options, executable_path='../driver/chromedriver.exe')

soup = ""
try:
    browser.get("https://www.flashscore.co/futbol/bulgaria/parva-liga/clasificacion/")
    timeout_in_seconds = 10
    WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.CLASS_NAME, 'tableWrapper')))
    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
except TimeoutException:
    print("I give up...")
finally:
    browser.quit()

# Data formatting
data = str(soup).split("tableWrapper")[1]
data = data.split("tableLegend")[0]
lines = data.split("\n")

# Table creation
raw_table = []
for i in lines:
    if i[-1] == "]":
        if not i.__contains__(">Forma<"):
            raw_table.append(i + "\n")
        else:
            temp = i.split(">Forma<")
            raw_table.append(temp[0] + "\n")
            raw_table.append(temp[1] + "\n")

resp = []
fila = 0
while fila < len(raw_table):
    resp.append("")
    for i in range(len(raw_table[fila])):
        if (raw_table[fila][i] == ">") and (i+1 < len(raw_table[fila])) and (raw_table[fila][i+1] != "<"):
            index = i+1
            while (index < len(raw_table[fila])) and (raw_table[fila][index] != "<"):
                resp[fila] += raw_table[fila][index]
                index += 1
            resp[fila] += "//"
    fila += 1

f = codecs.open("data/bulgaria-table.txt", "w", "utf-8")
j = 0
for i in resp:
    if j < 2:
        print(i)
        f.write(i)
    else:
        print(i[3:])
        f.write(i[3:])
    j += 1
    f.write("\n")
f.close()
