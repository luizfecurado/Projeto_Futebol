import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

def aceitar_cookies_iframe(navegador: WebDriver) -> bool:
    try:
        iframe = WebDriverWait(navegador, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='consent']"))
        )
        navegador.switch_to.frame(iframe)

        botao = WebDriverWait(navegador, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Accept & continue']]"))
        )
        botao.click()
        
        navegador.switch_to.default_content()
        print("Botão clicado")
        return True
        
    except TimeoutException:
        navegador.switch_to.default_content()
        return False
    except Exception as e:
        navegador.switch_to.default_content()
        return False

def salvar_dados(df: pd.DataFrame, output_path: str) -> None:
    if df.empty:
        print(f"Nenhum dado para salvar em {output_path}.")
        return

    try:
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Diretório criado: {output_dir}")
        
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"\nCSV salvo com {len(df)} registros em: {output_path}")

    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

def limpar_texto(texto):
    if texto:
        return " ".join(texto.split())
    return ""