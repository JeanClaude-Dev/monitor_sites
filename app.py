import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

import pytz
from datetime import datetime

fuso_sp = pytz.timezone('America/Sao_Paulo')
agora = datetime.now(fuso_sp).strftime("%d/%m/%Y %H:%M:%S")

st.title("Monitor de Sites 🌐")

sites = ["https://www.opee.com.br", "https://capacita.opee.com.br","https://www.opee.com.br/orientacao_profissional","https://opeeloja.opee.com.br","https://www.opee.com.br/lojavirtual","https://metodologia.opee.com.br","https://www.escolaparapais.opee.com.br"]


ARQUIVO_HISTORICO = "historico_testes.csv"

if st.button('Iniciar Teste de Status'):
    novos_resultados_visual = [] # Para a tabela com emojis
    novos_resultados_csv = []    # Para o arquivo sem emojis
    
    #agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    for url in sites:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                status_texto = "ONLINE"
                status_visual = "✅ ONLINE"
            else:
                status_texto = "ERRO"
                status_visual = "⚠️ ERRO"
            detalhe = f"Status {response.status_code}"
        except Exception:
            status_texto = "OFFLINE"
            status_visual = "❌ OFFLINE"
            detalhe = "Site inacessível"
        
        # Dados para exibir na tela (com emoji)
        novos_resultados_visual.append({
            "Data/Hora": agora, "Site": url, "Status": status_visual, "Detalhes": detalhe
        })
        
        # Dados para salvar no CSV (texto puro)
        novos_resultados_csv.append({
            "Data/Hora": agora, "Site": url, "Status": status_texto, "Detalhes": detalhe
        })
    
    # DataFrame para exibição
    df_visual = pd.DataFrame(novos_resultados_visual)
    # DataFrame para processamento/salvamento
    df_novo_csv = pd.DataFrame(novos_resultados_csv)

    # Lógica de acúmulo no arquivo
    if os.path.exists(ARQUIVO_HISTORICO):
        df_antigo = pd.read_csv(ARQUIVO_HISTORICO, sep=",")
        df_final_csv = pd.concat([df_antigo, df_novo_csv], ignore_index=True)
    else:
        df_final_csv = df_novo_csv

    # Salva sem emojis e com a codificação compatível com Excel
    df_final_csv.to_csv(ARQUIVO_HISTORICO, index=False, sep=",", encoding="utf-8-sig")

    # Exibe na tela com emojis para ficar amigável
    st.subheader("Resultados Atuais")
    st.table(df_visual)

    # O botão de download baixa o histórico SEM emojis
    csv_download = df_final_csv.to_csv(index=False, sep=",", encoding="utf-8-sig").encode('utf-8-sig')
    st.download_button(
        label="Baixar Histórico Limpo (CSV)",
        data=csv_download,
        file_name="historico_sites.csv",
        mime="text/csv"
    )

    st.success(f"Teste concluído!")