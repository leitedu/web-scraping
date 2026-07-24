from playwright.sync_api import sync_playwright
from time import sleep
import win32com.client as win32

#Handles browser
def get_browser():
    p = sync_playwright().start()
    browser = p.firefox.launch()
    context = browser.new_context()
    page = context.new_page()

    return p, browser, context, page

def close_browser(p, browser):
    browser.close()
    p.stop()

#Loop function to try login into ONS site and scrape REPDOE report 
def repdoe(page, day, login, password, folder):
    result = False
    trials = 0
    #Keep trying to scrape data until possible or a limit of tirals
    while not result and trials < 20:
        try:
            #Gets path of saved report and dictionary with reservoir level
            attachments = repdoe_scraper(page, day, login, password, folder)
            result = True
        except:
            trials += 1
            sleep(300)
    
    return [attachments] # Returns attachments as a list for loop in send_email function

#REPDOE scraper
def repdoe_scraper(page, day, login, password, folder):

    #REPDOE ONS report - Brazil's deeper hidrology analysis, thermal dispatch data, energy imports/exports etc.
    attachments = f'{folder}\\REPDOE-{day.strftime("%Y%m%d")}.pdf' #Path to save the file

    with page.expect_download() as download_info:

        page.goto(f'https://sintegre.ons.org.br/sites/9/51/_layouts/download.aspx?SourceUrl=/sites/9/51/Produtos/282/REPDOE-{day.strftime("%Y%m%d")}.pdf')

        # Site Login
        page.locator('xpath=//*[@id="username"]').fill(login)
        page.locator('xpath=//*[@id="password"]').fill(password)
        page.locator('xpath=//*[@id="kc-login"]').click()

    download = download_info.value
    sleep(2)
    download.save_as(attachments)

    return attachments

#Current reservoirs level information
def reservoirs(page, day):
    
    page.goto(f'https://www.ons.org.br/paginas/energia-agora/reservatorios')
    sleep(5)
    reservoirs = {'se': '', 's': '', 'ne': '', 'n': ''} #Dictionary with submarkets (Southeast, South, Northeast, and North)
    i = 1

    for subsistema in reservoirs:
        reservoirs[subsistema] = page.locator(f'xpath=/html/body/form/div[11]/div[1]/div[4]/div[3]/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div[{i}]/h5/span').text_content()
        i += 1

    #Writes email body according to reservoir data            
    body = (
        f"Good Morning!<br><br>Please find attached Daily Report for {day.strftime('%B %d, /%Y')}.<br><br>"
        f"<b>Reservoirs level</b><br>"
        f"Southeast: {reservoirs['se']}<br>"
        f"South: {reservoirs['s']}<br>"
        f"Northeast: {reservoirs['ne']}<br>"
        f"North: {reservoirs['n']}"
    )
    return body

#Email sender
def send_email(subject, to: list, body, attachments: list):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)

    #Ensures 'to' works whether it's a single string or a list
    if isinstance(to, str):
        list_to = [email.strip() for email in to.split(',')]
    else:
        list_to = to
        
    #Join email addresses - blind carbon copy used for security;
    mail.BCC = ';'.join(list_to)

    mail.Subject = subject
    mail.Body = body
    mail.HTMLBody = f'{body}'

    if attachments:
        for attachment in attachments:
            mail.Attachments.Add(attachment)

    mail.Send()
