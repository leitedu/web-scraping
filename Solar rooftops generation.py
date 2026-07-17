from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from pathlib import Path
import os

# --- Configuration ---
# Set up URLs and environment variables
GROWATT_URL = 'https://server.growatt.com/login'
GROWATT_PASSWORD = os.getenv('SENHA_GROWATT')
ROOFTOPS = [os.getenv('TELHADO_1'), os.getenv('TELHADO_2')]
SAVE_PATH = Path(os.getenv('PASTA_TELHADOS'))

# Setup Chrome options for headless execution
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

# Define the date (one day before, which is the last full day with generation data)
delta_days = 1 
target_date = datetime.today() - timedelta(days=delta_days)

# --- Functions ---
last_read = ""

def wait_for_chart_stability(driver):
    """
    Necessary due to an animation in generation graph after any input update in the page
    Checks if the Highcharts path attribute 'd', with represents generation line length, has stabilized.
    This ensures the animation is complete before saving.
    """
    global last_read
    try:
        current_read = driver.find_element(By.CSS_SELECTOR, ".highcharts-series-group path").get_attribute("d")
        
        # Check if the path data matches the previous state and has enough data points
        if current_read == last_read and current_read is not None and len(current_read) > 50:
            return True
        last_read = current_read
        return False
    except:
        return False

# --- Main Loop ---
for rooftop in ROOFTOPS:
    driver.get(GROWATT_URL)
    
    # Perform login
    login_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'val_loginAccount')))
    password_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'val_loginPwd')))
    login_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".hasColorBtn.loginB")))

    login_field.send_keys(rooftop)
    password_field.send_keys(GROWATT_PASSWORD)
    login_button.click()
    
    # Wait for the chart to render and be all avaiable in view page
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "svg.highcharts-root")))
    driver.execute_script("document.body.style.zoom='75%'")
    
    # Navigate back to the target day
    for _ in range(delta_days):
        back_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".prevLeft.prvTime")))
        back_button.click()

    # Wait until the chart animation is finished
    WebDriverWait(driver, 30).until(wait_for_chart_stability)

    # Capture and save the screenshot
    chart_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "svg.highcharts-root")))
    file_path = SAVE_PATH / f"generation {target_date.strftime('%Y.%m.%d')} {rooftop}.png"
    
    with open(file_path, "wb") as file:
        file.write(chart_element.screenshot_as_png)

    # Logout
    logout_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, 'btn_logout')))
    logout_button.click()

driver.quit()