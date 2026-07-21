from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from shutil import move
from time import sleep
from dotenv import load_dotenv

import os

# Load environment variables from .env file
load_dotenv()

# Configuration
ISOLAR_URL = 'https://www.isolarcloud.com.hk/?lang=pt_BR'
LOGIN = os.getenv('LOGIN_ISOLAR')
PASSWORD = os.getenv('SENHA_ISOLAR')
DOWNLOAD_FOLDER = os.getenv('PASTA_UFVS')
PLANTS = [os.getenv('FAZENDA_1'), os.getenv('FAZENDA_2')]
yesterday = datetime.today() - timedelta(days=1)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Setup Chrome
chrome_options = Options()
prefs = {
    "download.default_directory": DOWNLOAD_FOLDER,  
    "download.prompt_for_download": False,       
    "download.directory_upgrade": True,           
    "safebrowsing.enabled": True                  
}

chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)

driver.get(ISOLAR_URL)
driver.maximize_window()

# Login Process
login_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Conta']")))
password_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Senha']")))
login_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-v-b76c5374]")))

login_field.send_keys(LOGIN)
password_field.send_keys(PASSWORD)
login_button.click()

# Clicks on data report screen button and then annual reports section
relatorio_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.icon-G2_Report_28")))
relatorio_btn.click()
annual_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.customized-report-title")))
annual_button.click()

# Data Extraction Loop
for plant in PLANTS:
    # Select the power plant
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, f"//div[@class='el-checkbox-group']//label[normalize-space(.)='{plant}']"))
    ))

# Navigate to download options
btn_d1 = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(.)='Exportar']")))
btn_d1.click()

# Trigger download
opcao_excel = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Exportar como Excel')]")))
opcao_excel.click()
sleep(10) # Wait for file to finish downloading

driver.quit()
