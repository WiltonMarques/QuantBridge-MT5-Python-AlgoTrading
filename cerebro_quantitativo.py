import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import warnings

warnings.filterwarnings("ignore")

def obter_sinal_ia(ativo, timeframe=mt5.TIMEFRAME_M15, velas=2000, confianca_minima=0.55):
    """
    Treina o modelo em tempo real e retorna 'COMPRA', 'VENDA' ou 'AGUARDAR'.
    """
    rates = mt5.copy_rates_from_pos(ativo, timeframe, 0, velas)
    if rates is None:
        return "AGUARDAR"
        
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)

    # Feature Engineering
    df['SMA_10'] = df['close'].rolling(window=10).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['Volatilidade'] = df['high'] - df['low']
    
    delta = df['close'].diff()
    ganho = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    perda = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = ganho / perda
    df['RSI'] = 100 - (100 / (1 + rs))

    df['Target'] = np.where(df['close'].shift(-1) > df['close'], 1, 0)
    df.dropna(inplace=True)

    # Preparação para IA
    features = ['open', 'high', 'low', 'close', 'tick_volume', 'SMA_10', 'SMA_50', 'Volatilidade', 'RSI']
    X = df[features]
    y = df['Target']

    # Treino rápido
    modelo = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    modelo.fit(X.iloc[:-1], y.iloc[:-1]) # Treina sem usar a vela atual para não trapacear

    # Previsão da vela atual
    dados_atuais = X.iloc[-1:]
    sinal = modelo.predict(dados_atuais)[0]
    probabilidade = modelo.predict_proba(dados_atuais)[0]
    
    confianca = probabilidade[1] if sinal == 1 else probabilidade[0]

    # Filtro Institucional: Só opera se a IA tiver certeza acima do limite
    if confianca >= confianca_minima:
        return "COMPRA" if sinal == 1 else "VENDA"
    else:
        return "AGUARDAR"