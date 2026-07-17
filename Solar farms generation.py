from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from shutil import move
from time import sleep
from dotenv import load_dotenv

import glob
import os

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
ISOLAR_URL = 'https://www.isolarcloud.com.hk/?lang=pt_BR'
LOGIN = os.getenv('LOGIN_ISOLAR')
PASSWORD = os.getenv('SENHA_ISOLAR')
DOWNLOAD_FOLDER = os.getenv('PASTA_UFVS') # Path where files are initially downloaded
TARGET_BASE_DIR = 'C:/Users/eduardosilva-aeg/Documents/Materiais/Solar/Geração/'

PLANTS = [os.getenv('FAZENDA_1'), os.getenv('FAZENDA_2')]
yesterday = datetime.today() - timedelta(days=1)

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)

driver.get(ISOLAR_URL)
driver.maximize_window()

# --- Login Process ---
login_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Conta']")))
password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Senha']")))
login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-v-b76c5374]")))

login_field.send_keys(LOGIN)
password_field.send_keys(PASSWORD)
login_button.click()

# Handle initial popup/agreement
agree_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/span[1]')))
agree_button.click()

# --- Data Extraction Loop ---
for plant in PLANTS:
    # Select the power plant
    plant_element = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.XPATH, f"//*[text() = '{plant}']")))
    plant_element.click()

    # Navigate to download options
    btn_d1 = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[1]/section/div/div[2]/div/div[3]/div[1]/div[2]/button[1]')))
    btn_d1.click()
    
    date_box = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/div/div[2]/div/div[3]/div[2]/div[1]/div[1]/div/button')))
    date_box.click()

    # Trigger download
    download_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ul/li[1]')))
    download_button.click()
    sleep(10) # Wait for file to finish downloading

    # File management: Identify the latest file in the download folder
    files = glob.glob(f'{DOWNLOAD_FOLDER}/*')
    latest_file = max(files, key=os.path.getctime)
    
    # Rename and move the file to the target structure
    new_filename = f"{yesterday.strftime('%y.%m.%d')} {plant}.xlsx"
    destination_path = os.path.join(TARGET_BASE_DIR, plant, new_filename)
    
    os.rename(latest_file, os.path.join(DOWNLOAD_FOLDER, new_filename))
    move(os.path.join(DOWNLOAD_FOLDER, new_filename), destination_path)

    # Return to the main list
    back_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/span')))
    back_button.click()

driver.quit()