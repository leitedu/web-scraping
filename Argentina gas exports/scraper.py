from playwright.sync_api import sync_playwright
from pathlib import Path
from time import sleep
import pandas as pd
import re

#Scrapes Secretariat of Energy's website and downloads PDF gas export authorizations
def gas_licenses_database(id_min: int, id_max: int, download: bool, country: str, attempts: int, target_dir: str):
    folder = Path(target_dir)
    folder.mkdir(parents=True, exist_ok=True)
    
    results = [] #Results

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        
        for i in range(id_min, id_max):

            url = f'https://exportaciongasnatural.energia.gob.ar/exportacion-gas-natural/detalle/id/{i}'
            page.goto(url)
            sleep(0.1) #Avoids error on playwright asyncio internal running

            #Reads destination country
            dest_country = page.locator(".panel:has-text('Destino') .panel-body p").inner_text().strip().replace('.', '')

            #Reads seller company name
            raw_text_seller = page.locator("p:has-text('Vendedor:')").inner_text()
            match = re.search(r"Vendedor:\s*(.*?)(?=\s*CUIT|\n|$)", raw_text_seller)
            if match:
                seller = match.group(1).strip().replace('.', '')

            #Reads buyer company name
            raw_text_buyer = page.locator("p:has-text('Vendedor:')").inner_text()
            match = re.search(r"Comprador:\s*(.*)", raw_text_buyer)
            if match:
                buyer = match.group(1).strip().replace('.', '')

            #Downloads licenses from specified country or all liceses if no country is provided
            if (download == True) and (country in dest_country or country == None):

                #Sets PDF name and path
                file_name = f"{i} - {seller} - {buyer}.pdf"
                file_path = folder / file_name

                #Verifies if file is already downloaded and saves it in the file_path if it is not.
                if not file_path.exists():

                    pdf_url = page.locator("#secondary:has(h4:has-text('Adjuntos')) a.download").get_attribute("href")

                    #Try to request until defined maximum atempts
                    for attempt in range(1, attempts):
                        try:
                            response = page.request.get(pdf_url, timeout=30000)
                            with open(folder / file_name, "wb") as f:
                                f.write(response.body())
                        except:
                            sleep(2*attempt) #Increases waiting time as attempts counter increases

            #Appends new row to list of results
            results.append({
                    "ID": i,
                    "Country": dest_country,
                    "Seller": seller,
                    "Buyer": buyer
                })

    #Converts list of results in a dataframe       
    df = pd.DataFrame(results)
    df.to_excel(folder / 'Licenses_by_country.xlsx', index=False)
