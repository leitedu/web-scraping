# Brazilian Power Sector: Automated Daily ONS Report & Reservoir Monitoring

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Execution](https://img.shields.io/badge/Execution-Fully_Runnable-success?style=for-the-badge)

This project automates the extraction, processing, and distribution of critical daily data for the Brazilian electricity market. 

Operating in a hydrothermal power system heavily reliant on water storage, market participants must closely monitor reservoir levels and thermal dispatch dynamics. This pipeline authenticates into the **ONS (Operador Nacional do Sistema Elétrico)** secure portal, downloads the official daily PDF report (`REPDOE`) containing comprehensive hydrological and thermal dispatch data, extracts hydro reservoir storage data, and automatically dispatches a consolidated summary via Microsoft Outlook.

## 📌 Market Context & Business Value
In Brazil's interconnected power grid (SIN), which is divided into four submarkets (Southeast, South, Northeast, and North) according to regional characteristics, pricing and operational decisions are deeply tied to hydrological conditions, making daily tracking of hydro reservoir storage levels and grid operation metrics vital for power trading, generation planning, and market intelligence. 

This automation pipeline fetches daily operational data from **ONS (Operador Nacional do Sistema Elétrico)**:

1. **REPDOE (Relatório Executivo da Programação Diária da Operação Eletroenergética):** Downloads official daily electrical operation reports requiring authenticated portal access.
2. **Hydro Reservoir Storage Data:** Extracts subsystem reservoir storage capacities to track hydro balances across the National Interconnected System (SIN), which act as a direct indicator of the system's generation capacity and energy security.

> **Execution Flexibility:** The script is designed to run gracefully even without ONS credentials (LOGIN and PASSWORD). If omitted, it will skip the REPDOE file download step and proceed directly to reservoir metrics collection.

## ⚙️ How It Works

The main orchestrator execution flow operates as follows:
   ```bash  
   [ main.py ]
   │
   ├── 1. Initialize Browser Instance (Playwright)
   │      └── Launch Playwright context
   │
   ├── 2. ONS Portal Authentication (Conditional)
   │      └── If LOGIN/PASSWORD exist: Download REPDOE report to target folder.
   │              └── Authenticate with retry logic (up to 20 attempts)
   │                   and download REPDOE PDF repor
   │      └── Else: Skip report download
   │
   ├── 3. Reservoir Data Ingestion
   │      └── Extract hydro storage levels from public ONS page
   │      └── Generate email HTML/text body
   |
   ├── 4. Teardown
   │      └── Safely close Playwright browser context
   │
   └── 5. Distribution (MS Outlook)
          └── Format HTML body, attach PDF, and send via BCC
   ```

## 🛠️ Technologies Used
* **Python 3.x** — Core automation language.
* **Playwright** — Dynamic browser automation for portal authentication and scraping.
* **python-dotenv** — Secure management of environment variables (`.env`).
* **pywin32** — Windows COM integration for automated email dispatch (Outlook/Mail services).
* **Python Standard Library:**
  * `datetime` — Target execution date calculations (`D-1` offset).
  * `os` — File path resolution and variable access.

## 🚀 Quick Start

1. Ensure you are running Windows with **Microsoft Outlook** installed locally, configured, and logged in (required for `win32com`).
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install firefox
3. Create a .env file in the root directory based on the .env.example template and fill in your credentials:
   ```bash
   # Optional ONS Credentials
   LOGIN=your_ons_username
   PASSWORD=your_ons_password
   
   # Configuration
   FOLDER=./dados_ons
   TO_EMAIL=email1@domain.com, email2@domain.com
4. Run the orchestrator:
   ```bash
   python main.py
