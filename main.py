# Imports
from scripts.A_league_results_scraper import A_league_results_scraper
from scripts.B_average_stats_calculator import B_average_stats_calculator
from scripts.C_upcoming_matches_scraper import C_upcoming_matches_scraper
from scripts.utils import crear_ruta


def main(pais, liga, cant_omitir):
    # Lectura de parámetros
    link_liga = "https://www.flashscore.co/futbol/{}/{}".format(pais, liga)

    # Lectura de versión
    version = 1

    # Especificación de las rutas de datos
    paths = [f'data/2023-24',
             f'data/2023-24/version{version}',
             f'data/2023-24/version{version}/anteriores',
             f'data/2023-24/version{version}/promedios',
             f'data/2023-24/version{version}/proximos']
    for i in paths:
        crear_ruta(i)

    # Ejecución del programa
    print("-------------------- Parte 1 de 3 --------------------")
    print("Recolectando estadísticas anteriores")
    print()
    #league_results_scraper(link_liga + "-2022-2023/resultados/", path + f"/{pais}_{liga}.xlsx", cant_omitir)
    A_league_results_scraper(link_liga + "/resultados/", paths[2] + f"/{pais}_{liga}_23-24.xlsx", cant_omitir)

    print("-------------------- Parte 2 de 3 --------------------")
    print("Calculando estadísticas promedio")
    print()
    B_average_stats_calculator(paths[2] + f"/{pais}_{liga}_23-24.xlsx")

    print("-------------------- Parte 3 de 3 --------------------")
    print("Obteniendo lista de próximos partidos")
    print()
    C_upcoming_matches_scraper(link_liga + "/partidos/", paths[4] + f"/{pais}_{liga}_23-24.xlsx")

# --------------- Grupo 1 - Europa primera división ---------------

main("belgica", "jupiler-pro-league", 0)
main("espana", "laliga-ea-sports", 0)
main("francia", "ligue-1", 0)
main("inglaterra", "premier-league", 0)
main("italia", "serie-a", 0)
main("paises-bajos", "eredivisie", 0)
main("portugal", "liga-portugal", 0)

# --------------- Grupo 1 - Europa segunda división ---------------

##main("belgica", "challenger-pro-league", 0)
#main("espana", "laliga-hypermotion", 0)
##main("francia", "ligue-2", 0)
##main("inglaterra", "championship", 0)
##main("italia", "serie-b", 0)
##main("paises-bajos", "keuken-kampioen-divisie", 0)
#main("portugal", "liga-portugal-2", 0)

# --------------- Grupo 2 - Europa primera división ---------------

#main("alemania", "bundesliga", 0)
##main("austria", "bundesliga", 0)
##main("croacia", "hnl", 0)
##main("dinamarca", "superliga", 0)
##main("escocia", "premiership", 0)
#main("grecia", "superliga", 0)
#main("polonia", "ekstraklasa", 0)
##main("rumania", "liga-1", 0)
#main("rusia", "premier-league", 0)
#main("suiza", "super-league", 0)
#main("turquia", "super-lig", 0)
##main("ucrania", "premier-league", 0)

# --------------- Grupo 2 - Europa segunda división ---------------

##main("alemania", "2-bundesliga", 0)
##main("austria", "2-liga", 0)
##main("croacia", "prva-nl", 0)
#main("dinamarca", "1-division", 0)
#main("escocia", "championship", 0)
##main("grecia", "super-league-2", 0)
##main("polonia", "division-1", 0)
#main("rumania", "liga-2", 0)
#main("rusia", "fnl", 0)
##main("suiza", "challenge-league", 0)
#main("turquia", "1-lig", 0)
##main("ucrania", "persha-liga", 0)

# --------------- Grupo 3 - Sudamérica primera división ---------------

#main("colombia", "primera-a", 226)  # 0 / 226
###main("brasil", "brasileirao-serie-a", 0)

# --------------- Grupo 3 - Sudamérica segunda división ---------------

###main("colombia", "primera-b", 154)  # 0 / 154
