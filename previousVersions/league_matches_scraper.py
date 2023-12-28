# Imports
import time, codecs
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
    browser.get("https://www.flashscore.co/futbol/inglaterra/premier-league/resultados/")
    WebDriverWait(browser, timeout_in_seconds).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'event__round--static')))
    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
except TimeoutException:
    print("I give up...")

# Data formatting
data = str(soup).split("sportName soccer")[1]
data = data.split("notificationsDialog")[0]
lines = data.split("id=\"")

ids = []
for i in lines[1:]:
    ids.append(i[4:12])

f = codecs.open("../data/england-1st-division-matches.txt", "w", "utf-8")

# Matches
temp = 0
for i in ids:
    soup = ""
    try:
        time.sleep(0.4)
        browser.get("https://www.flashscore.co/partido/" + i + "/#/resumen-del-partido/estadisticas-del-partido/0")
        WebDriverWait(browser, timeout_in_seconds).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'stat__worseSideOrEqualBackground')))
        html = browser.page_source
        soup = BeautifulSoup(html, features="html.parser")
    except TimeoutException:
        print("I give up...")

    # Header
    header = str(soup).split("tournamentHeader__country")[1]
    header = header.split("Enfrentamientos H2H")[0]
    temp = header.split("</")
    linesHeader = []
    for j in temp:
        if len(j) >= 6:
            linesHeader.append(j)

    infoHeader = []
    infoHeader.append(linesHeader[0].split(">")[-1])  # League Round
    infoHeader.append(linesHeader[1].split(">")[-1])  # Date
    infoHeader.append(linesHeader[7].split(">")[-1] + " " + linesHeader[8].split(">")[-1])  # Home Team Name and Goals
    infoHeader.append(linesHeader[16].split(">")[-1] + " " + linesHeader[10].split(">")[-1])  # Away Team Name and Goals

    # Stats
    stats = str(soup).split("subTabs tabs__detail--sub")[1]
    stats = stats.split("Cuotas prepartido")[0]
    temp = stats.split("</")
    linesStats = []
    for j in temp:
        if len(j) >= 6:
            linesStats.append(j)

    infoStats = []
    for j in range(3, len(linesStats)-5, 5):
        infoStats.append(linesStats[j].split(">")[-1] + " " + linesStats[j+1].split(">")[-1] + " " + linesStats[j+2].split(">")[-1])

    # Printing
    for j in infoHeader:
        f.write(j + "\n")
        print(j)
    f.write("\n")
    print()
    for j in infoStats:
        f.write(j + "\n")
        print(j)
    f.write("------------------------------\n" + "\n")
    print("------------------------------\n")

f.close()
browser.quit()
