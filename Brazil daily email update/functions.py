from playwright.sync_api import sync_playwright
from datetime import date, timedelta
from time import sleep
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

def loop_try(dia, login, senha, pasta):
    result = False
    tentativas = 0
    while not result and tentativas < 20:
        try:
            local, reservatorios = infos(dia, login, senha, pasta)
            result = True
        except:
            tentativas += 1
            sleep(300)
    

def infos(dia, login, senha, pasta):

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()

        #REPDOE
        local = f'{pasta}\\REPDOE-{dia.strftime("%Y%m%d")}.pdf'

        with page.expect_download() as download_info:

            page.goto(f'https://sintegre.ons.org.br/sites/9/51/_layouts/download.aspx?SourceUrl=/sites/9/51/Produtos/282/REPDOE-{dia.strftime("%Y%m%d")}.pdf')

            page.locator('xpath=//*[@id="username"]').fill(login)
            page.locator('xpath=//*[@id="password"]').fill(senha)
            page.locator('xpath=//*[@id="kc-login"]').click()


        download = download_info.value
        sleep(2)
        download.save_as(local)

        #Reservatorios
        page.goto(f'https://www.ons.org.br/paginas/energia-agora/reservatorios')
        sleep(5)
        reservatorios = {'se': '', 's': '', 'ne': '', 'n': ''}
        i = 1

        for subsistema in reservatorios:
            reservatorios[subsistema] = page.locator(f'xpath=/html/body/form/div[11]/div[1]/div[4]/div[3]/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div[{i}]/h5/span').text_content()
            i += 1

        browser.close()
    
    return local, reservatorios

def envia_email(assunto, destinatarios: list, corpo, anexos: list):
    import win32com.client as win32
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)

    # Junta os emails com ;
    mail.BCC = ';'.join(destinatarios)

    mail.Subject = assunto
    mail.Body = corpo
    mail.HTMLBody = f'{corpo}'


    for anexo in anexos:
        mail.Attachments.Add(anexo)

    #mail.Display(True)
    mail.Send()
