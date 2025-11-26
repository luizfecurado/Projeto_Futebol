import os
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.utils.navegador import configurar_navegador
from src.utils.helpers import aceitar_cookies_iframe

def processar_inicial(navegador,ano):
    ano_id = ano - 1
    ano_real = ano
    # navegador = configurar_navegador() teste pra orquestrar na main
    dados_ano = []

    try:
        url = f"https://www.transfermarkt.co.uk/campeonato-brasileiro-serie-a/startseite/wettbewerb/BRA1/plus/?saison_id={ano_id}"
        navegador.get(url)
        aceitar_cookies_iframe(navegador)

        wait = WebDriverWait(navegador, 15)
        tabela = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#yw1 table.items")))
        
        linhas = tabela.find_elements(By.CSS_SELECTOR, "tbody tr")

        for linha in linhas:
            cols = linha.find_elements(By.TAG_NAME, "td")
            
            if len(cols) >= 7:
                try:
                    try:
                        elemento_nome = cols[1].find_element(By.TAG_NAME, "a")
                        nome_clube = elemento_nome.get_attribute("title")
                    except:
                        nome_clube = cols[1].get_attribute("textContent")

                    dados_ano.append({
                        "Ano": ano_real,
                        "Clube": nome_clube,
                        "Squad": cols[2].get_attribute("textContent").strip(),
                        "Idade Media": cols[3].get_attribute("textContent").strip(),
                        "Estrangeiros": cols[4].get_attribute("textContent").strip(),
                        "Valor Medio": cols[5].get_attribute("textContent").strip(),
                        "Valor Total": cols[6].get_attribute("textContent").strip()
                    })
                except Exception as e_linha:
                    print(f"Erro")
                    continue

        print(f"   ✅ Capturado: {len(dados_ano)} times de {ano_real}.")

    except Exception as e:
        print(f"   ❌ Erro crítico no ID {ano_id}: {e}")

    #finally:
        #navegador.quit()
    
    return dados_ano

if __name__ == "__main__":
    anos_id = range(2023, 2025) 
    todos = []

    for ano in anos_id:
        dados = processar_inicial(ano)
        todos.extend(dados)
        time.sleep(2)

    if todos:
        df = pd.DataFrame(todos)
        
        colunas = ["Ano", "Clube", "Squad", "Idade Media", "Estrangeiros", "Valor Medio", "Valor Total"]
        df = df[colunas]

        for col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'\n', '', regex=True).str.strip()

        
        pasta_saida = os.path.join("data", "clubes_pag_inicial")
        
        os.makedirs(pasta_saida, exist_ok=True)
        
        caminho_arquivo = os.path.join(pasta_saida, "tabela_brasileirao_final1.csv")

        df.to_csv(caminho_arquivo, index=False, encoding="utf-8-sig")
        
        print(f"\n💾 Salvo com sucesso em:\n  {caminho_arquivo}")
        print(f"   📊 Total de linhas: {len(df)}")
        print(df.head())
    else:
        print("❌ Falha: Nada extraído.")