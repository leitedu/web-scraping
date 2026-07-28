# ⚡Energy Market Web-Scraping Hub

A centralized collection of automated web scrapers and data ingestion scripts tailored for **Latin American energy market data** (Natural Gas & Electricity).


## 📁 Repository Overview

| Subfolder / Script | Target Data / Platform | Description |
| :--- | :--- | :--- |
| **`Argentina gas exports/`** | Secretariat of Energy (Argentina) | Scrapes gas export authorizations, downloads PDFs and, extracts licenses metadata. |
| **`solar generation/`** | Power Grid / Generation Portals | Extracts solar generation time-series and formats performance metrics. |
| **`Brazil daily email update/`** | Brazilian Energy Market | Automated daily dispatch/email report pipeline for national energy metrics. |
| **`Market intelligence report update/`** | Market Intelligence Data | Web scraper feeding market intelligence data directly to VBA Powerpoint orchestrator. |

## 🚀 Quick Start

### 1. Requirements
For each project, install dependencies across the hub.
> Example: For playwright projects
```bash
pip install playwright pandas openpyxl matplotlib
playwright install chromium
```
### 2. Running a Scraper
Navigate to the desired project folder and execute the main entrypoint:
> Example: Running the Argentina Gas Scraper
```bash
cd gas_argentina
python main.py
```
## 🖼️ Sample Outputs & Visuals

Argentina Gas Flow Scraper (`Argentina gas exports/`)
Outputs structured excel files with extracted buyer, seller, and license IDs:

```bash
licenses/
├── 590 - Pan American Energy SL - Cinergia Chile SpA.pdf
├── macro_gas_licenses_database.xlsx
```
