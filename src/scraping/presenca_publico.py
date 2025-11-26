import os
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.utils.navegador import configurar_navegador
from src.utils.helpers import aceitar_cookies_iframe

def processar_publico(navegador,ano):
    ano_id = ano - 1
    ano_real = ano
   # navegador = configurar_navegador() teste pra orquestrar na main
    dados_ano = []

    try:
        url = f"https://www.transfermarkt.co.uk/campeonato-brasileiro-serie-a/besucherzahlen/wettbewerb/BRA1/plus/?saison_id={ano_id}"
        navegador.get(url)
        aceitar_cookies_iframe(navegador)

        wait = WebDriverWait(navegador, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#yw1 table.items")))
        
        linhas = tabela = navegador.find_elements(By.CSS_SELECTOR, "#yw1 table.items tbody tr")

        for linha in linhas:

            cols = linha.find_elements(By.XPATH, "./td")

            if len(cols) == 5:
                try:
                    col_info = cols[1]

                    try:
                        nome_clube = col_info.find_element(By.TAG_NAME, "img").get_attribute("title")
                    except:
                        nome_clube = "N/A"

                    try:
                        nome_estadio = col_info.find_element(By.CSS_SELECTOR, ".hauptlink a").get_attribute("text")
                    except:
                        nome_estadio = "N/A"

                    capacidade = cols[2].get_attribute("textContent").strip()
                    total = cols[3].get_attribute("textContent").strip()
                    media = cols[4].get_attribute("textContent").strip()

                    dados_ano.append({
                        "Ano": ano_real,
                        "Clube": nome_clube,
                        "Estadio": nome_estadio,
                        "Capacidade": capacidade,
                        "Publico_Total": total,
                        "Media_Publico": media
                    })
                except Exception as e:
                    print(f"Erro linha: {e}")
                    continue

        print(f"Capturado: {len(dados_ano)} registros.")

    except Exception as e:
        print(f"Erro em {ano_id}: {e}")

    #finally:
        #navegador.quit()
    
    return dados_ano

if __name__ == "__main__":
    anos_id = range(2023, 2024)
    todos = []

    for ano in anos_id:
        dados = processar_publico(ano)
        todos.extend(dados)
        time.sleep(2)

    if todos:
        df = pd.DataFrame(todos)
        
        for col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'\n', '', regex=True).str.strip()

        pasta_saida = os.path.join("data", "presenca")
        os.makedirs(pasta_saida, exist_ok=True)
        
        caminho_completo = os.path.join(pasta_saida, "media_publico_brasileirao.csv")
        df.to_csv(caminho_completo, index=False, encoding="utf-8-sig")
        
        print(f"\nSalvo: {caminho_completo}")
        print(df.head())
    else:
        print("Nada extraído.")