# Imports
import time, codecs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import openpyxl

nom_estadisticas = ['Posesión de balón','Remates','Remates a puerta','Remates fuera','Remates rechazados'
    ,'Tiros libres','Córneres','Fueras de juego','Saques de banda','Paradas','Faltas'
    ,'Tarjetas rojas','Tarjetas amarillas','Pases totales','Pases completados','Tackles'
    , 'Ataques','Ataques peligrosos']

def funcion_principal(link):
    # WebDriver config
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options, executable_path='../driver/chromedriver.exe')
    timeout_in_seconds = 10

    # Data retrieving
    soup = ""
    try:
        browser.get(link)
        while True:
            time.sleep(1)
            html = browser.page_source
            soup = BeautifulSoup(html, features="html.parser")
            if str(soup).__contains__("Mostrar más partidos"):
                time.sleep(1)
                browser.execute_script("arguments[0].click();",
                                       browser.find_element_by_xpath('//*[@id="live-table"]/div[1]/div/div/a'))
            else:
                break
    except TimeoutException:
        print("I give up...")

    # Data formatting
    season = ((str(soup).split("sportName soccer")[0]).split(" class=\"heading__info\">")[1]).split("</div>")[0]
    data = str(soup).split("sportName soccer")[1]
    data = data.split("notificationsDialog")[0]
    lines = data.split("id=\"")

    ids = []
    for i in lines[1:]:
        ids.append(i[4:12])

    f = codecs.open("../data/england-1st-division-matches.txt", "w", "utf-8")

    # Matches
    temp = 0
    for i in ids[-3:]:
        soup = ""
        try:
            time.sleep(0.25)
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
        infoHeader.append(
            linesHeader[7].split(">")[-1] + " " + linesHeader[8].split(">")[-1])  # Home Team Name and Goals
        infoHeader.append(
            linesHeader[16].split(">")[-1] + " " + linesHeader[10].split(">")[-1])  # Away Team Name and Goals

        # Stats
        stats = str(soup).split("subTabs tabs__detail--sub")[1]
        stats = stats.split("Cuotas prepartido")[0]
        temp = stats.split("</")
        linesStats = []
        for j in temp:
            if len(j) >= 6:
                linesStats.append(j)

        infoStats = []
        for j in range(3, len(linesStats) - 5, 5):
            if linesStats[j + 1].split(">")[-1] in nom_estadisticas:
                infoStats.append([linesStats[j].split(">")[-1], linesStats[j + 1].split(">")[-1], linesStats[j + 2].split(">")[-1]])
            else:
                continue

        # Printing
        print(season)
        if len(season.split("/")) > 1:
            nom_hoja = (infoHeader[0].split("-"))[0] + season.split("/")[0] + season.split("/")[1]
        else:
            nom_hoja = (infoHeader[0].split("-"))[0] + season.split("/")[0]
        wb = openpyxl.load_workbook('../data/data_matches_mismarcadores.xlsx')
        existe_hoja = False
        hoja = wb.active

        for hoja_w in wb:
            if nom_hoja == hoja_w.title:
                existe_hoja = True

        if existe_hoja:
            hoja = wb[nom_hoja]
            wb.active = hoja

        else:
            hoja = wb.create_sheet(nom_hoja)
            wb.active = hoja
            # Crea la fila del encabezado con los títulos
            hoja.append(
                (
                    'Date', 'HomeTeam', 'AwayTeam', 'HG', 'AG', 'HP', 'AP', 'HTS', 'ATS', 'HSI', 'ASI', 'HSO', 'ASO','HBS',
                    'ABS',
                    'HFK',
                    'AFK',
                    'HC', 'AC', 'HOFF', 'AOFF', 'HTI', 'ATI', 'HGS', 'AGS',
                    'HF', 'AF', 'HRC',
                    'ARC', 'HYC', 'AYC', 'HTP', 'ATP', 'HPC', 'APC', 'HT', 'AT', 'HA', 'AA', 'HDA', 'ADA'))

        stats_gen = []
        stats_gen.append(infoHeader[1])
        datos_local = infoHeader[2]
        datos_visita = infoHeader[3]
        stats_gen.append(datos_local[:-2])
        stats_gen.append(datos_visita[:-2])
        stats_gen.append(datos_local[-2:])
        stats_gen.append(datos_visita[-2:])
        print(datos_visita[:-2])
        print(datos_visita[-2:])
        # for j in infoHeader:
        #     f.write(j + "\n")
        #     print(j)
        # f.write("\n")
        # print()
        #print(len(infoStats))
        contador=0
        for j in infoStats:
            act = j
            #print(act)
            if act[1] == nom_estadisticas[contador]:
                stats_gen.append(act[0])
                stats_gen.append(act[2])
                contador = contador+1
            else:
                dif_index = nom_estadisticas.index(act[1]) - contador
                #print(dif_index)
                #print(nom_estadisticas.index(act[1]))
                contador = nom_estadisticas.index(act[1]) + 1

                for i in range(dif_index):
                    stats_gen.append(None)
                    stats_gen.append(None)
                stats_gen.append(act[0])
                stats_gen.append(act[2])

        hoja.append(stats_gen)
        wb.save('./data/data_matches_mismarcadores.xlsx')

        #     f.write(j + "\n")
        #     print(j)

        # f.write("------------------------------\n" + "\n")
        # print("------------------------------\n")
    wb.close()
    f.close()
    browser.quit()


with open("../data/linksLigas.txt") as archivo:
    for linea in archivo:
        funcion_principal(linea)
# funcion_principal("")