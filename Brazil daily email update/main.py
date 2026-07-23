from functions import loop_try, send_email
from dotenv import load_dotenv
import os

#Load environment variables from .env file
load_dotenv()
login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
folder = os.getenv('FOLDER')
to = os.getenv('TO_EMAIL', '')

#Sets day and email's subject
day = date.today() + timedelta(-1)
subject = f'Daily Report {day.strftime("%d/%m/%Y")}'

if __name__ == "__main__":

  #Scrapes information from ONS site and returns file path and email's body 
  attachments, body = loop_try(day, login, password, folder)

  #Writes and send email 
  send_email(subject, to, body, attachments)
