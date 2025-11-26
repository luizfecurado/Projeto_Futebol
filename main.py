import os
import time
import pandas as pd
from src.utils.navegador import configurar_navegador
from src.scraping.sem_sofrer_gol import processar_goleiros
from src.scraping.presenca_publico import processar_publico
from src.scraping.historico_valor import processar_valor_mercado
from src.scraping.estrangeiros import processar_estrangeiros
from src.scraping.brasileirao_tabela import processar_tabela
from src.scraping.brasileirao_fora import processar_fora
from src.scraping.brasileirao_casa import processar_casa
from src.scraping.brasileirao_inicial import processar_inicial
from src.scraping.artilheiros import processar_artilheiros

def salvar_dados(dados, pasta, arquivo):
    if not dados:
        print(f"Aviso: Nenhum dado coletado para {arquivo}")
        return

    df = pd.DataFrame(dados)
    
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(r'\n', '', regex=True).str.strip()

    caminho_pasta = os.path.join("data", pasta)
    os.makedirs(caminho_pasta, exist_ok=True)
    
    caminho_completo = os.path.join(caminho_pasta, arquivo)
    df.to_csv(caminho_completo, index=False, encoding="utf-8-sig")
    print(f"💾 Salvo: {caminho_completo} ({len(df)} registros)")

def main():
    ANOS = range(2010, 2026)
    
    TAREFAS = [
        {
            "func": processar_tabela,
            "pasta": "tabela",
            "arquivo": "classificacao_geral.csv",
            "nome": "1. Tabela Geral"
        },
        {
            "func": processar_casa,
            "pasta": "clubes_vitoria_casa",
            "arquivo": "classificacao_mandante.csv",
            "nome": "2. Tabela Mandante"
        },
        {
            "func": processar_fora,
            "pasta": "clubes_vitoria_fora",
            "arquivo": "classificacao_visitante.csv",
            "nome": "3. Tabela Visitante"
        },
        {
            "func": processar_inicial,
            "pasta": "clubes_pag_inicial",
            "arquivo": "resumo_temporadas.csv",
            "nome": "4. Resumo da Temporada"
        },
        {
            "func": processar_publico,
            "pasta": "presenca",
            "arquivo": "media_publico.csv",
            "nome": "5. Média de Público"
        },
        {
            "func": processar_estrangeiros,
            "pasta": "estrangeiros",
            "arquivo": "estrangeiros.csv",
            "nome": "6. Jogadores Estrangeiros"
        },
        {
            "func": processar_artilheiros,
            "pasta": "artilheiros",
            "arquivo": "artilheiros.csv",
            "nome": "7. Artilharia"
        },
        {
            "func": processar_goleiros,
            "pasta": "sem_sofrer_gols",
            "arquivo": "clean_sheets.csv",
            "nome": "8. Goleiros (Clean Sheets)"
        },
        {
            "func": processar_valor_mercado,
            "pasta": "valor_mercado",
            "arquivo": "valor_mercado_historico.csv",
            "nome": "9. Valor de Mercado"
        }
    ]

    print(f"Iniciando automação completa (9 scripts)")
    print(f"Período Real: {ANOS[0]} a {ANOS[-1]}")


    navegador = configurar_navegador()

    try:
        for tarefa in TAREFAS:
            print(f"\nniciando: {tarefa['nome']}...")
            dados_acumulados = []
            
            for ano in ANOS:
                try:                   
                    resultado = tarefa["func"](navegador, ano)
                    
                    if resultado:
                        dados_acumulados.extend(resultado)
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"Erro em {ano}: {e}")

            salvar_dados(dados_acumulados, tarefa["pasta"], tarefa["arquivo"])

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
    
    except Exception as e:
        print(f"\nErro fatal na main: {e}")
        
    finally:
        print("\nProcesso finalizado. Fechando navegador...")
        if 'navegador' in locals():
            navegador.quit()

if __name__ == "__main__":
    main()