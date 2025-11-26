<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Projeto Futebol - Web Scraping Transfermarkt</title>
<style>
    body {
        font-family: Arial, Helvetica, sans-serif;
        line-height: 1.6;
        padding: 20px;
        max-width: 900px;
        margin: auto;
        color: #222;
        background: #fafafa;
    }
    h1, h2, h3 {
        color: #1a73e8;
    }
    pre {
        background: #1e1e1e;
        padding: 15px;
        border-radius: 8px;
        color: #f8f8f2;
        overflow-x: auto;
        font-size: 14px;
    }
    ul {
        margin-left: 20px;
    }
    .section {
        margin-top: 35px;
    }
    .tag {
        display: inline-block;
        background: #1a73e8;
        color: white;
        padding: 3px 8px;
        border-radius: 5px;
        font-size: 12px;
        margin-right: 6px;
    }
</style>
</head>

<body>

<h1>⚽ Projeto Futebol – Web Scraping Transfermarkt (Brasileirão)</h1>

<p>
Este é um projeto completo de automação em <strong>Python</strong> para coleta de dados estatísticos do 
<strong>Campeonato Brasileiro Série A</strong> diretamente do site 
<strong>Transfermarkt</strong>. Ele percorre temporadas históricas 
(de 2010 a 2025 por padrão) e salva cada conjunto de dados em arquivos CSV organizados.
</p>

<div class="section">
<h2>🚀 Funcionalidades Atuais</h2>
<ul>
    <li>📊 <strong>Classificação Geral</strong></li>
    <li>🏟️ <strong>Tabela Mandante</strong></li>
    <li>🚍 <strong>Tabela Visitante</strong></li>
    <li>🧩 <strong>Resumo da Temporada</strong></li>
    <li>👥 <strong>Média de Público</strong></li>
    <li>🌎 <strong>Jogadores Estrangeiros</strong></li>
    <li>🎯 <strong>Artilharia</strong></li>
    <li>🛡️ <strong>Clean Sheets (Goleiros)</strong></li>
    <li>💰 <strong>Valor de Mercado</strong></li>
</ul>
</div>

<div class="section">
<h2>🛠️ Arquitetura e Lógica do Projeto</h2>

<ul>
    <li><span class="tag">main.py</span> Orquestra a execução completa do pipeline.</li>
    <li><span class="tag">Correção Automática</span> Ajusta a temporada devido ao calendário europeu do Transfermarkt.</li>
    <li><span class="tag">Extração Robusta</span> Selectors CSS + XPath para buscar dados complexos.</li>
    <li><span class="tag">Alta Resiliência</span> Reinicia o navegador automaticamente em falhas.</li>
</ul>
</div>

<div class="section">
<h2>📂 Estrutura Completa do Projeto</h2>

<pre>Projeto_Futebol/
├── main.py                      # Script principal (Orquestrador)
├── requirements.txt             # Dependências do projeto
│
├── data/                        # Dados brutos extraídos (CSV)
│   ├── artilheiros/             # Artilharia
│   ├── clubes_pag_inicial/      # Resumo geral dos clubes
│   ├── clubes_vitoria_casa/     # Tabela Mandante
│   ├── clubes_vitoria_fora/     # Tabela Visitante
│   ├── estrangeiros/            # Jogadores estrangeiros
│   ├── kaggle/                  # Dados auxiliares
│   ├── presenca/                # Média de público e ocupação
│   ├── sem_sofrer_gols/         # Clean Sheets (goleiros)
│   ├── tabela/                  # Classificação geral
│   └── valor_mercado/           # Histórico financeiro
│
└── src/
    ├── scraping/                # Scripts de scraping (9 módulos)
    ├── utils/                   # Configurações do navegador, helpers, logs
    ├── transformation/          # [FUTURO] Limpeza e padronização
    └── loading/                 # [FUTURO] Carga em bancos de dados / DW
</pre>
</div>

<div class="section">
<h2>🚧 Próximos Passos (Roadmap)</h2>

<h3>🔹 Transformation</h3>
<p>
Será responsável por padronizar campos, corrigir tipos de dados, remover inconsistências
e integrar tabelas para análises mais avançadas.
</p>

<h3>🔹 Loading</h3>
<p>
Envio automático dos dados tratados para:
</p>
<ul>
    <li>PostgreSQL</li>
    <li>MySQL</li>
    <li>BigQuery</li>
    <li>Redshift</li>
    <li>DuckDB</li>
    <li>Data Warehouse corporativo</li>
</ul>
</div>

<div class="section">
<h2>⚙️ Instalação e Uso</h2>

<p><strong>Pré-requisitos:</strong></p>
<ul>
    <li>Python 3.10+</li>
    <li>Google Chrome instalado</li>
</ul>

<h3>📦 Instalar dependências</h3>
<pre>pip install -r requirements.txt</pre>

<h3>▶ Executar o projeto</h3>
<pre>python main.py</pre>
</div>

<div class="section">
<h2>📊 Resultado</h2>
<p>
Após a execução completa, a pasta <code>data/</code> conterá arquivos CSV históricos,
prontos para uso em:
</p>

<ul>
    <li>Excel</li>
    <li>Power BI</li>
    <li>Pandas</li>
    <li>Dashboards e Modelos de Machine Learning</li>
</ul>
</div>

</body>
</html>
