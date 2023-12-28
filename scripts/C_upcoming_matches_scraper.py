# Imports
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from scripts.utils import *


def C_upcoming_matches_scraper(link, output_file):
    # Configuracion del WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options, executable_path='driver/chromedriver.exe')
    timeout_in_seconds = 10

    # Obtiene el html con la lista de partidos
    soup = obtener_lista_partidos(browser, link)

    # Data formatting: extract matches ID
    data = str(soup).split("sportName soccer")[1]
    data = data.split("notificationsDialog")[0]
    lines = data.split("id=\"")

    ids = []
    for i in lines[1:]:
        if i[12] != "<":
            ids.append(i[4:12])

    # Matches
    total = len(ids)
    completados = 0
    index = 0

    # Crear Dataframe
    df = pd.DataFrame(columns=titulos_estadisticas)

    while (index < len(ids)) and (completados < 30):
        # ID actual
        i = ids[index]

        # Obtener información del partido
        soup = ""
        try:
            time.sleep(random.uniform(0.2, 0.25))

            link_partido = "https://www.flashscore.co/partido/" + i + "/#/resumen-del-partido"
            browser.get(link_partido)

            WebDriverWait(browser, timeout_in_seconds).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'participant__participantNameWrapper')))
            html = browser.page_source
            soup = BeautifulSoup(html, features="html.parser")
        except TimeoutException:
            print("I give up...")

        # Header
        if len(str(soup).split("tournamentHeader__country")) < 2:
            continue
        header = str(soup).split("tournamentHeader__country")[1]  # Inicio header
        header = header.split("Enfrentamientos H2H")[0]  # Fin header
        temp = header.split("</")
        lines_header = []
        for j in temp:
            if len(j) >= 6:
                lines_header.append(j.split(">")[-1])
                # print(j.split(">")[-1])  # Debug (no borrar)

        new_row = {'Date': lines_header[1],  # Date
                   'HomeTeam': lines_header[7],  # Home Team Name
                   'AwayTeam': lines_header[13] if lines_header[15] == "Resumen" else lines_header[15]}  # Away Team Name

        # Predicted (average) stats
        ruta = output_file.replace("proximos", "promedios").split(".")[0]
        home_df = pd.read_csv(ruta + "_home-averages.csv", sep=',', encoding='utf-8', na_values='-')
        away_df = pd.read_csv(ruta + "_away-averages.csv", sep=',', encoding='utf-8', na_values='-')

        for j in titulos_estadisticas[3:-1]:
            if j.startswith("H"):
                fila = home_df[home_df['HomeTeam'] == new_row['HomeTeam']]
                new_row[j] = fila.iloc[0][j]
            else:
                fila = away_df[away_df['AwayTeam'] == new_row['AwayTeam']]
                new_row[j] = fila.iloc[0][j]
            print(new_row[j])

        # Console printing
        completados += 1
        print("Partido " + str(completados) + " de " + str(total) + ":")
        print(new_row['HomeTeam'] + " vs " + new_row['AwayTeam'])
        print()

        index += 1
        # Append the new row to the DataFrame
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Exporta el df a excel
    df.to_excel(output_file, index=False)

    # Cerrar el driver del navegador
    browser.quit()

    # Convierte el archivo excel en un archivo CSV
    convertir_excel_a_csv(output_file)
