import re
import fitz
from pathlib import Path
import pandas as pd

#Reads downloaed PDFs and extracts data via Regex, then compile in Excel spreadsheet.
def scrape_pdf_content(target_dir: str) -> None:
    folder = Path(target_dir)
    files = [f for f in folder.iterdir() if f.suffix == '.pdf']

    #Note: PIST stands for molecule price in transport system entry
    data = {
        "Seller": [], "Buyer": [], "Destination country": [], "Delievery point": [], 
        "Daily Volume Contracted": [], "Maximum volume": [], "Firm": [], "Interruptible": [], 
        "Gas source": [], "Start": [], "End": [], 'PIST': [], 
        'Border price': [], 'Reajustment formula?': []
    }
    #Patterns for regex search
    patterns = {
        "Destination country": r"País de destino:\s*(.*)",
        "Delievery point": r"Punto de exportación:\s*(.*)",
        "Daily Volume Contracted": r"Cantidad máxima diaria \(en MMm3\):\s*(.*)",
        "Maximum volume": r"Cantidad máxima total \(en MMm3\)\s*[:|:]\s*(.*)",
        "Firm": r"En firme:\s*(.*)",
        "Interruptible": r"Interrumpible:\s*(.*)",
        "Gas source": r"Origen del gas natural \(áreas y yacimiento\):\s*(.*)",
        "Start": r"Fecha de inicio:\s*(\d{2}/\d{2}/\d{4})",
        'End': r"Fecha de fin:\s*(\d{2}/\d{2}/\d{4})",
        'PIST': r"Precio a percibir en el punto de ingreso del transporte:\s*([\d.,]+)",
        'Border price': r'Precio en el punto/puntos de exportación de frontera:\s*([\d.,]+)',
        'Reajustment formula?': r"¿Aplica fórmula de ajuste\?\s*:\s*([A-Za-zÁÉÍÓÚáéíóúñÑ]+)"
    }

    for file in files:
        doc = fitz.open(file)

        #Extracts Buyer (Comprador) and Seller (Vendedor) names directly from file name
        partial_name = file.stem.split(" - ")
        data["Seller"].append(partial_name[1] if len(partial_name) > 1 else "N/A")
        data["Buyer"].append(partial_name[2] if len(partial_name) > 2 else "N/A")

        #Searches data from "patterns" in the PDF file 
        for item, pattern in patterns.items():
            found_names = []
            for page in doc:
                dtext = page.get_text()
                found = re.findall(pattern, dtext)
                found_names.extend(found)
              
            #Appends result on database or "N/A" if not found
            if found_names:
                data[item].append(found_names[0].strip())
            else:
                data[item].append('N/A')
              
    #Generates Excel file database and saves it
    df = pd.DataFrame(data)
    #Translates Spanish
    cols = ['Firm', 'Interruptible', 'Reajustment formula?']
    df[cols] = df[cols].replace({'Si': 'Yes', 'Sí': 'Yes', 'No': 'No'})
    #Saves database
    df.to_excel(folder / 'Licenses_database.xlsx', index=False)
