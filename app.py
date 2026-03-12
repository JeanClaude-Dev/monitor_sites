import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def monitorar():
    # Configurações do Navegador
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    
    # Lista de sites para o usuário testar (pode ser alterada aqui antes de gerar o exe)
    sites = {
        "opee": ("https://www.opee.com.br", "body"),
        "não existe": ("https://www.sitenaoexiste.org", "#about")
    }

    print(f"\n{'SITE':<20} | {'STATUS':<10} | {'DETALHES'}")
    print("-" * 60)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    resultados = []

    for nome, (url, seletor) in sites.items():
        try:
            driver.get(url)
            WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor)))
            status = "ONLINE"
            detalhe = "OK"
        except:
            status = "OFFLINE"
            detalhe = "Erro ou Timeout"
        
        print(f"{nome:<20} | {status:<10} | {detalhe}")
        resultados.append([datetime.now(), nome, url, status])

    driver.quit()

    # Salva o log em CSV
    with open("relatorio_testes.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(resultados)

    print("-" * 60)
    print("\n✅ Relatório salvo em 'relatorio_testes.csv'")
    input("\nPressione ENTER para fechar...")



if __name__ == "__main__":
    monitorar()
    
    input("\nTeste finalizado. Pressione Enter para sair...")