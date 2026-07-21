import re
import fitz

#Reads downloaed PDFs and extracts data via Regex, then compile in Excel spreadsheet.
def scrape_pdf_content(target_dir: str) -> None:
    pasta = Path(target_dir)
    arquivos = [f for f in pasta.iterdir() if f.suffix == '.pdf']

    dados = {
        "Vendedor": [], "Comprador": [], "País de destino": [], "Ponto de entrega": [], 
        "QDC": [], "Quantidade máxima": [], "Firme": [], "Interruptível": [], 
        "Origem do gás": [], "Início": [], "Fim": [], 'PIST': [], 
        'Preço Fronteira': [], 'Fórmula de Reajuste?': []
    }

    padroes = {
        "País de destino": r"País de destino:\s*(.*)",
        "Ponto de entrega": r"Punto de exportación:\s*(.*)",
        "QDC": r"Cantidad máxima diaria \(en MMm3\):\s*(.*)",
        "Quantidade máxima": r"Cantidad máxima total \(en MMm3\)\s*[:|:]\s*(.*)",
        "Firme": r"En firme:\s*(.*)",
        "Interruptível": r"Interrumpible:\s*(.*)",
        "Origem do gás": r"Origen del gas natural \(áreas y yacimiento\):\s*(.*)",
        "Início": r"Fecha de inicio:\s*(\d{2}/\d{2}/\d{4})",
        'Fim': r"Fecha de fin:\s*(\d{2}/\d{2}/\d{4})",
        'PIST': r"Precio a percibir en el punto de ingreso del transporte:\s*([\d.,]+)",
        'Preço Fronteira': r'Precio en el punto/puntos de exportación de frontera:\s*([\d.,]+)',
        'Fórmula de Reajuste?': r"¿Aplica fórmula de ajuste\?\s*:\s*([A-Za-zÁÉÍÓÚáéíóúñÑ]+)"
    }

    for arquivo in arquivos:
        doc = fitz.open(arquivo)

        #Extracts buyes (Comprador) and Seller (Vendedor) names directly from file name
        partes_nome = arquivo.stem.split(" - ")
        dados["Vendedor"].append(partes_nome[1] if len(partes_nome) > 1 else "N/A")
        dados["Comprador"].append(partes_nome[2] if len(partes_nome) > 2 else "N/A")

        #Searches data from "padroes" in the PDF file 
        for item, padrao in padroes.items():
            nomes_encontrados = []
            for page in doc:
                texto = page.get_text()
                encontrados = re.findall(padrao, texto)
                nomes_encontrados.extend(encontrados)
              
            #Appends result on database or "N/A" if not found
            if nomes_encontrados:
                dados[item].append(nomes_encontrados[0])
            else:
                dados[item].append('N/A')
              
    #Generates Excel file database and saves it
    df = pd.DataFrame(dados)
    df.to_excel(pasta / 'BD_licencas_Brasil.xlsx', index=False)
