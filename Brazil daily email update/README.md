# Brazilian Power Sector: Automated Daily ONS Report & Reservoir Monitoring

This project automates the extraction, processing, and distribution of critical daily data for the Brazilian electricity market. 

Operating in a hydrothermal power system heavily reliant on water storage, market participants must closely monitor reservoir levels and thermal dispatch dynamics. This pipeline authenticates into the **ONS (Operador Nacional do Sistema Elétrico)** secure portal, downloads the official daily PDF report (`REPDOE`), extracts key storage metrics, and automatically dispatches a consolidated summary via Microsoft Outlook.

## 📌 Market Context & Business Value
In Brazil's interconnected power grid (SIN), pricing and operational decisions are deeply tied to hydrological conditions:
* **Reservoir Levels:** Act as a direct indicator of the system's generation capacity and energy security.
* **Thermal Dispatch:** Triggered when hydro levels drop, directly impacting marginal prices (PLD) and market volatility.

This script demonstrates proficiency in automating interactions with authenticated institutional platforms, handling retry resilience, and streamlining executive communication for energy trading and market intelligence desks.

## ⚙️ How It Works

The automated pipeline executes the following steps:
1. **Authenticated Scraping (Playwright):** Handles credentials to log into the ONS portal securely with a built-in retry mechanism (up to 20 attempts) to ensure resilience against connection drops.
2. **Data Retrieval:** Downloads the official daily PDF report (`REPDOE`) containing comprehensive hydrological and thermal dispatch data.
3. **Information Extraction:** Parses current subsystem reservoir levels directly from the public energy dashboard.
4. **Automated Dispatch (`win32com`):** Uses local Microsoft Outlook integration to format an HTML summary body, attach the PDF report securely, and blind-copy (BCC) the stakeholder distribution list.

## 🛠️ Technologies Used
* **Python 3**
* **Playwright** (Headless browser automation & secure session handling)
* **pywin32** (Local Microsoft Outlook desktop automation)
* **python-dotenv** (Secure credential and environment management)

## 🚀 Quick Start

1. Ensure you are running Windows with **Microsoft Outlook** installed locally (required for `win32com`).
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install firefox
3. Create a .env file in the root directory based on the .env.example template and fill in your credentials:
   ```bash
   LOGIN=your_ons_username
   PASSWORD=your_ons_password
   FOLDER=./dados_ons
   TO_EMAIL=email1@domain.com, email2@domain.com
4. Run the orchestrator:
   ```bash
   python main.py
