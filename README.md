
# Projeto ETL - Dados Históricos do Clima nas Capitais Brasileiras

**Status:** em desenvolvimento

<br>

## Sobre o projeto

Este projeto consiste no desenvolvimento de um pipeline ETL (Extract, Transform, Load) para coletar, transformar e armazenar dados históricos do clima das capitais dos estados brasileiros.

Os dados são extraídos da Historical Weather API da Open-Meteo, processados com Python e Pandas e carregados em um banco de dados PostgreSQL, permitindo a análise desses dados utilizando SQL.

<br>

## Objetivo

Construir um pipeline ETL de ponta a ponta que coleta 5 anos de dados históricos do clima das 27 capitais brasileiras, estrutura esses dados em um banco relacional e permite consultá-los com SQL para responder perguntas sobre o clima no país.

Este projeto está sendo desenvolvido como um exercício prático de aprendizado.

<br>

## Stack utilizada
- Python
- Pandas
- SQL
- PostgreSQL
- Docker
- requests

<br>

## Como funciona

API Open-Meteo → extract.py → transform.py → load.py → PostgreSQL

1. **Extract** (`extract.py`): Consulta a API e salva a resposta bruta em raw_data.json.
2. **Transform** (`transform.py`): Lê o JSON, achata a estrutura aninhada e gera dois DataFrames.
3. **Load** (`load.py`): Carrega os DataFrames no banco de dados PostgreSQL.

<br>

## Estrutura do projeto

```
api_clima_brasil/
├── .dockerignore                        # Arquivos e pastas ignorados pelo Docker.
├── .gitignore                           # Arquivos e pastas ignorados pelo Git.
├── compose.yaml                         # Orquestra serviços e contêineres da aplicação.
├── Dockerfile                           # Define as instruções para construir a imagem da aplicação.
├── extract.py                           # Extrai os dados da API.
├── load.py                              # Carrega os dados no banco de dados.
├── main.py                              # Orquestra o pipeline.
├── raw_data.json                        # Dados brutos armazenados para evitar chamadas repetidas à API.
├── README.md                            # Visão geral e instruções para o projeto.
├── requirements.txt                     # Dependências do projeto.
├── transform.py                         # Transforma os dados.
```

<br>

## Modelo de dados

**Em breve**

<br>

## Como executar 

**Em breve**

<br>

## Próximos passos

- [ ] Banco de dados PostgreSQL
- [ ] load.py
- [ ] Análise com SQL
- [ ] Revisão e possível refatoração do código




