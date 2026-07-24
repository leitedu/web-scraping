# Solar Assets Generation Data Collection Automation

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Execution](https://img.shields.io/badge/Execution-Showcase_Only-blue?style=for-the-badge)

**Attention:** This repository contains automation logic only. It does not contain any authentication credentials or sensitive environment data. It is presented here primarily as a code architecture showcase rather than a publicly runnable application, due to its exclusive dependency on private credentials.

## 📌 Business Context & Value

This repository provides automation scripts for the daily collection of solar generation data.

The script automatically logs into the solar inverter management portal to retrieve detailed, plant-level generation metrics. This data is critical for solar energy teams to continuously monitor performance, build daily KPIs, and map overall plant efficiency (such as Performance Ratio and yield).

### ☀️ Why Solar Generation Monitoring Matters

For renewable energy assets, consistent monitoring is essential due to the inherent nature of the resource:

* **Intermittency & Seasonality:** Solar energy output is highly sensitive to daily weather variations, cloud coverage, and seasonal irradiation shifts. Continuous data collection allows operations teams to baseline expected output against real-time weather dynamics.
* **Performance Degradation & Anomaly Detection:** Automated daily metrics help identify equipment underperformance, string outages, or inverter trips immediately—minimizing lost generation and revenue.
* **Asset Optimization:** Aggregating granular, inverter-level generation data enables long-term performance trend analysis, optimizing preventive maintenance schedules and ensuring maximum yield across the plant's operational lifecycle.


## 📂 Project Summary

| Script | Platform | Focus | Key Functionality |
| :--- | :--- | :--- | :--- |
| `solar_farms_generation.py` | **iSolarCloud** | Solar farms | Downloads generation database |
| `solar_rooftops_generation.py` | **Growatt** | Rooftops | Downloads generation graphs |


## 📋 Detailed Overview

### `solar_farms_generation.py`
*   **Purpose:** Automated extraction of high-volume generation data for utility-scale assets.
*   **Key Features:**
    *   **Workflow:** Performs multi-site authentication, navigates to specific plant dashboards, and triggers report exports by power plant.
    *   **File Handling:** Automatically organizes downloaded `.xlsx` files into plant-specific storage directories.

### `solar_rooftops_generation.py`
*   **Purpose:** Visual monitoring and reporting of rooftop solar performance.
*   **Technical Highlights:**
    *   **Smart Stabilization:** Implements a polling logic that monitors the Highcharts SVG `d` attribute in real-time. This ensures that screenshots are captured only after the rendering animation is 100% complete, preventing incomplete or "cut-off" images.
    *   **Browser Orchestration:** Uses Selenium WebDriver combined with JavaScript injection to handle dynamic UI states and zoom levels, ensuring consistent screenshot quality.
    *   **Portfolio Management:** Iterates through rooftop portfolios, applying precise date-based filtering to generate accurate time-series captures.


### ⚙️ Environment Configuration
To run the scripts, it's necessary to configure credentials locally in an `.env` file:

| Variable | Description |
| :--- | :--- |
| `LOGIN_ISOLAR` / `SENHA_ISOLAR` | Credentials for the iSolarCloud portal. |
| `SENHA_GROWATT` | Password for the Growatt rooftop portals. |
| `FAZENDA_1` / `FAZENDA_2` | Names of the utility-scale solar farms. |
| `TELHADO_1` / `TELHADO_2` | Login IDs for the rooftop units (same name as rooftop itself). |
| `PASTA_UFVS` | Destination path for solar farm reports. |
| `PASTA_TELHADOS` | Destination path for rooftop screenshots. |


## 🛠️ Technologies Used

* **Python 3.x** — Core programming language.
* **Selenium WebDriver** — Web browser automation framework used for navigating web elements, handling dynamic content, and waiting for explicit conditions (`WebDriverWait`).
* **Python Standard Library:**
  * `datetime` — For handling date calculations and dynamic time intervals.
  * `pathlib` & `os` — For file system path manipulations and environment handling.
