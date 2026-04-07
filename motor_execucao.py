import MetaTrader5 as mt5

def calcular_lote_dinamico(ativo, sl_pontos, risco_pct=1.0):
    """
    Calcula o lote exato para arriscar apenas X% do patrimônio atual.
    """
    conta_info = mt5.account_info()
    if conta_info is None:
        return 0.01 # Lote mínimo de segurança em caso de falha de conexão

    patrimonio = conta_info.equity
    risco_financeiro_maximo = patrimonio * (risco_pct / 100)

    info_ativo = mt5.symbol_info(ativo)
    # Lógica de cálculo de exposição do MT5
    valor_tick = info_ativo.trade_tick_value
    tamanho_tick = info_ativo.trade_tick_size
    point = info_ativo.point

    if valor_tick == 0 or tamanho_tick == 0:
        return 0.01

    # Quanto dinheiro perdemos por cada LOTE se o mercado bater no Stop Loss
    perda_por_lote = sl_pontos * (valor_tick / (tamanho_tick / point))
    
    # Calculando quantos lotes cabem no nosso risco financeiro permitido
    lote_calculado = risco_financeiro_maximo / perda_por_lote

    # Arredondando para as regras da corretora
    lote_step = info_ativo.volume_step
    lote_final = round(lote_calculado / lote_step) * lote_step

    # Garantindo que não exceda os limites do ativo
    return max(info_ativo.volume_min, min(lote_final, info_ativo.volume_max))


def executar_ordem(ativo, direcao, risco_por_operacao_pct=1.0, sl_pontos=150, risco_retorno=2.0):
    """
    Motor Institucional com Inversão de Risco e Lote Dinâmico.
    """
    if not mt5.initialize():
        return False

    mt5.symbol_select(ativo, True)
    info_ativo = mt5.symbol_info(ativo)
    tick = mt5.symbol_info_tick(ativo)
    point = info_ativo.point

    # 1. Relação Risco/Retorno (TP é sempre o dobro ou triplo do SL)
    tp_pontos = sl_pontos * risco_retorno

    # 2. Lote Dinâmico (Tamanho de Posição Inteligente)
    volume_lote = calcular_lote_dinamico(ativo, sl_pontos, risco_pct=risco_por_operacao_pct)

    # 3. Engenharia de Preços
    if direcao == "COMPRA":
        ordem_tipo = mt5.ORDER_TYPE_BUY
        preco = tick.ask
        sl = preco - (sl_pontos * point)
        tp = preco + (tp_pontos * point)
    elif direcao == "VENDA":
        ordem_tipo = mt5.ORDER_TYPE_SELL
        preco = tick.bid
        sl = preco + (sl_pontos * point)
        tp = preco - (tp_pontos * point)
    else:
        return False

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": ativo,
        "volume": float(volume_lote),
        "type": ordem_tipo,
        "price": preco,
        "sl": sl,
        "tp": tp,
        "deviation": 10, # Reduzimos o slippage aceitável para 10 pontos
        "magic": 999111,
        "comment": "QuantBridge AI V2",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    print(f"🚀 Disparo: {direcao} | Lote Dinâmico: {volume_lote:.2f} (Risco 1%) | R:R 1:{risco_retorno}")
    resultado = mt5.order_send(request)

    if resultado.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"⚠️ Ordem Rejeitada. Código: {resultado.retcode}")
        return False
        
    print(f"✅ Executado! SL em {sl:.5f} e TP em {tp:.5f}.")
    return True