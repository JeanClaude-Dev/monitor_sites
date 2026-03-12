import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

st.title("Monitor de Sites 🌐")

# Lista de sites que você quer testar
sites = ["https://www.opee.com.br", "https://www.google.com"]

# Nome do arquivo onde o histórico será salvo no servidor do Streamlit
ARQUIVO_HISTORICO = "historico_testes.csv"

if st.button('Iniciar Teste de Status'):
    novos_resultados = []
    # Captura data e hora atual formatada
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    for url in sites:
        try:
            response = requests.get(url, timeout=10)
            status = "✅ ONLINE" if response.status_code == 200 else "⚠️ ERRO"
            detalhe = f"Status {response.status_code}"
        except Exception:
            status = "❌ OFFLINE"
            detalhe = "Site inacessível"
        
        # Adiciona a data e hora em cada linha
        novos_resultados.append({
            "Site": url, 
            "Data/Hora": agora, 
            "Status": status, 
            "Detalhes": detalhe
        })
    
    # Criar DataFrame com os novos dados
    df_novo = pd.DataFrame(novos_resultados)

    # LÓGICA DE ACUMULAR: Verifica se o arquivo já existe
    if os.path.exists(ARQUIVO_HISTORICO):
        # Lê o histórico existente
        df_antigo = pd.read_csv(ARQUIVO_HISTORICO, sep=",")
        # Junta o antigo com o novo (append)
        df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
    else:
        # Se não existe, o histórico é apenas o resultado atual
        df_final = df_novo

    # Salva no "disco" do servidor (separado por vírgula)
    df_final.to_csv(ARQUIVO_HISTORICO, index=False, sep=",")

    # Exibe na tela (os resultados mais recentes primeiro para facilitar a leitura)
    st.subheader("Resultados Atuais")
    st.table(df_novo)

    # Botão para baixar o histórico COMPLETO acumulado
    csv_download = df_final.to_csv(index=False, sep=",").encode('utf-8')
    st.download_button(
        label="Baixar Histórico Acumulado (CSV)",
        data=csv_download,
        file_name="historico_sites.csv",
        mime="text/csv"
    )

    st.success(f"Teste concluído! O histórico agora tem {len(df_final)} registros.")