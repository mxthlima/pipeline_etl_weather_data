import requests
import json
from pathlib import Path

import logging 
logging.basicConfig(level=logging.INFO, format='%asctime)s - %(levelname)s - %(message)s')


# Função de extração dos dados
def extract_weather_data (url:str) -> list:
    response = requests.get(url)
    data = response.json() # Transformando a resposta da API em dicionário Python

    if response.status_code != 200:
        logging.error("Erro na requisição")
        return []

    if not data:
        logging.warn('Nenhum dado retornado')
        return []

    #Criando o caminho das pastas para salvarmos o arquivo
    output_path = 'data/weather_data.json'
    output_dir = Path(output_path).parent # .parent indica ao python q estamos 1 pasta acima (sai do src e busca 'data')
    output_dir.mkdir(parents=True, exist_ok=True)

    #Abrindo o arquivo gerado e escrever dentro dele
    with open(output_path, 'w') as f: # 'w' = write (modo escrita)
        json.dump(data, f, indent=4)
        
    logging.info(f'Arquivo salvo em {output_path}')
    return data 

