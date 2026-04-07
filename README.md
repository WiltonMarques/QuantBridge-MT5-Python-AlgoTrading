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
