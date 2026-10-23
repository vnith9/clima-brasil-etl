#Open-Meteo Historical Weather API

import requests
import json
import os


def get_weather_data(capitais):


    latitudes = [c[0] for c in capitais.values()]

    longitudes = [c[1] for c in capitais.values()]

    url = "https://archive-api.open-meteo.com/v1/archive"


    query_params = {
        "latitude": ",".join(map(str, latitudes)),
        "longitude": ",".join(map(str, longitudes)),
        "start_date": "2020-01-01",
        "end_date": "2025-12-31",
        "daily": ["temperature_2m_mean","precipitation_sum", "daylight_duration",
                  "shortwave_radiation_sum"],
        "timezone": "auto",
        }

    try:
        response = requests.get(url, params=query_params, timeout=60)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.ConnectionError:
        print("Ocorreu um erro na conexão!")
        raise

    except requests.exceptions.HTTPError:
        print("Ocorreu um erro HTTP!")
        raise

    except requests.exceptions.TooManyRedirects:
        print("O número máximo de redirecionamentos foi excedido!")
        raise

    except requests.exceptions.Timeout:
        print("A requisição demorou demais!")
        raise

    except requests.exceptions.JSONDecodeError:
        print("Não foi possivel decodificar o texto para JSON!")
        raise

def save_json_file(raw_data):
    try:
        with open("raw_data.json", "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)
        return True

    except PermissionError:
        print("Sem permissões do sistema, para realizar essa ação!")
        raise

    except OSError as e:
        print(f"Erro ao salvar o arquivo! {e}")
        raise


def extrair_dados(get_weather_data, save_json_file, capitais):

    if os.path.exists("raw_data.json"):
            print("Um arquivo json já existe.")

    else:
        raw_data = get_weather_data(capitais)
    
        if raw_data is None:
            print("Abortando: nenhum dado para salvar.")
        else:
            if not save_json_file(raw_data):
                print("Abortando: erro ao salvar.")
            else:
                print("Dados salvos com sucesso!")