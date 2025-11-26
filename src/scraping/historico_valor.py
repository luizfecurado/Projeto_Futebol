import os
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.utils.navegador import configurar_navegador
from src.utils.helpers import aceitar_cookies_iframe
from src.utils.helpers import limpar_texto

def processar_valor_mercado(navegador, ano):
    stichtag = f"{ano}-12-01"
    print(f"Processando valor de mercado em {stichtag}...")
    
   # navegador = configurar_navegador() teste pra orquestrar na main
    dados_ano = []

    try:
        url = f"https://www.transfermarkt.co.uk/campeonato-brasileiro-serie-a/marktwerteverein/wettbewerb/BRA1/plus/?stichtag={stichtag}"
        navegador.get(url)
        aceitar_cookies_iframe(navegador)

        wait = WebDriverWait(navegador, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#yw1 table.items")))
        
        linhas = navegador.find_elements(By.CSS_SELECTOR, "#yw1 table.items > tbody > tr")

        for linha in linhas:
            cols = linha.find_elements(By.XPATH, "./td")
            
            if len(cols) >= 5:
                try:
                    try:
                        nome_clube = cols[2].find_element(By.TAG_NAME, "a").get_attribute("title")
                    except:
                        nome_clube = limpar_texto(cols[2].get_attribute("textContent"))

                    valor_na_data = limpar_texto(cols[4].get_attribute("textContent"))
                    
                    valor_atual = limpar_texto(cols[5].get_attribute("textContent"))

                    dados_ano.append({
                        "Ano": ano,
                        "Data_Referencia": stichtag,
                        "Clube": nome_clube,
                        "Valor_Mercado_Data": valor_na_data,
                        "Valor_Mercado_Atual": valor_atual
                    })
                except Exception as e:
                    continue

        print(f"Capturado: {len(dados_ano)} clubes.")

    except Exception as e:
        print(f"Erro em {ano}: {e}")

    #finally:
        #navegador.quit()
    
    return dados_ano

if __name__ == "__main__":

    anos = range(2024, 2025)
    todos = []

    for ano in anos:
        dados = processar_valor_mercado(ano)
        todos.extend(dados)
        time.sleep(2)

    if todos:
        df = pd.DataFrame(todos)
        
        for col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'\n', '', regex=True).str.strip()

        pasta_saida = os.path.join("data", "valor_mercado")
        os.makedirs(pasta_saida, exist_ok=True)
        
        caminho_completo = os.path.join(pasta_saida, "valor_mercado_brasileirao.csv")
        df.to_csv(caminho_completo, index=False, encoding="utf-8-sig")
        
        print(f"\nSalvo: {caminho_completo}")
        print(df.head())
    else:
        print("Nada extraído.")