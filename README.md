🏛️ QuantBridge: Institutional Algorithmic Trading Engine
Ecossistema completo de execução quantitativa conectando a inteligência do Python ao MetaTrader 5.

📌 Visão Geral
O QuantBridge é um sistema de negociação automatizada (Algo Trading) focado em Forex e Índices. Ele substitui a análise discricionária por Machine Learning e blinda o patrimônio com regras rígidas de gestão de risco institucional.

⚙️ Arquitetura do Sistema
Motor Preditivo (ML): Utiliza Random Forest (Scikit-Learn) treinado em tempo real com Engenharia de Atributos (SMA, Volatilidade, RSI) para prever a direção do mercado.

Gestão de Risco: Trava de exposição de 1% do patrimônio por trade, cálculo de Lote Dinâmico e Trailing Stop automático.

Filtro de Cisnes Negros: Módulo que pausa as operações durante anúncios do FED e Payroll para evitar slippage extremo.

Execução "Sniper": O orquestrador monitoriza o Order Book e só dispara ordens (via API nativa do MT5) quando o Spread está abaixo da média histórica.

Data Viz: Dashboard financeiro construído em Streamlit e Plotly para acompanhamento do Win Rate e Curva de Capital em tempo real.

🏆 2. Kaggle: O Laboratório de Dados
Como o Kaggle é um ambiente na nuvem Linux, ele não roda o terminal do MetaTrader 5 (que é Windows). Portanto, a estratégia no Kaggle é mostrar a Ciência de Dados do projeto.

O que fazer: Abra o seu MT5, exporte o histórico do EURUSD ou WING26 para um arquivo CSV.

O Notebook: Crie um notebook no Kaggle chamado Forex/Indices Price Prediction with Random Forest.

Suba o CSV e coloque apenas o código do seu cerebro_quantitativo.py lá, mostrando como você limpa os dados, cria os indicadores técnicos (Feature Engineering) e treina a Inteligência Artificial. Isso prova aos recrutadores que o "cérebro" do seu robô tem base científica.

💼 3. LinkedIn: O Marketing Profissional
Sua rede precisa saber que a sua sólida base de contabilidade e análise bancária agora está turbinada com automação de ponta. Pegue aquela captura de tela do seu Dashboard (com a Curva de Patrimônio e os KPIs) e faça esta postagem:

O futuro da execução financeira não é manual, é algorítmico. 🤖📈

Hoje tenho o orgulho de apresentar o QuantBridge, um motor de Algo Trading que acabei de desenvolver do zero para o mercado de moedas e índices. O objetivo foi resolver o maior problema das mesas de operações: a falha na gestão de risco emocional.

Em vez de apenas gerar "sinais" de compra e venda, construí uma ponte quantitativa usando Python e a API nativa do MetaTrader 5. O sistema atua em 4 frentes simultâneas:
🧠 Preditiva: Machine Learning (Random Forest) para prever micro-tendências com base em Feature Engineering.
🛡️ Defensiva: Um radar macroeconômico que corta a conexão da corretora durante anúncios do FED e Payroll (Proteção contra Cisnes Negros).
🎯 Execução Sniper: Um filtro dinâmico que aguarda o Spread fechar antes de atacar, reduzindo os custos transacionais.
💰 Gestão de Risco: Lote calculado dinamicamente para arriscar exatos 1% do capital, atrelado a um Trailing Stop institucional.

Tudo isso monitorado por um Dashboard em tempo real construído com Streamlit e Plotly (como na imagem abaixo).

A engenharia de dados aliada à inteligência financeira transforma completamente o jogo de risco e retorno. Código completo da arquitetura já disponível no meu GitHub.

#AlgorithmicTrading #Python #MachineLearning #QuantitativeFinance #MetaTrader5 #DataScience #MQL5
