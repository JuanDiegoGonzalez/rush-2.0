# Imports
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from scripts.utils import *


def A_league_results_scraper(link, output_file, cant_omitir):
    # Revisa si ya existe el archivo, para actualizar el existente
    file_exists = os.path.exists(output_file)
    previous_data = {}
    first_value = {}
    if file_exists:
        previous_data = pd.read_csv(output_file.split(".")[0] + ".csv", sep=',', encoding='utf-8', na_values='-')
        first_value = previous_data.iloc[0]

    # Configuracion del WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options, executable_path='driver/chromedriver.exe')
    timeout_in_seconds = 10

    # Obtiene el html con la lista de partidos
    soup = obtener_lista_partidos(browser, link)

    # Obtener el id de cada partido
    data = str(soup).split("sportName soccer")[1]  # Inicio tabla de resultados
    data = data.split("notificationsDialog")[0]  # Fin tabla de resultados
    lines = data.split("id=\"")

    ids = []  # Lista de IDs de los partidos
    for i in lines[1:]:
        ids.append(i[4:12])

    # Matches
    total = len(ids) - cant_omitir
    completados = 0
    terminar = False
    index = 0

    # Crear Dataframe
    df = pd.DataFrame(columns=titulos_estadisticas)

    #while (index < len(ids[:-cant_omitir])) and (not terminar):  # Temporada corta (ej: Colombia)
    while (index < len(ids)) and (not terminar):  # Temporada larga
        # ID actual
        i = ids[index]

        # Obtener información del partido
        try:
            time.sleep(random.uniform(0.2, 0.25))

            link_partido = "https://www.flashscore.co/partido/" + i + "/#/resumen-del-partido/estadisticas-del-partido/0"
            browser.get(link_partido)

            WebDriverWait(browser, timeout_in_seconds).until(
                ec.presence_of_element_located((By.CLASS_NAME, '_row_lq1k0_9')))
            html = browser.page_source
            soup = BeautifulSoup(html, features="html.parser")

        except TimeoutException:
            completados += 1
            print("Partido " + str(completados) + " de " + str(total) + ":")
            print("No se disputó")
            print()
            index += 1
            continue

        # Header
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
                   'AwayTeam': lines_header[17],  # Away Team Name
                   'HG': int(lines_header[8]),  # Home Team Goals
                   'AG': int(lines_header[10])}  # Away Team Goals
        new_row['Resultado'] = new_row['HG'] - new_row['AG']

        # Stats
        stats = str(soup).split("estadisticas-del-partido/2")[1]  # Inicio stats
        stats = stats.split("Juegue con responsabilidad")[0]  # Fin stats
        temp = stats.split("</")
        lines_stats = []
        for j in temp[2:]:
            if len(j) >= 8 and not j.endswith(">"):
                lines_stats.append(j.split(">")[-1])
                # print(j.split(">")[-1])  # Debug (no borrar)

        info_stats = []
        termino = False
        # Primera linea: primera estadistica del local (el numero)
        j = 0
        while (j < len(lines_stats)) and not termino:
            if lines_stats[j + 1] in nom_estadisticas:
                # (Local, Nombre estadistica, Visitante)
                info_stats.append([lines_stats[j], lines_stats[j + 1], lines_stats[j + 2]])
            else:
                termino = True
            j += 3

        for j in info_stats:
            pos = nom_estadisticas.index(j[1])*2 + 5  # Busca los índices de nom_estadisticas en titulos_estadisticas
            new_row[titulos_estadisticas[pos]] = j[0]  # Estadística local
            new_row[titulos_estadisticas[pos+1]] = j[2]  # Estadística visitante

        # Transformaciones estadísticas
        new_row['HP'] = str(new_row['HP'])[:-1]
        new_row['AP'] = str(new_row['AP'])[:-1]

        if 'HRC' not in new_row:
            new_row['HRC'] = 0
            new_row['ARC'] = 0

        if 'HYC' not in new_row:
            new_row['HYC'] = 0
            new_row['AYC'] = 0

        # Revisar si ya existe la linea
        if (file_exists and (first_value['Date'] == new_row["Date"]) and
                (first_value["HomeTeam"] == new_row["HomeTeam"]) and
                (first_value["AwayTeam"] == new_row["AwayTeam"])):

            print("Datos anteriores encontrados. Actualizando archivo")
            print()

            df = pd.concat([df, previous_data], ignore_index=True)
            terminar = True
        else:
            # Console printing
            completados += 1
            print("Partido " + str(completados) + " de " + str(total) + ":")
            print(new_row['HomeTeam'] + " vs " + new_row['AwayTeam'])
            print(str(new_row['HG']) + " a " + str(new_row['AG']))
            print()

            index += 1
            # Append the new row to the DataFrame
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Exporta el df a excel
    df = df.astype(tipos)
    df.to_excel(output_file, index=False)

    # Cerrar el driver del navegador
    browser.quit()

    # Convierte el archivo excel en un archivo CSV
    convertir_excel_a_csv(output_file)
