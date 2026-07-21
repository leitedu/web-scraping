from playwright.sync_api import sync_playwright
from pathlib import Path
import pandas as pd
from time import sleep

#Generates list with IDs based on initial and final ID inputed in main.py.
def gera_lista(pasta):
    arquivos = os.listdir(pasta)
    numbers = [int(x[:3]) for x in arquivos]

    return numbers

#Scrapes Secretariat of Energy's website and downloads PDF gas export authorizations
def download_gas_licenses(id_min: int, id_max: int, target_dir: str):
    pasta = Path(target_dir)
    pasta.mkdir(parents=True, exist_ok=True)
    
    erros = []
    paises = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        for i in range(id_max, id_min, -1):
            try:
                sleep(2)
                url = f'https://exportaciongasnatural.energia.gob.ar/exportacion-gas-natural/detalle/id/{i}'
                page.goto(url, wait_until='load', ignore_https_errors=True)
                sleep(2)
                
                pais = page.locator('xpath=/html/body/main/div/div/div/div[2]/div[2]/div[2]/div[2]/p').inner_text()
                paises[i] = pais

                if 'Brasil' not in pais:
                    continue

                vendedor = page.locator('xpath=/html/body/main/div/div/div/div[2]/div[1]/div[2]/div/p/span').text_content().split(":")[1].split("\t")[0].strip()
                comprador = page.locator('xpath=/html/body/main/div/div/div/div[2]/div[1]/div[2]/div/p/span').text_content().split(":")[-1][:-2].strip()

                with page.expect_download() as download_info:
                    page.locator('xpath=/html/body/main/div/div/div/div[3]/table/tbody/tr/td[2]/a').click()

                download = download_info.value
                file_name = f"{i} - {vendedor} - {comprador}.pdf"
                download.save_as(pasta / file_name)
                
            except Exception:
                erros.append(i)
                continue
                
    print(f'Erros encontrados nos IDs: {erros}')
    df = pd.DataFrame(list(paises.items()), columns=['ID', 'Pais'])
    df.to_excel(pasta / 'Licencas_por_pais.xlsx', index=False)
