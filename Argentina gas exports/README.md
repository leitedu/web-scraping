# Argentine Natural Gas Exports: Automated Data Extraction for Market Intelligence

This project automates the extraction of public natural gas export authorizations granted by the Argentine Secretariat of Energy. 

It aims to construct a datased based on public data published for the entity in pdf format and designed to enable deep **Market Intelligence** and data-driven analysis of cross-border energy trade, specifically focusing on exports to Brazil.

## 📌 Business & Regulatory Context
In the energy sector, regulatory compliance and public transparency generate a massive amount of valuable data. The Argentine government publishes official natural gas export permits on a public portal (e.g., `https://exportaciongasnatural.energia.gob.ar/exportacion-gas-natural/`), where each authorization is tied to a unique ID. 

This pipeline was built to apply data engineering in extraction of key commercial conditions (pricing, volumes, delivery points, and durations) that are crucial for market analysis.

## ⚙️ How It Works

The project is divided into a two-step automated pipeline:

1. **Web Scraping (Playwright):** Iterates through a defined range of authorization IDs on the government portal, checks if the destination country matches the target (e.g., Brazil), and automatically downloads the official PDF permits.
2. **Data Extraction & Processing (PyMuPDF + Regex):** Scans the downloaded PDFs to extract critical unstructured data, including:
   - Seller & Buyer
   - Delivery Point (Punto de exportación)
   - Daily and Total Maximum Quantities
   - Contract Type (Firm / Interruptible)
   - Pricing (PIST and Border Price)
   - Validity (Start and End dates)
3. **Consolidation:** Outputs a clean, structured `.xlsx` database ready for BI tools and market analysis.

## 🛠️ Technologies Used
* **Python 3**
* **Playwright** (Headless browser automation)
* **PyMuPDF / fitz** (PDF processing)
* **Pandas** (Data structuring and export)
* **Regular Expressions (Regex)** (Pattern matching for specific contract clauses)

## 🚀 Quick Start

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
2. Set the ID_MIN and ID_MAX parameters in main.py according to the range of permits you want to analyze.
3. Run the orchestrator:
   ```bash
   main.py
