# Market Intelligence & Energy Report Automation

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Execution](https://img.shields.io/badge/Execution-Fully_Runnable-success?style=for-the-badge)

> **Execution Note:** This project relies partly on private credentials and internal corporate endpoints. It is presented here primarily as a **code architecture showcase**, but can be executed according to the following breakdown:
> * **scraping.py (Python Pipeline):** Can be executed locally for testing and demonstration purposes. Automaticly skips pages that requires login if credentials are not provided
> * **report generator.bas (VBA Module):** Included as illustrative reference to provide full context on the legacy process and end-to-end workflow.

## 🌎 Business & Market Context

The primary purpose of this tool is to automate the daily generation of a **Market Intelligence Report**, providing a comprehensive overview of commodity pricing, energy supply, and demand balance across the **Southern Cone (Cone Sul) market**.

To monitor key financial and energy indicators, data is aggregated from several official sector entities and financial exchanges:

* **ENARGAS (Ente Nacional Regulador del Gas - Argentina):** Official regulatory body publishing gas supply, consumption, and pipeline flow data in Argentina.
* **ONS (Operador Nacional do Sistema Elétrico - Brazil):** Brazil's National Grid Operator, providing operational data on electricity demand, hydro reservoir levels, generation dispatch, and **CMO** (*Custo Marginal de Operação* / Marginal Operational Cost).
* **CCEE (Câmara de Comercialização de Energia Elétrica - Brazil):** The Brazilian power clearinghouse responsible for calculating the **PLD** (*Preço de Liquidação das Diferenças* / Spot Energy Price).
* **CME (Chicago Mercantile Exchange):** Global financial exchange providing futures and options market curves for energy commodities (Brent, TTF, JKM, Currency exchange rates).
* **Argus & Investing.com:** Financial intelligence platforms providing international benchmark and historical pricing and currency exchange rates.



## 🔄 How It Works

The system operates as a hybrid pipeline using **Python for Data Ingestion & Extraction** and **VBA for Presentation Assembly**:

1. **Web Scraping & Data Extraction (Python):** 
   Using `Playwright`, the `orchestrator.py` module accesses regulatory portals and market platforms to fetch updated datasets, pricing tables, and PDF figures:
   * **`enargas(page)`**: Extracts natural gas operational and balance daily data, transport grid linepck projection and gas export reports.
   * **`cmo(page)` & `pld(page)`**: Collects Brazilian spot price signals (CMO/PLD) from power trading portals.
   * **`argus(page, ...)`**: Authenticates and retrieves proprietary market benchmarks (executed conditionally via local credentials).
   * **`investing(page)` & `cme(page, ...)`**: Gathers commodity historical prices and futures curves, respectively.

2. **Data Aggregation & Processing (Python):**
   The raw extracted data, dynamic web screenshots, and tables compiled into structured Excel datasets (`pandas`/`openpyxl`) and local temporary files.

3. **Presentation & Distribution (VBA / Legacy):**
   Once Python finishes data extraction, a secondary Excel spreadsheet reads the scraped files and other company data and imports the updated figures. Thus, **report generator.bas (VBA script)** builds a daily **PowerPoint slide deck**, and formats the final report for executive distribution.



## 🛠️ Technologies Used

* **Python 3.x** — Core language for ETL and web automation.
* **Playwright** — Dynamic browser automation for scraping sector portals.
* **Pandas & OpenPyXL** — Data manipulation, aggregation, and Excel generation.
* **PyMuPDF (`fitz`)** — PDF document parsing and text/image extraction.
* **VBA (Visual Basic for Applications)** — PowerPoint presentation assembly and report formatting.



## 🚀 Quick Start (Scraping Pipeline)

Only the **Python web scraping suite** can be run locally for demonstration purposes. 

1. Install Dependencies
Clone the repository and install the required packages:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
2. Run the Pipeline
Execute the main scraping orchestrator:
   ```bash
   python orchestrator.py
Note on Argus Authentication: The code includes an optional argus() function model that handles user authentication (LOGIN_ARGUS / PASSWORD_ARGUS). This was included solely to demonstrate how login flows are handled in the production pipeline and is not expected to be configured or executed for testing.
