# Imports
import os

import pandas as pd
from scripts.utils import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

titulos_estadisticas = (
                    'HomeTeam',
                    'AwayTeam',
                    'HAPP',  # Home Accurate Passes Percentage

                    'HACr',  # Home Accurate Crosses
                    'HTCr',  # Home Total Crosses
                    'HACrP',  # Home Accurate Crosses Percentage

                    'HALB',  # Home Accurate Long Balls
                    'HTLB',  # Home Total Long Balls
                    'HALBP',  # Home Accurate Long Balls Percentage

                    'HIn',  # Home Interceptions
                    'HCl',  # Home Clearances

                    'HBC',  # Home Big Chances
                    'HBCM',  # Home Big Chances Missed

                    'HHW',  # Home Hit Woodwork

                    'HSIB',  # Home Shots Inside Box
                    'HSOB',  # Home Shots Outside Box



                    'Resultado'
                )


def league_matches_scraper_sofascore(link, output_file, cant_omitir):
    file_exists = os.path.exists(output_file)
    previous_data = {}
    first_value = {}
    if file_exists:
        previous_data = pd.read_csv(output_file.split(".")[0] + ".csv", sep=',', encoding='utf-8', na_values='-')
        first_value = previous_data.iloc[0]

    # Se crea un archivo nuevo
    create_file(output_file)

    # Configuracion del WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options, executable_path='../driver/chromedriver.exe')
    timeout_in_seconds = 10

    print("Obteniendo partidos por fecha")
    try:
        print(link)
        browser.get(link)
        browser.execute_script("arguments[0].click();",
                               browser.find_element_by_xpath('//*[@id="__next"]/div/main/div[1]/div[2]/div[1]/div['
                                                             '5]/div/div[1]/div[2]'))
    except TimeoutException:
        print("I give up...")

    lista_partidos = []
    i = 1
    while i < 3:
        try:
            time.sleep(1)
            browser.get(link)
            browser.execute_script("arguments[0].click();",
                                   browser.find_element_by_xpath('//*[@id="downshift-23-toggle-button"]'))
            time.sleep(1)
            browser.get(link)
            browser.execute_script("arguments[0].click();",
                                   browser.find_element_by_xpath('//*[@id="downshift-23-item-{}"]'.format(i-1)))

            html = browser.page_source
            soup = BeautifulSoup(html, features="html.parser")
            data = str(soup).split("Valoraciones de Sofascore")[1].split("Mostrar más")[0].split("/es/")
            for i in data:
                print(i)

            #links = str(soup).split("https://www.aiscore.com/es/match")[1:]
            #for j in links:
            #    if not j.__contains__("h2h"):
            #        lista_partidos.append(j.split("\"")[0])
        except TimeoutException:
            print("I give up...")
        except NoSuchElementException:
            break
        print("Fecha {}".format(i))
        i += 1
        break
    print()

    '''
    total = len(lista_partidos)
    completados = 0
    terminar = False
    index = 0

    total -= cant_omitir
    while (index < len(lista_partidos)) and (not terminar):
        i = lista_partidos[-1-index]
        # Match info retrieving
        try:
            time.sleep(0.25)
            browser.get("https://www.aiscore.com/es/match" + i)
            WebDriverWait(browser, timeout_in_seconds).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'statsInfo')))
            html = browser.page_source
            soup = BeautifulSoup(html, features="html.parser")
        except TimeoutException:
            completados += 1
            print("Partido " + str(completados) + " de " + str(total) + ":")
            print("No se disputó")
            print(i)
            print()
            index += 1
            continue

        # Header
        header = str(soup).split("flex w-bar-100 homeBox")[1]
        header = header.split("tab-bar")[0]
        temp = header.split("\n")
        info_header = []
        for j in temp:
            if not (j.__contains__("<") or j.__contains__(">")):
                info_header.append(j.strip())

        # Stats
        stats = str(soup).split("possessionBox")[1]
        stats = stats.split("detail-box overview hideBox1")[0]

        temp = stats.split("</")
        info_stats = []
        for j in temp:
            linea = j.split(">")[-1]
            if len(linea) > 1 and bool(re.search(r'\d', linea)):
                info_stats.append(linea.strip())

        # Escritura del archivo excel
        nom_hoja = "Hoja11"
        wb = openpyxl.load_workbook(output_file)
        existe_hoja = False

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
            hoja.append(titulos_estadisticas)

        # File writting
        stats_gen = []
        stats_gen.append(info_header[0])
        stats_gen.append(info_header[-1])
        stats_gen.append(info_header[1])
        stats_gen.append(info_header[-2])

        for j in info_stats[:10]:
            stats_gen.append(j)
        for j in info_stats[-18:]:
            stats_gen.append(j)

        stats_gen.append(int(info_header[1]) - int(info_header[-2]))  # Resultado

        if file_exists and (first_value["HomeTeam"] == stats_gen[0]) and (first_value["AwayTeam"] == stats_gen[1]):
            print("Datos anteriores encontrados. Actualizando archivo")
            print()
            for i in range(len(previous_data)):
                hoja.append(previous_data.iloc[i].tolist())
                wb.save(output_file)
            terminar = True

        if not terminar:
            hoja.append(stats_gen)
            wb.save(output_file)

            # Console printing
            completados += 1
            print("Partido " + str(completados) + " de " + str(total) + ":")
            print(info_header[0] + " vs " + info_header[-1])
            print(info_header[1] + " a " + info_header[-2])
            print(info_stats)
            print()

        index += 1

    # Elimina la hoja por defecto
    eliminar_hoja_por_defecto(output_file)

    # Cerrar el driver del navegador
    browser.quit()

    # Convierte el archivo excel en un archivo CSV
    convertir_excel_a_csv(output_file)
    '''


def main_sofascore(pais_es, pais_en, liga_clasica, liga_nueva, codigo_liga, cant_omitir):
    version = 0
    link_liga = "https://www.sofascore.com/es/torneo/futbol/{}/{}/{}".format(pais_en, liga_nueva, codigo_liga)

    # Especificación de la ruta con los datos
    if not os.path.exists(f'data_sofascore/{pais_es}_{liga_clasica}'):
        os.mkdir(os.path.abspath(os.getcwd()).replace("\\", "/") + "/" + f'data_sofascore/{pais_es}_{liga_clasica}')

    path = f'data_sofascore/{pais_es}_{liga_clasica}/version{version}'
    if not os.path.exists(path):
        os.mkdir(os.path.abspath(os.getcwd()).replace("\\", "/") + "/" + path)

    league_matches_scraper_sofascore(link_liga, path + "/resultados_anteriores.xlsx", cant_omitir)


#main_aiscore("belgica", "belgian", "jupiler-pro-league", "pro-league", "n527r3imms17evx", 0)
#main_aiscore("espana", "spanish", "laliga", "la-liga", "yzrkn6iorbjqle4", 0)
#main_aiscore("espana", "spanish", "laliga-smartbank", "segunda-division", "9oj7x9i9rhe7g3y", 0)
#main_aiscore("francia", "french", "ligue-1", "ligue-1", "5xvkjoilecr7938", 0)
#main_aiscore("francia", "french", "ligue-2", "ligue-2", "0m2q15i5obp76xw", 0)
#main_aiscore("inglaterra", "english", "championship", "football-league-championship", "8vrqwnin9sjqn2o", 0)
#main_aiscore("inglaterra", "english", "premier-league", "premier-league", "mo07dni2vfxknxy", 0)
#main_aiscore("italia", "italian", "serie-a", "serie-a", "r8lk2di1xb0736d", 0)
#main_aiscore("italia", "italian", "serie-b", "serie-b", "g63kv9i9gcz7ezv", 0)
#main_aiscore("paises-bajos", "netherlands", "eredivisie", "eredivisie", "yzrkn6i2rcjqle4", 0)
#main_aiscore("portugal", "portuguese", "liga-portugal", "primera-liga", "n527r3ipms17evx", 0)
main_sofascore("turquia", "turkey", "super-lig", "super-lig", "52", 0)
