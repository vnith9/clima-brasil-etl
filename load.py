import psycopg
import os


def ajustar_dataframe_clima(df_clima, mapa_cidades):
    df_clima["cidade"] = df_clima["cidade"].map(mapa_cidades)
    df_clima = df_clima.rename(columns={"cidade": "cidade_id"})

    return df_clima


def conectar_db():
    
    conn = psycopg.connect(dbname=os.environ["POSTGRES_DB"], 
                           user=os.environ["POSTGRES_USER"], 
                           password=os.environ["POSTGRES_PASSWORD"],
                           host=os.environ["POSTGRES_HOST"], 
                           port="5432")
    
    return conn


def criar_tabelas(conn):

    with conn.cursor() as cur:

        cur.execute("""
            CREATE TABLE IF NOT EXISTS cidade(
                id              serial PRIMARY KEY,
                nome            varchar(30) UNIQUE NOT NULL,
                latitude        double precision NOT NULL,
                longitude       double precision NOT NULL);

            CREATE TABLE IF NOT EXISTS clima(
                id                      serial PRIMARY KEY,
                cidade_id               int REFERENCES cidade (id) NOT NULL,
                data                    date NOT NULL,
                temperatura_media_c     real NOT NULL,
                precipitacao_mm         real NOT NULL,
                duracao_luz_dia_h       real NOT NULL,
                radiacao_solar_mj_m2    real NOT NULL,
            UNIQUE (cidade_id, data));
            """)


def inserir_dados_cidade(conn, lista_cidade):

    with conn.cursor() as cur:

        sql_cidade = "INSERT INTO cidade (nome, latitude, longitude) VALUES (%s, %s, %s) ON CONFLICT (nome) DO NOTHING"
        dados_cidade = lista_cidade

        cur.executemany(sql_cidade, dados_cidade)


def query_nome_id(conn):

    mapa_cidades = {}

    with conn.cursor() as cur:

        query = "SELECT id, nome FROM cidade"

        cur.execute(query)
        for id_cidade, nome in cur:
            mapa_cidades[nome] = id_cidade

    return mapa_cidades

            

def inserir_dados_clima(conn, lista_clima):

    with conn.cursor() as cur:

        
        sql_clima = """INSERT INTO clima (data, temperatura_media_c, precipitacao_mm, duracao_luz_dia_h, radiacao_solar_mj_m2, cidade_id)
                        VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (cidade_id, data) DO NOTHING"""
        dados_clima = lista_clima


        cur.executemany(sql_clima, dados_clima)


def carregar_dados_banco(df_cidade, df_clima):

    with conectar_db() as conn:

        criar_tabelas(conn)

        lista_cidade = list(df_cidade.itertuples(index=False, name=None))

        inserir_dados_cidade(conn, lista_cidade)


        mapa_cidades = query_nome_id(conn)

        df_clima = ajustar_dataframe_clima(df_clima, mapa_cidades)

        lista_clima = list(df_clima.itertuples(index=False, name=None))

        inserir_dados_clima(conn, lista_clima)


if __name__ == "__main__":

    from transform import transformar

    df_clima, df_cidade = transformar()

    carregar_dados_banco(df_cidade, df_clima)



    