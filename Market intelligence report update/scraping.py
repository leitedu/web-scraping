from playwright.sync_api import sync_playwright
from datetime import date, timedelta
from PIL import Image
from bs4 import BeautifulSoup
from time import sleep
from pathlib import Path
from dotenv import load_dotenv
from io import StringIO
import cv2, numpy as np, pandas as pd, fitz
import os

# Configuration
load_dotenv()
day = date.today()
folder = Path(os.getenv('DATA_FOLDER'))
indexes_path = Path(folder / 'Indexers')
indexes_path.mkdir(parents=True, exist_ok=True)

#Handles browser
def get_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()

    return p, browser, context, page


def close_browser(p, browser):
    browser.close()
    p.stop()


# Scraping functions
def enargas(page):
    relatorios = {'Despacho': ['https://www.enargas.gob.ar/secciones/transporte-y-distribucion/dod-reporte-diario-sistema.php', 'Despacho'],
                'Linepack': ['https://www.enargas.gob.ar/secciones/transporte-y-distribucion/dod-proyeccion-semanal.php', 'Linepack Argentina'],
                'Exportaciones mes': ['https://www.enargas.gob.ar/secciones/reportes/dod-reporte-mensual-exportaciones.php', 'Exportaciones mes', (0, 70, 1190, 1280)],
                'Exportaciones semana': ['https://www.enargas.gob.ar/secciones/reportes/dod-reporte-semanal-exportaciones.php', 'Exportaciones semana', (0, 350, 1190, 1350)]
                }

    for key, param in relatorios.items():

        page.goto(param[0], timeout=0)

        with page.expect_download() as download_info:
            page.locator('xpath=/html/body/main/div/section/div/div/p[1]/a').click()

        download = download_info.value
        download.save_as(folder/f'{param[1]}.pdf')
    
        pdf = fitz.open(folder/f'{param[1]}.pdf')
        matriz = fitz.Matrix(2, 2)

        for pagina in pdf:
            imagem = pagina.get_pixmap(matrix=matriz)
            imagem.save(folder / f'{param[1]}.jpg')
        
        if key in ['Exportaciones mes', 'Exportaciones semana']:
            cut = Image.open(folder/f'{param[1]}.jpg')
            cut = cut.crop(param[2])
            cut.save(folder / f'{param[1]}.jpg')

        elif key == 'Despacho':
            fonte = folder / 'Despacho.jpg'
            caminho_str = str(fonte)
          
            #Finds image contours - table size inside pdf changes from day to day
            im = cv2.imdecode(np.fromfile(caminho_str, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
            ret, thresh_value = cv2.threshold(im, 100, 200, cv2.THRESH_BINARY_INV)
            kernel = np.ones((5,5), np.uint8)
            dilated_value = cv2.dilate(thresh_value, kernel, iterations = 1)
            contours, hierarchy = cv2.findContours(dilated_value, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

            #Applies found contours to crop image
            x = y = w = h = 0
            counter = 0
            for cnt in contours:
                x0, y0, w0, h0 = cv2.boundingRect(cnt)
                if counter == 0:
                    x = x0
                    yi = y0
                    w = w0
                    yf = y0
                else:
                    if x0 < x: x = x0
                    if y0 > yi: yi = y0
                    if w0 > w: w = w0
                    if y0 < yf: yf = y0
                counter += 1


            cut = Image.open(folder / 'Despacho.jpg')
            cut = cut.crop((x, 0.78 * yf, x + w, yi + 15))
            cut.save(folder / 'Despacho.jpg')


def cmo(page):
    page.goto('https://www.ons.org.br/paginas/energia-amanha/cmo-semi-horario/cmo-semi-hor%C3%A1rio')

    with page.expect_download() as download_info:
            page.get_by_text('Acesse o histórico do CMO').click()

    download = download_info.value
    download.save_as(folder/f'CMO.xlsx')
    

def pld(page):
    url_pld = 'https://www.ccee.org.br/precos/painel-precos'
    page.goto(url_pld, wait_until='domcontentloaded')
    sleep(3)

    page.locator('xpath=/html/body/div[1]/div[2]/section[1]/div/div[6]/div/div/div/section/div/div[2]/div/div[1]/div[1]/div/div/div[1]/div/select').select_option('Preço Horário')

    pld_i = page.locator('xpath=/html/body/div[1]/div[2]/section[1]/div/div[6]/div/div/div/section/div/div[2]/div/div[1]/div[1]/div/div/div[2]/div/input')
    pld_i.fill((day + timedelta(-6)).strftime('%d/%m/%Y'))
    pld_i.click()
    pld_i.press('Space')
    pld_i.press('Backspace')
    

    pld_f = page.locator('xpath=/html/body/div[1]/div[2]/section[1]/div/div[6]/div/div/div/section/div/div[2]/div/div[1]/div[1]/div/div/div[3]/div/input')
    pld_f.fill((day).strftime('%d/%m/%Y'))
    pld_f.click()
    pld_f.press('Space')
    pld_f.press('Backspace')
    
    with page.expect_download() as download_info:
        page.locator('xpath=/html/body/div[1]/div[2]/section[1]/div/div[6]/div/div/div/section/div/div[2]/div/div[1]/div[1]/div/div/div[4]/button').click()

    download = download_info.value
    download.save_as(folder/f'PLD.xls')


def argus(page, login, senha):
    url_DES = 'https://direct.argusmedia.com/charts/edit/526779'
    
    page.goto(url_DES)
    page.locator('xpath=//*[@id="username"]').fill(login)
    page.locator('button:has-text("Next")').click()
    page.locator('xpath=//*[@id="password"]').fill(senha)
    page.locator('button:has-text("Sign In")').click()
    sleep(20)

    iframe = page.frame_locator('xpath=/html/body/app-root/app-layout/app-direct-frame/app-frame/iframe')
    botao_exportar = iframe.locator('xpath=/html/body/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/form/div[2]/button').click()
    
    with page.expect_download() as download_info:
        botao_xls = iframe.locator('xpath=/html/body/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/form/div[2]/ul/li[2]/a').click()

    download = download_info.value
    download.save_as(folder/f'Argus.xls')


def investing(page):
    indexes = {'Brent': ['https://finance.yahoo.com/quote/BZ=F/history/', 0],
        'TTF': ['https://finance.yahoo.com/quote/TTF%3DF/history/', 0],
        'HH': ['https://finance.yahoo.com/quote/NG%3DF/history/', 0]}

    data = f'?period1=1672617600&period2={1672542000+(date.today()-date(2022,12,31)).days*86400}&interval=1d&filter=history&frequency=1d'
    consolidado = pd.DataFrame()
    
    for index, url in indexes.items():

        page.goto(f'{url[0]}{data}', wait_until='domcontentloaded')

        page.locator("table tbody tr").first.wait_for(state="visible")
        html_content = page.content()
        tabelas = pd.read_html(StringIO(html_content))

        atualiza = tabelas[url[1]]

        atualiza = atualiza[['Date', 'Close Close price adjusted for splits.', 'Open', 'High', 'Low', 'Volume']]
        atualiza = atualiza.rename(columns={'Close Close price adjusted for splits.': 'Price', 'Volume': 'Vol.'})

        atualiza['Date'] = pd.to_datetime(atualiza['Date'], format='%b %d, %Y')

        atualiza.to_excel(indexes_path / f'{index}.xlsx', index=False)
        atualiza = atualiza.rename(columns={'Price': index})
        
        if consolidado.empty:
            consolidado = atualiza[['Date', index]]
        else:
            consolidado = consolidado.merge(atualiza[['Date', index]], how='outer', on='Date')

        consolidado.to_excel(folder / f'Indexers.xlsx', index=False)


def cme(page, curvas):
    indexes = {'HH': 'https://www.cmegroup.com/markets/energy/natural-gas/natural-gas.settlements.html',
        'TTF': 'https://www.cmegroup.com/markets/energy/natural-gas/dutch-ttf-natural-gas-calendar-month.settlements.html',
        'JKM': 'https://www.cmegroup.com/markets/energy/natural-gas/lng-japan-korea-marker-platts-swap.settlements.html',
        'Brent': 'https://www.cmegroup.com/markets/energy/crude-oil/brent-crude-oil.settlements.html',
        'Euro': 'https://www.cmegroup.com/markets/fx/g10/euro-fx.settlements.html',
        'Dólar': 'https://www.cmegroup.com/markets/fx/emerging-market/brazilian-real.settlements.html'}
    
    date = day + timedelta(-1)
    data = f'#tradeDate={date.strftime("%m")}%2F{date.strftime("%d")}%2F{date.strftime("%Y")}'

    for indice, url in indexes.items():
        page.goto(f'{url}{data}', wait_until='domcontentloaded')
        try:
            page.locator('button:has-text("Load All")').click()
        except:
            pass

        html_content = page.content()
        tabelas = pd.read_html(StringIO(html_content))
        tabela = tabelas[0]

        curva = tabela[['Month', 'Settle']]
        curva = curva.rename(columns={'Month': 'Contrato', 'Settle': indice})

        if curvas.empty:
            curvas = curva
        else:
            curvas = curvas.merge(curva, how = 'outer')

    curvas['Dólar'] = curvas['Dólar'].apply(lambda x: 1/x)

    curvas = curvas.iloc[:-1,:].ffill()
    curvas.to_excel(folder / f'Future curve {day}.xlsx')
    curvas = curvas.iloc[0:0]


# Orchestrator
def main():

    p, browser, context, page = get_browser()

    enargas(page)
    cmo(page)
    pld(page)

    # Executes Argus if credentials are locally configured
    if os.getenv('LOGIN_ARGUS'):
        argus(page, os.getenv('LOGIN_ARGUS'), os.getenv('PASSWORD_ARGUS'))

    investing(page)
    cme(page, curvas = pd.DataFrame())

    close_browser(p, browser)

if __name__ == "__main__":
    main()
