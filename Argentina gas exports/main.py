from scraper import gas_licenses_database
from processor import scrape_pdf_content

ID_MIN = None
ID_MAX = None
DOWNLOAD = True
COUNTRY = '' #Name in Spanish, empty for download all countries data
TARGET_DIR = None
ATTEMPTS = None

if __name__ == "__main__":

    gas_licenses_database(ID_MIN, ID_MAX, DOWNLOAD, COUNTRY, ATTEMPTS, TARGET_DIR)
    
    if DOWNLOAD:
        scrape_pdf_content(TARGET_DIR)
