import csv
import pandas as pd

from scripts.utils import convertir_excel_a_csv


def B_average_stats_calculator(db_location):
    # Lectura del archivo
    df = pd.read_csv(db_location.split(".")[0] + ".csv", sep=',', encoding='utf-8', na_values='-')

    # Calculo de promedios por equipo
    # Local
    home_df = df.copy()
    home_df = home_df.drop(['Date', 'AwayTeam', 'Resultado'], axis=1)
    home_average_stats = home_df.groupby('HomeTeam', as_index=False).mean().round(1)

    # Visitante
    away_df = df.copy()
    away_df = away_df.drop(['Date', 'HomeTeam', 'Resultado'], axis=1)
    away_average_stats = away_df.groupby('AwayTeam', as_index=False).mean().round(1)

    # Escritura en archivos de excel
    ruta = db_location.replace("anteriores", "promedios").split(".")[0]
    home_average_stats.to_excel(ruta + "_home-averages.xlsx", index=False)
    away_average_stats.to_excel(ruta + "_away-averages.xlsx", index=False)

    convertir_excel_a_csv(ruta + "_home-averages.xlsx")
    convertir_excel_a_csv(ruta + "_away-averages.xlsx")
