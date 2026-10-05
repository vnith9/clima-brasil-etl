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
            raise
    
    except OSError as e:
            print(f"Erro ao abrir o arquivo! {e}")
            raise

    except json.JSONDecodeError as e:
          print(f"Erro ao ler arquivo json! {e}")
          raise


def normalizar_dados(raw_data):
      df = pd.json_normalize(raw_data)
      df["cidade"] = list(CAPITAIS.keys())
      return df

def filtrar_colunas(df):
      colunas = [x for x in df.columns if x.startswith("daily.")]
      return colunas

def transformar_colunas(df, colunas):
      df_clima = df[colunas + ["cidade"]]
      df_cidade = df[["cidade", "latitude", "longitude"]]
      df_clima = df_clima.explode(colunas, ignore_index=True)
      df_clima = df_clima.rename(columns={
            "daily.time": "data",
            "daily.temperature_2m_mean": "temperatura_media_c",
            "daily.precipitation_sum": "precipitacao_mm",
            "daily.daylight_duration": "duracao_luz_dia_h",
            "daily.shortwave_radiation_sum": "radiacao_solar_mj_m2"
      })
      df_clima["duracao_luz_dia_h"] = (df_clima["duracao_luz_dia_h"] / 3600).round(2)
      df_clima["data"] = pd.to_datetime(df_clima["data"])
      colunas_numeric = ["temperatura_media_c", "precipitacao_mm", "duracao_luz_dia_h", "radiacao_solar_mj_m2"]
      df_clima[colunas_numeric] = df_clima[colunas_numeric].apply(pd.to_numeric)
      return df_clima, df_cidade


def transformar():
      raw_data = abrir_arquivo()

      df = normalizar_dados(raw_data)

      colunas = filtrar_colunas(df)

      df_clima, df_cidade = transformar_colunas(df, colunas)

      return df_clima, df_cidade




#Main

if __name__ == "__main__":

            df_clima, df_cidade = transformar()

            print(df_clima)

            print(df_cidade)