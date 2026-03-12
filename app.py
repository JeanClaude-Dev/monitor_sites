#script para rodar teste eno streamlit

import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title("Monitor de Sites 🌐")

# Lista de sites que você quer testar
sites = ["https://www.opee.com.br", "https://www.naoexiste.com"]

if st.button('Iniciar Teste de Status'):
    resultados = []
    for url in sites:
        try:
            inicio = datetime.now()
            response = requests.get(url, timeout=10)
            status = "✅ ONLINE" if response.status_code == 200 else "⚠️ ERRO"
            detalhe = f"Status {response.status_code}"
        except Exception as e:
            status = "❌ OFFLINE"
            detalhe = "Site inacessível"
        
        resultados.append({"Site": url, "Status": status, "Detalhes": detalhe})
    
    # Exibe na tela como uma tabela bonita
    df = pd.DataFrame(resultados)
    st.table(df)
    
    # Botão para baixar o CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Baixar Relatório CSV", csv, "relatorio.csv", "text/csv")