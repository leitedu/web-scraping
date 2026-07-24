from functions import get_browser, close_browser, repdoe, reservoirs, send_email
from dotenv import load_dotenv
from datetime import date, timedelta
import os

#Load environment variables from .env file
load_dotenv()

#ONS credentials
login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
folder = os.getenv('FOLDER') #Folder where REPDOE report will be saved - must be informed
to = os.getenv('TO_EMAIL') #Recipient email address - must be informed

#Sets day and email's subject
day = date.today() + timedelta(-1)
subject = f'Daily Report {day.strftime("%d/%m/%Y")}'

if __name__ == "__main__":
    #Opens browser
    p, browser, context, page = get_browser()

    #Scrapes information from ONS to download REPDOE if credentials are provided
    if login and password:
        attachments = repdoe(page, day, login, password, folder)
    else:
        attachments = []

    #Writes email's body with reservoir data information
    body = reservoirs(page, day)
    
    #Closes browser
    close_browser(p, browser)

    #Writes and send email 
    send_email(subject, to, body, attachments)
