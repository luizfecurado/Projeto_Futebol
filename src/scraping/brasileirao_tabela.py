import os
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.utils.navegador import configurar_navegador
from src.utils.helpers import aceitar_cookies_iframe

def processar_tabela(navegador,ano):
    ano_id = ano - 1
    ano_real = ano
   # navegador = configurar_navegador() teste pra orquestrar na main
    dados_ano = []

    try:
        url = f"https://www.transfermarkt.co.uk/campeonato-brasileiro-serie-a/tabelle/wettbewerb/BRA1/plus/?saison_id={ano_id}"
        navegador.get(url)
        aceitar_cookies_iframe(navegador)

        wait = WebDriverWait(navegador, 15)
        tabela = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#yw1 table.items")))
        
        linhas = tabela.find_elements(By.CSS_SELECTOR, "tbody tr")

        for linha in linhas:
            cols = linha.find_elements(By.TAG_NAME, "td")
            
            if len(cols) >= 9:
                try:
                    posicao = cols[0].get_attribute("textContent").strip()
                    
                    try:
                        elem_nome = cols[2].find_element(By.TAG_NAME, "a")
                        nome_clube = elem_nome.get_attribute("title")
                    except:
                        nome_clube = cols[2].get_attribute("textContent").strip()
                    stats = [c.get_attribute("textContent").strip() for c in cols[-7:]]
                    jogos, v, e, d, gols, saldo, pontos = stats

                    dados_ano.append({
                        "Ano": ano_real,
                        "Posicao": posicao,
                        "Clube": nome_clube,
                        "Jogos": jogos,
                        "Vitorias": v,
                        "Empates": e,
                        "Derrotas": d,
                        "Gols": gols,
                        "Saldo": saldo,
                        "Pontos": pontos
                    })
                except:
                    continue

        print(f"Capturado: {len(dados_ano)} times.")

    except Exception as e:
        print(f"Erro em {ano_id}: {e}")

    #finally:
        #navegador.quit()
    
    return dados_ano

if __name__ == "__main__":
    anos_id = range(2023, 2024)
    todos = []

    for ano in anos_id:
        dados = processar_tabela(ano)
        todos.extend(dados)
        time.sleep(2)

    if todos:
        df = pd.DataFrame(todos)
        
        for col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'\n', '', regex=True).str.strip()

        pasta_saida = os.path.join("data", "tabela")
        os.makedirs(pasta_saida, exist_ok=True)
        
        caminho_completo = os.path.join(pasta_saida, "classificacao_brasileirao.csv")
        df.to_csv(caminho_completo, index=False, encoding="utf-8-sig")
        
        print(f"\nSalvo: {caminho_completo}")
        print(df.head())
    else:
        print("Nada extraído.")