from scraper import download_gas_licenses
from processor import scrape_pdf_content

ID_MIN = None
ID_MAX = None
TARGET_DIR = "./dados_gas"

if __name__ == "__main__":
    print("Passo 1: Iniciando o download dos PDFs via Playwright...")
    download_gas_licenses(ID_MIN, ID_MAX, TARGET_DIR)
    
    print("\nPasso 2: Processando os PDFs e gerando a planilha consolidada...")
    scrape_pdf_content(TARGET_DIR)
    
    print("\nProcesso concluído com sucesso!")
