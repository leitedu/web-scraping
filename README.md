# Solar Data Collection Automation

This repository provides robust automation scripts for the daily collection of solar generation data, designed for scalability and asset performance monitoring.

## ⚠️ Security & Disclaimer
**Attention:** This repository contains automation logic only. It does **not** contain any authentication credentials or sensitive environment data. 

To use these scripts, you must provide your own credentials for the respective platforms (iSolarCloud and Growatt). 
- **Privacy:** Never share your `.env` file or hardcoded credentials in any public repository.
- **Compliance:** Ensure you have the appropriate authorization to access and automate data extraction from the platforms configured in this project.

## 📂 Project Summary

| Script | Platform | Focus | Key Functionality |
| :--- | :--- | :--- | :--- |
| `solar_farms_generation.py` | **iSolarCloud** | Utility Scale | Automated login, report downloads, and directory management. |
| `solar_rooftops_generation.py` | **Growatt** | Rooftop | Historic navigation, data filtering, and automated visual capture. |

---

## 🛠️ Detailed Overview

### `solar_farms_generation.py`
*   **Purpose:** Automated extraction of high-volume generation data for utility-scale assets.
*   **Key Features:**
    *   **Workflow:** Performs multi-site authentication, navigates to specific plant dashboards, and triggers report exports.
    *   **File Handling:** Automatically organizes downloaded `.xlsx` files into plant-specific storage directories.

### `solar_rooftops_generation.py`
*   **Purpose:** Visual monitoring and reporting of rooftop solar performance.
*   **Technical Highlights:**
    *   **Smart Stabilization:** Implements a polling logic that monitors the Highcharts SVG `d` attribute in real-time. This ensures that screenshots are captured only after the rendering animation is 100% complete, preventing incomplete or "cut-off" images.
    *   **Browser Orchestration:** Uses Selenium WebDriver combined with JavaScript injection to handle dynamic UI states and zoom levels, ensuring consistent screenshot quality.
    *   **Portfolio Management:** Iterates through rooftop portfolios, applying precise date-based filtering to generate accurate time-series captures.

---

### 3. Environment Configuration
To run the scripts, you must configure your credentials locally:

1. Create a file named `.env` in the root directory (you can use `.env.example` as a template).
2. Fill in the required variables:

| Variable | Description |
| :--- | :--- |
| `LOGIN_ISOLAR` / `SENHA_ISOLAR` | Credentials for the iSolarCloud portal. |
| `SENHA_GROWATT` | Password for the Growatt rooftop portals. |
| `FAZENDA_1` / `FAZENDA_2` | Names of the utility-scale solar farms. |
| `TELHADO_1` / `TELHADO_2` | Login IDs for the rooftop units. |
| `PASTA_UFVS` | Destination path for solar farm reports. |
| `PASTA_TELHADOS` | Destination path for rooftop screenshots. |

---
