import os
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.utils.navegador import configurar_navegador
from src.utils.helpers import aceitar_cookies_iframe

def processar_estrangeiros(navegador, ano):
    ano_id = ano - 1
    ano_real = ano    
   # navegador = configurar_navegador() teste pra orquestrar na main
    dados_ano = []

    try:
        url = f"https://www.transfermarkt.co.uk/campeonato-brasileiro-serie-a/legionaereeinsaetze/wettbewerb/BRA1/plus/?option=spiele&saison_id={ano_id}&altersklasse=alle"
        navegador.get(url)
        aceitar_cookies_iframe(navegador)

        wait = WebDriverWait(navegador, 15)
        tabela = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#yw1 table.items")))
        
        linhas = tabela.find_elements(By.CSS_SELECTOR, "tbody tr")

        for linha in linhas:
            cols = linha.find_elements(By.TAG_NAME, "td")

            if len(cols) >= 5:
                try:
                    try:
                        nome_clube = cols[1].find_element(By.TAG_NAME, "a").get_attribute("title")
                    except:
                        nome_clube = cols[1].get_attribute("textContent").strip()
                    jogadores = cols[2].get_attribute("textContent").strip()
                    min_nacionais = cols[3].get_attribute("textContent").strip()
                    min_estrangeiros = cols[4].get_attribute("textContent").strip()

                    dados_ano.append({
                        "Ano": ano_real,
                        "Clube": nome_clube,
                        "Jogadores_Usados": jogadores,
                        "Minutos_Nacionais": min_nacionais,
                        "Minutos_Estrangeiros": min_estrangeiros
                    })
                except Exception as e:
                    print(f"Erro na linha: {e}")
                    continue

        print(f"Capturado: {len(dados_ano)} times.")

    except Exception as e:
        print(f"Erro em {ano_id}: {e}")

    #finally:
       # navegador.quit()
    
    return dados_ano

if __name__ == "__main__":
    anos_id = [2022, 2023, 2024]
    todos = []

    for ano in anos_id:
        dados = processar_estrangeiros(ano)
        todos.extend(dados)
        time.sleep(2)

    if todos:
        df = pd.DataFrame(todos)
        
        for col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'\n', '', regex=True).str.strip()

        pasta_saida = os.path.join("data", "estrangeiros") 
        os.makedirs(pasta_saida, exist_ok=True)
        
        caminho_completo = os.path.join(pasta_saida, "uso_jogadores_estrangeiros.csv")
        df.to_csv(caminho_completo, index=False, encoding="utf-8-sig")
        
        print(f"\nSalvo: {caminho_completo}")
        print(df.head())
    else:
        print("Nada extraído.")