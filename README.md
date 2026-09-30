PROJETO ETL

Projeto ETL com dados históricos de clima das capitais dos estados do Brasil.

Stack utilizada:
Python
SQL
Docker
PostgreSQL
Pandas

Fluxo: 
Extrair dados da api Historical Weather da Open-Meteo, e salvar num arquivo json.
Transformar os dados em uma tabela.
Carregar os dados em um Banco de Dados PostgreSQL.
Analisar os dados usando SQL.


Extract.py:

Extrai dados históricos de 5 anos, das capitais dos estados do Brasil. Temperatura Média, Precipitação, Duração de luz do dia, radiação solar.

E salva esses dados num arquivo JSON.



Transform.py: 

Normalização e transformação dos dados, adequando-os ao banco de dados.



