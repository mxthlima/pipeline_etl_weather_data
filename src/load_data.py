from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#carregando as variaveis de ambiente q estão dentro da pasta config/.env
env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(env_path)

#pegando as variáveis
user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')
host = "postgres"  # Nome do serviço definido no docker-compose.yml

#montando a url pra fazer a conexão com o banco de dados
def get_engine():
    logging.info(f'-> Conectando em {host}:5432/{database}')
    return create_engine(
        f'postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}'
    )

engine = get_engine()

#função para enviar os dados para o banco de dados
def load_weather_data(table_name:str, df):
    df.to_sql(
        name = table_name,
        con = engine,
        if_exists = 'append',
        index = False
    )

    logging.info(f'-> Dados carregados na tabela {table_name} com sucesso!')

    df_check = pd.read_sql(f'SELECT * FROM {table_name}', con=engine)
    logging.info(f'Total de registros na tabela {table_name}: {len(df_check)}\n')