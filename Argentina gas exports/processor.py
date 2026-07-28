import re
import fitz
from pathlib import Path
import pandas as pd

#Reads downloaed PDFs and extracts data via Regex, then compile in Excel spreadsheet.
def scrape_pdf_content(target_dir: str) -> None:
    folder = Path(target_dir)
    files = [f for f in folder.iterdir() if f.suffix == '.pdf']

    #Note 1: PIST stands for molecule price in transport system entry
    data = {
        "ID": [], "Seller": [], "Buyer": [], "Destination country": [], "Delievery point": [], 
        "Daily Volume Contracted": [], "Maximum volume": [], "Firm": [], "Interruptible": [], 
        "Gas source": [], "Start": [], "End": [], 'PIST': [], 
        'Border price': [], 'Reajustment formula?': []
    }

    patterns = {
        "Destination country": r"País de destino:?\s*([\s\S]+?)(?=\n\s*\n|\n[A-ZÁÉÍÓÚ]|$)",
        "Delievery point": r"Punto de exportación:?\s*([\s\S]+?)(?=\n\s*\n|\n[A-ZÁÉÍÓÚ]|$)",
        "Daily Volume Contracted": r"Cantidad máxima diaria \(en MMm3\):\s*(.*)",
        "Maximum volume": r"Cantidad máxima total \(en MMm3\)\s*[:|:]\s*(.*)",
        "Firm": r"En firme:\s*(.*)",
        "Interruptible": r"Interrumpible:\s*(.*)",
        "Gas source": r"Origen del gas natural \(áreas y yacimiento\):\s*(.*)",
        "Start": r"Fecha de inicio:\s*(\d{2}/\d{2}/\d{4})",
        'End': r"Fecha de fin:\s*(\d{2}/\d{2}/\d{4})",
        'PIST': r"Precio a percibir en el punto de ingreso del transporte:\s*([\s\S]+?)(?=\n\n|\n[¿A-ZÁÉÍÓÚ]|$)",
        'Border price': r"Precio en el punto/puntos de exportación de frontera:\s*([\s\S]+?)(?=\n\n|\n[¿A-ZÁÉÍÓÚ]|$)",
        'Reajustment formula?': r"¿Aplica fórmula de ajuste\?\s*:\s*([A-Za-zÁÉÍÓÚáéíóúñÑ]+)"
    }

    for file in files:
        doc = fitz.open(file)

        #Extracts Buyer (Comprador) and Seller (Vendedor) names directly from file name
        partial_name = file.stem.split(" - ")
        data["ID"].append(partial_name[0].strip() if len(partial_name) > 1 else "N/A")
        data["Seller"].append(partial_name[1].strip() if len(partial_name) > 1 else "N/A")
        data["Buyer"].append(partial_name[2].strip() if len(partial_name) > 2 else "N/A")

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
              
    #Generates dataframe
    df = pd.DataFrame(data)

    #Translates Y/N columns in Spanish
    cols_translate = ['ID', 'Firm', 'Interruptible', 'Reajustment formula?']
    df[cols_translate] = df[cols_translate].replace({'Si': 'Yes', 'Sí': 'Yes', 'No': 'No'})

    #Converts numeric values of prices and volumes to float and preserves formulas as strings
    cols_convert = ['Daily Volume Contracted', 'Maximum volume', 'PIST', 'Border price']
    for col in cols_convert:
        df[col] = df[col].apply(parse_mixed_price)

    #Creates transport price as the difference of border price and PIST and replaces it
    df['Transport price'] = df.apply(calculate_transport, axis=1)
    transport_col = df.pop(df.columns[-1])
    df.insert(len(df.columns) - 2, transport_col.name, transport_col)

    #Saves df as excel file
    df.to_excel(folder / 'detailed_gas_licenses_database.xlsx', index=False)

def parse_mixed_price(val):
    val_str = str(val).strip() #text treatment
    temp_str = val_str.replace(',', '.') #decimal adjustment
    
    try:
        return float(temp_str) # converts numerical values to float
    except ValueError:
        return val_str #keeps original string (with formula or note) on error

def calculate_transport(row):
    border = row['Border price']
    pist = row['PIST']
    
    # Calculates transport if both border price and PIST are numbers
    if isinstance(border, (int, float)) and isinstance(pist, (int, float)):
        return round(border - pist, 4)
    else:
        return "N/A"
