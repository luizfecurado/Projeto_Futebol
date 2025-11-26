import os
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.utils.navegador import configurar_navegador
from src.utils.helpers import aceitar_cookies_iframe
from src.utils.helpers import limpar_texto

def processar_artilheiros(navegador, ano):
    ano_id = ano - 1
    ano_real = ano
    print(f"Processando Artilheiros ID {ano} (Temp. {ano_real})...")
    
   # navegador = configurar_navegador() teste pra orquestrar na main
    dados_ano = []

    try:
        url = f"https://www.transfermarkt.co.uk/campeonato-brasileiro-serie-a/torschuetzenliste/wettbewerb/BRA1/saison_id/{ano_id}"
        navegador.get(url)
        aceitar_cookies_iframe(navegador)

        wait = WebDriverWait(navegador, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#yw1 table.items")))
        
        linhas = navegador.find_elements(By.CSS_SELECTOR, "#yw1 table.items > tbody > tr")

        for linha in linhas:
            cols = linha.find_elements(By.XPATH, "./td")
            
            if len(cols) >= 7:
                try:
                    ranking = limpar_texto(cols[0].get_attribute("textContent"))

                    col_info = cols[1]
                    
                    try:
                        nome_jogador = col_info.find_element(By.TAG_NAME, "img").get_attribute("title")
                    except:
                        try:
                            nome_jogador = col_info.find_element(By.CSS_SELECTOR, ".hauptlink a").get_attribute("title")
                        except:
                            nome_jogador = "N/A"

                    try:
                        tabela_interna = col_info.find_element(By.TAG_NAME, "table")
                        linhas_internas = tabela_interna.find_elements(By.TAG_NAME, "tr")
                        posicao = limpar_texto(linhas_internas[-1].get_attribute("textContent"))
                    except:
                        posicao = "N/A"

                    try:
                        nacionalidade = cols[2].find_element(By.TAG_NAME, "img").get_attribute("title")
                    except:
                        nacionalidade = "N/A"

                    idade = limpar_texto(cols[3].get_attribute("textContent"))

                    try:
                        nome_clube = cols[4].find_element(By.TAG_NAME, "a").get_attribute("title")
                    except:
                        try:
                            nome_clube = cols[4].find_element(By.TAG_NAME, "img").get_attribute("title")
                        except:
                            nome_clube = "N/A"

                    jogos = limpar_texto(cols[5].get_attribute("textContent"))

                    gols = limpar_texto(cols[6].get_attribute("textContent"))

                    dados_ano.append({
                        "Ano": ano_real,
                        "Ranking": ranking,
                        "Jogador": nome_jogador,
                        "Posicao": posicao,
                        "Nacionalidade": nacionalidade,
                        "Idade": idade,
                        "Clube": nome_clube,
                        "Jogos": jogos,
                        "Gols": gols
                    })
                except Exception as e:
                    continue

        print(f"Capturado: {len(dados_ano)} artilheiros.")

    except Exception as e:
        print(f"Erro em {ano_id}: {e}")

    #finally:
        #navegador.quit() testar na main
    
    return dados_ano

if __name__ == "__main__":
    anos_id = range(2022,2023)
    todos = []

    for ano in anos_id:
        dados = processar_artilheiros(ano)
        todos.extend(dados)
        time.sleep(2)

    if todos:
        df = pd.DataFrame(todos)
        
        pasta_saida = os.path.join("data", "artilheiros")
        os.makedirs(pasta_saida, exist_ok=True)
        
        caminho_completo = os.path.join(pasta_saida, "artilheiros_brasileirao.csv")
        df.to_csv(caminho_completo, index=False, encoding="utf-8-sig")
        
        print(f"\nSalvo: {caminho_completo}")
        print(df.head())
    else:
        print("Nada extraído.")