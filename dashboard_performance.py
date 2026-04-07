import streamlit as st
import MetaTrader5 as mt5
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# ==========================================
# CONFIGURAÇÕES DA PÁGINA WEB
# ==========================================
st.set_page_config(page_title="QuantBridge | Performance", page_icon="📈", layout="wide")
st.title("🏛️ Painel de Performance Institucional - QuantBridge")
st.markdown("Monitoramento em tempo real do P&L (Profit and Loss) do Fundo Quantitativo.")
st.divider()

# ==========================================
# CONEXÃO COM O METATRADER 5
# ==========================================
@st.cache_resource # Evita que o Streamlit fique reconectando a cada clique
def conectar_mt5():
    if not mt5.initialize():
        return False
    return True

if not conectar_mt5():
    st.error("❌ Falha crítica: O MetaTrader 5 precisa estar aberto para carregar os dados.")
    st.stop()

# ==========================================
# EXTRAÇÃO E ENGENHARIA DE DADOS
# ==========================================
# Puxando o histórico dos últimos 30 dias
hoje = datetime.now()
inicio = hoje - timedelta(days=30)
historico_negocios = mt5.history_deals_get(inicio, hoje)

if historico_negocios is None or len(historico_negocios) == 0:
    st.warning("⚠️ Nenhum negócio encontrado no histórico da corretora nos últimos 30 dias.")
    st.stop()

# Convertendo tuplas C++ para DataFrame Pandas
df = pd.DataFrame(list(historico_negocios), columns=historico_negocios[0]._asdict().keys())
df['time'] = pd.to_datetime(df['time'], unit='s')

# Filtrando apenas operações de negociação (excluindo saques/depósitos da corretora)
# E pegando apenas linhas onde o profit é diferente de 0
df_trades = df[(df['type'].isin([mt5.DEAL_TYPE_BUY, mt5.DEAL_TYPE_SELL])) & (df['profit'] != 0)].copy()

if df_trades.empty:
    st.info("Nenhuma operação finalizada com lucro ou prejuízo até o momento.")
    st.stop()

# Criando a Curva de Capital (Soma cumulativa do lucro)
df_trades['P&L Acumulado'] = df_trades['profit'].cumsum()
df_trades['Resultado'] = df_trades['profit'].apply(lambda x: 'Gain' if x > 0 else 'Loss')

# ==========================================
# MÉTRICAS DE TOPO (KPIs INSTITUCIONAIS)
# ==========================================
lucro_total = df_trades['profit'].sum()
total_trades = len(df_trades)
gains = len(df_trades[df_trades['profit'] > 0])
win_rate = (gains / total_trades) * 100 if total_trades > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Resultado Financeiro Acumulado", f"U$ {lucro_total:.2f}", delta=f"{lucro_total:.2f}")
col2.metric("Taxa de Acerto (Win Rate)", f"{win_rate:.1f}%")
col3.metric("Total de Operações", total_trades)
col4.metric("Ativos Operados", df_trades['symbol'].nunique())

st.divider()

# ==========================================
# PLOTAGEM DE GRÁFICOS (PLOTLY)
# ==========================================
col_grafico1, col_grafico2 = st.columns([2, 1])

with col_grafico1:
    st.subheader("📈 Curva de Patrimônio (Equity Curve)")
    # Gráfico de linha mostrando o crescimento (ou queda) da conta
    fig_equity = px.line(df_trades, x='time', y='P&L Acumulado', markers=True, 
                         template='plotly_dark' if st.get_option('theme.base') == 'dark' else 'plotly_white')
    fig_equity.update_traces(line_color='#00FF00' if lucro_total >= 0 else '#FF0000')
    st.plotly_chart(fig_equity, use_container_width=True)

with col_grafico2:
    st.subheader("⚖️ Distribuição Gain vs Loss")
    # Gráfico de pizza para visualização de acertos e erros
    fig_pie = px.pie(df_trades, names='Resultado', color='Resultado', 
                     color_discrete_map={'Gain':'#00cc96', 'Loss':'#ef553b'}, hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("📋 Registro de Operações (Trade Log)")
# Exibindo a tabela com as colunas essenciais
df_exibicao = df_trades[['time', 'symbol', 'type', 'volume', 'price', 'profit', 'comment']].sort_values(by='time', ascending=False)
# Traduzindo o tipo de operação para exibição na tabela
df_exibicao['type'] = df_exibicao['type'].map({mt5.DEAL_TYPE_BUY: 'COMPRA', mt5.DEAL_TYPE_SELL: 'VENDA'})
df_exibicao.columns = ['Data/Hora', 'Ativo', 'Tipo', 'Lotes', 'Preço Executado', 'Lucro/Prejuízo (U$)', 'Comentário']

st.dataframe(df_exibicao, use_container_width=True)