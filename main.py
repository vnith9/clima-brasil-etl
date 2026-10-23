from extract import extrair_dados, get_weather_data, save_json_file
from transform import transformar
from load import carregar_dados_banco
from config import CAPITAIS


def main():

    extrair_dados(get_weather_data, save_json_file, CAPITAIS)

    df_clima, df_cidade = transformar(CAPITAIS)

    carregar_dados_banco(df_cidade, df_clima)


if __name__ == "__main__":

    main()



