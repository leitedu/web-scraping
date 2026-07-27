# Argentine Natural Gas Exports: Automated Data Extraction for Market Intelligence

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Execution](https://img.shields.io/badge/Execution-Fully_Runnable-success?style=for-the-badge)

This project automates the extraction of public natural gas export data from authorizations granted by the Argentine Secretariat of Energy. 

It is structured to download license PDFs, parse their contents, and compile a clean Excel database rooted on public data published for the entity, in order to enable deep **Market Intelligence** and data-driven analysis of cross-border energy trade.


## 🌎 Business & Regulatory Context
In the energy sector, regulatory compliance and public transparency generate a massive amount of valuable data. The Argentine government publishes official natural gas export permits on a [public portal](exportaciongasnatural.energia.gob.ar/exportacion-gas-natural), where each authorization is tied to a unique ID. 

This pipeline was built to apply data engineering in extraction of key commercial conditions (pricing, volumes, delivery points, and durations) that are crucial for market analysis.

## 💡 Industry Domain & Economic Concepts

To evaluate natural gas export contracts, the processor automatically scans the downloaded PDFs to extract critical unstructured data, including:

* **Seller & Buyer (*Vendedor y Comprador*)**: The producing or marketing entity in Argentina and the counterpart off-taker/importer in neighboring countries (e.g., Brazil, Chile, Uruguay).
* * **Contract Type (*Condición de Venta*)**: Classifies the supply commitment as either:
  * **Firm (*Firme*)**: Non-curtailable supply where capacity is guaranteed.
  * **Interruptible (*Interrumpible*)**: Supply that can be curtailed by regulatory authorities if domestic demand surges.
* **Delivery Point (*Punto de Exportación*)**: The physical cross-border interconnect facility or pipeline boundary node through which the gas flows (e.g., *Paso de los Libres - Uruguayana*, *Gasoducto NorAndino*, *Cruz del Sur*).
* **Daily and Total Maximum Quantities (*Volúmenes Máximos*)**:
  * **Daily Maximum**: Peak authorized daily flow rate expressed in $m^3/\text{day}$ (at $9,300 \text{ kcal/m}^3$).
  * **Total Maximum**: Cumulative authorized volume cap over the lifetime of the license.
* **Validity (*Plazo de Vigencia*)**: The regulatory operational window, defining the exact start and end dates within which exports are legally permitted.
* * **PIST (*Precio de Ingreso al Sistema de Transporte*)**: The price of the gas molecule right at the entry point of the transportation grid (essentially the gas wellhead/production price before main transmission).
* **Border Price (*Precio en Frontera*)**: The delivered gas price at the export node (border delivery point) before entering the importing country.
* **Transport Tariff (*Precio de Transporte*)**: Derived dynamically by the script:
$$\text{Transport Price} = \text{Border Price} - \text{PIST}$$
This differential represents the pipeline/transmission tariff required to move the gas from the production basin to the border.


## 📌 Architecture & Overview

This project executes a two-tier extraction process designed for scalability and efficiency:
```bash
              ┌──────────────────────────────────────────────┐
              │                 main.py                      │
              └──────────────────────┬───────────────────────┘
                                     │
             ┌───────────────────────┴───────────────────────┐
             ▼                                               ▼
┌───────────────────────────┐                   ┌───────────────────────────┐
│        Stage 1            │                   │        Stage 2            │
│    High-Level Scraper     │                   │    Deep PDF Processor     │
│       (scraper.py)        │                   │      (processor.py)       │
└─────────────┬─────────────┘                   └─────────────┬─────────────┘
│                                               │
▼                                               ▼
• Scrapes web portal metadata                   • Parses downloaded PDFs
• Extracts Buyer, Seller, Country               • Extracts PIST & Border Prices
• Filters by Country & License ID               • Calculates Transport Tariffs
• Downloads PDF Files (Skip existing)           • Handles Formulas vs. Numbers
│                                               │
▼                                               ▼
📊 Database 1: High-Level Flows                 📊 Database 2: Detailed Contract Specs
```

#### 1️⃣ Stage 1: Macro Flow Scraper (`scraper.py`)
* **Web Metadata Harvesting**: Navigates the Secretariat of Energy portal to extract basic license indicators (*Destination Country*, *Buyer*, *Seller*, and *License ID*).
* **Targeted Filtering**: Restricts extraction based on specified ID boundaries (`ID_MIN` / `ID_MAX`) or target countries (`COUNTRY`).
* **Smart File Storage**: Downloads authorization PDFs to the target directory. Includes duplicate checking to skip already downloaded files and exponential backoff retry logic (`ATTEMPTS`) for network resilience.
* **Output**: Generates **Database 1** (`macro_gas_licenses_database.xlsx`), providing an immediate macro-level view of trade flows leaving Argentina.

#### 2️⃣ Stage 2: Deep PDF Processor (`processor.py`)
* **Text Layer Extraction**: Scans downloaded PDFs page-by-page using PyMuPDF to extract granular clauses via resilient Regex patterns.
* **Pricing & Formula Parsing**: Captures **PIST** (*Precio de Ingreso al Sistema de Transporte*) and **Border Prices**, distinguishing between fixed numeric values and indexed formulas.
* **Calculated Metrics**: Computes the **Transport Tariff** ($\text{Border Price} - \text{PIST}$) dynamically for numeric rows while preserving textual formulas intact.
* **Data Cleaning & Standardization**: Translates Spanish Boolean terms (`Si`/`No` $\rightarrow$ `Yes`/`No`), fixes decimal formatting (`3,50` $\rightarrow$ `3.50`), and sanitizes illegal characters.
* **Output**: Generates **Database 2** (`detailed_gas_licenses_database.xlsx`), containing deep contractual specs, volume caps, and operational metrics.

> 📋 **Analytical Note on Market & Data Heterogeneity**  
> Due to regulatory evolution and varying contractual practices at the Secretariat of Energy (*Secretaría de Energía*), authorization documents do not follow a rigid, single-standard reporting format. Pricing fields across licenses frequently alternate between fixed nominal rates (e.g., USD/MMBtu) and complex indexed adjustment formulas (e.g., tied to international benchmarks, Brent, or seasonal tiers).  
>  
> Rather than forcing artificial numeric assumptions or dropping non-standard entries, this pipeline treats heterogeneity as an **intrinsic feature of the energy market**. The dual-type database architecture is deliberately designed to preserve original contractual formulas as intact text strings alongside numeric floats. This guarantees total analytical integrity, allowing energy analysts to evaluate both fixed-price contracts and dynamic indexation mechanisms in their authentic regulatory context.

## 🚀 Key Features & Data Engineering

### 1. Dual-Layer Database Output
* **Database 1 (Macro Flow)**: Quick overview derived directly from web metadata. Ideal for knowing *who* is exporting from Argentina, *who* is buying, and *where* the gas is going.
* **Database 2 (Micro Contract)**: Comprehensive dataset containing deep PDF insights (volumes, PIST, border prices, transport differentials, and contractual clauses).

### 2. Smart File & Network Management
* **Skip Existing Files**: Uses `pathlib.Path.exists()` to check if a license PDF is already stored locally before executing HTTP GET requests.
* **Resilient Retry Mechanism**: Employs an exponential/iterative retry loop (`ATTEMPTS`) to gracefully recover from network timeouts, rate limiting, or server resets (`socket hang up`).
* **Filename Sanitization**: Automatically strips line breaks (`\n`), carriage returns (`\r`), and illegal Windows filesystem characters (`:`, `/`, `\`) from company names to prevent `OSError` bugs during file creation.

### 3. Advanced PDF Parsing & Data Cleaning
* **Regex Extraction (`re`)**: Searches text layers in PDFs for flexible pricing, volumes, and legal clauses, using lookaheads/captures to catch values even if they span multiple lines.
* **Mixed Data Type Handling (`parse_mixed_price`)**: Export contracts often state prices as fixed numbers (e.g., `USD 3.50`) or complex indexed formulas (e.g., `1.1 * Brent + 0.5`). The engine converts purely numerical prices into float types (`3.50`) while **preserving formulas as intact strings**.
* **Safe Transport Calculation (`calculate_transport`)**: Calculates `Border Price - PIST` **only** when both terms are numeric float values. If either term contains a formula or non-numeric note, it safely assigns `"N/A"` without crashing or poisoning valid rows.
* **Language Standardization**: Automatically translates Spanish Boolean flags (`Si`/`No` -> `Yes`/`No`) and converts European/Latin decimal commas (`3,50`) to standard floating-point dots (`3.50`).


## ⚙️ Configuration & Usage

All pipeline execution parameters are centralized inside `main.py`.

```python
from scraper import gas_licenses_database
from processor import scrape_pdf_content

# Configuration Parameters
ID_MIN = 590               # Starting License ID
ID_MAX = 604               # Ending License ID
DOWNLOAD = True            # True: Download PDFs & process deep database
COUNTRY = ''               # Filter by destination country in Spanish (e.g. 'Brasil'). Set '' for all.
TARGET_DIR = "./licenses"  # Output folder for PDFs and Excel files
ATTEMPTS = 3               # Max network retries per PDF download

if __name__ == "__main__":
    # Stage 1: High-Level Macro Database & PDF Downloader
    gas_licenses_database(ID_MIN, ID_MAX, DOWNLOAD, COUNTRY, ATTEMPTS, TARGET_DIR)
    
    # Stage 2: Deep PDF Text Extraction & Processing
    if DOWNLOAD:
        scrape_pdf_content(TARGET_DIR)
```

To run the pipeline, simply execute:
```bash
python main.py
```

## 📁 Output Structure

Upon completion, your target directory (`TARGET_DIR`) will contain:

```bash
licenses/
├── 590 - Pan American Energy SL - Cinergia Chile SpA.pdf
├── 591 - Pampa Energía SA - GM Holdings SA.pdf
├── [...]
├── macro_gas_licenses_database.xlsx    # Database 1: High-Level Web Metadata
└── detailed_gas_licenses_database.xlsx # Database 2: Deep PDF Parsed Dataset
```

## 🛠️ Technologies Used
* **Python 3**
* **Playwright** (Headless browser automation)
* **PyMuPDF / fitz** (PDF processing)
* **Pandas** (Data structuring and export)
* **Regular Expressions (Regex)** (Pattern matching for specific contract clauses)

Install the required dependencies:
```bash
pip install -r requirements.txt
playwright install chromium

