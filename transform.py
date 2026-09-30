import pandas as pd
import json
from extract import CAPITAIS


def abrir_arquivo():
    try:
        with open ("raw_data.json", "r", encoding="utf-8") as f:
            raw_data=json.load(f)
        return raw_data
    
    except PermissionError:
            print("Sem permissões do sistema, para realizar essa ação!")
            return False
    
    except OSError as e:
            print(f"Erro ao abrir o arquivo! {e}")
            return False

    except json.JSONDecodeError as e:
          print(f"Erro ao ler arquivo json! {e}")
          return False


def normalizar_dados(raw_data):
      df = pd.json_normalize(raw_data)
      df["cidade"] = list(CAPITAIS.keys())
      return df

def filtrar_colunas(df):
      colunas = [x for x in df.columns if x.startswith("daily.")]
      return colunas

def transformar_colunas(df, colunas):
      df_transformado = df[colunas + ["cidade"]]
      df_transformado = df_transformado.explode(colunas, ignore_index=True)
      df_transformado = df_transformado.rename(columns={
            "daily.time": "data",
            "daily.temperature_2m_mean": "temperatura_media_c",
            "daily.precipitation_sum": "precipitacao_mm",
            "daily.daylight_duration": "duracao_luz_dia_h",
            "daily.shortwave_radiation_sum": "radiacao_solar_mj_m2"
      })
      df_transformado["duracao_luz_dia_h"] = (df_transformado["duracao_luz_dia_h"] / 3600).round(2)
      df_transformado["data"] = pd.to_datetime(df_transformado["data"])
      colunas_numericas = ["temperatura_media_c", "precipitacao_mm", "duracao_luz_dia_h", "radiacao_solar_mj_m2"]
      df_transformado[colunas_numericas] = df_transformado[colunas_numericas].apply(pd.to_numeric)

      return df_transformado

#Main

raw_data = abrir_arquivo()

df = normalizar_dados(raw_data)

colunas = filtrar_colunas(df)

df_transformado = transformar_colunas(df, colunas)

print(df_transformado)

print(df_transformado.dtypes)

print(df_transformado.isnull().sum())