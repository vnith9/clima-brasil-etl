#Open-Meteo Historical Weather API

import requests
import json

def get_weather_data():

    capitais = {
    "Macapá":           (0.03,   -51.07),
    "Boa Vista":        (2.82,   -60.67),
    "Belém":            (-1.45,  -48.50),
    "São Luís":         (-2.53,  -44.30),
    "Manaus":           (-3.11,  -60.02),
    "Fortaleza":        (-3.73,  -38.54),
    "Teresina":         (-5.09,  -42.80),
    "Natal":            (-5.79,  -35.21),
    "João Pessoa":      (-7.11,  -34.86),
    "Recife":           (-8.05,  -34.88),
    "Porto Velho":      (-8.76,  -63.90),
    "Maceió":           (-9.66,  -35.74),
    "Palmas":           (-10.21, -48.33),
    "Aracaju":          (-10.91, -37.07),
    "Salvador":         (-12.97, -38.51),
    "Cuiabá":           (-15.60, -56.09),
    "Brasília":         (-15.78, -47.92),
    "Goiânia":          (-16.68, -49.25),
    "Belo Horizonte":   (-19.92, -43.93),
    "Vitória":          (-20.31, -40.33),
    "Campo Grande":     (-20.44, -54.61),
    "Rio Branco":       (-9.97,  -67.81),
    "Rio de Janeiro":   (-22.90, -43.17),
    "São Paulo":        (-23.55, -46.63),
    "Curitiba":         (-25.42, -49.27),
    "Florianópolis":    (-27.59, -48.54),
    "Porto Alegre":     (-30.03, -51.23),
}


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

    except requests.exceptions.HTTPError:
        print("Ocorreu um erro HTTP!")

    except requests.exceptions.TooManyRedirects:
        print("O número máximo de redirecionamentos foi excedido!")

    except requests.exceptions.Timeout:
        print("A requisição demorou demais!")

    except requests.exceptions.JSONDecodeError:
        print("Não foi possivel decodificar o texto para JSON!")

def save_json_file(raw_data):
    try:
        with open("raw_data.json", "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)
        return True

    except PermissionError:
        print("Sem permissões do sistema, para realizar essa ação!")
        return False

    except OSError as e:
        print(f"Erro ao salvar o arquivo! {e}")
        return False


if __name__ == "__main__":
    raw_data = get_weather_data()
    if raw_data is None:
        print("Abortando: nenhum dado para salvar.")

    else:
        if not save_json_file(raw_data):
            print("Abortando: erro ao salvar.")