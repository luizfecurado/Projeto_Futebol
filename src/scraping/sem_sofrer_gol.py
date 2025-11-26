import os
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.utils.navegador import configurar_navegador
from src.utils.helpers import aceitar_cookies_iframe
from src.utils.helpers import limpar_texto

def processar_goleiros(navegador, ano):
    ano_id = ano - 1    
   # navegador = configurar_navegador() teste pra orquestrar na main
    dados_ano = []
    ano_real = ano
    try:
        url = f"https://www.transfermarkt.co.uk/campeonato-brasileiro-serie-a/weisseweste/wettbewerb/BRA1/saison_id/{ano_id}"
        navegador.get(url)
        aceitar_cookies_iframe(navegador)

        wait = WebDriverWait(navegador, 15)
        tabela = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#yw1 table.items")))
        
        linhas = navegador.find_elements(By.CSS_SELECTOR, "#yw1 table.items > tbody > tr")

        for linha in linhas:
            cols = linha.find_elements(By.XPATH, "./td")
            

            if len(cols) >= 5:
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
                         if len(linhas_internas) > 1:
                             clube = limpar_texto(linhas_internas[1].get_attribute("textContent"))
                         else:
                             clube = "N/A"
                    except:
                        clube = "N/A"


                    jogos = limpar_texto(cols[2].get_attribute("textContent"))
                    clean_sheets = limpar_texto(cols[3].get_attribute("textContent"))
                    porcentagem = limpar_texto(cols[4].get_attribute("textContent"))

                    dados_ano.append({
                        "Ano": ano,
                        "Ranking": ranking,
                        "Jogador": nome_jogador,
                        "Clube": clube,
                        "Jogos_Disputados": jogos,
                        "Jogos_Sem_Sofrer_Gol": clean_sheets,
                        "Porcentagem": porcentagem
                    })
                except Exception as e:
                    continue

        print(f"Capturado: {len(dados_ano)} goleiros.")

    except Exception as e:
        print(f"Erro em {ano_id}: {e}")

    #finally:
        #navegador.quit() esta como comentario pra funcionar na main
    
    return dados_ano

if __name__ == "__main__":
    anos_id = range(2022, 2023)
    todos = []

    for ano in anos_id:
        dados = processar_goleiros(ano)
        todos.extend(dados)
        time.sleep(2)

    if todos:
        df = pd.DataFrame(todos)
        
        for col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'\n', '', regex=True).str.strip()

        pasta_saida = os.path.join("data", "sem_sofrer_gols")
        os.makedirs(pasta_saida, exist_ok=True)
        
        caminho_completo = os.path.join(pasta_saida, "clean_sheets_brasileirao.csv")
        df.to_csv(caminho_completo, index=False, encoding="utf-8-sig")
        
        print(f"\nSalvo: {caminho_completo}")
        print(df.head())
    else:
        print("Nada extraído.")