import MetaTrader5 as mt5

def gerenciar_trailing_stop(ativo, pontos_distancia=150, pontos_ativacao=50):
    """
    Monitora a posição aberta e ajusta o Stop Loss à medida que o preço avança.
    - pontos_distancia: A distância que o SL deve manter do preço atual.
    - pontos_ativacao: Quantos pontos de lucro são necessários para começar a arrastar.
    """
    posicoes = mt5.positions_get(symbol=ativo)
    
    if posicoes is None or len(posicoes) == 0:
        return

    for pos in posicoes:
        ticket = pos.ticket
        tipo = pos.type
        preco_atual = pos.price_current
        sl_atual = pos.sl
        preco_abertura = pos.price_open
        point = mt5.symbol_info(ativo).point

        # LÓGICA PARA POSIÇÃO DE COMPRA (BUY)
        if tipo == mt5.POSITION_TYPE_BUY:
            # Verifica se o preço já subiu o suficiente para ativar o trailing
            if (preco_atual - preco_abertura) > (pontos_ativacao * point):
                novo_sl = preco_atual - (pontos_distancia * point)
                
                # O novo SL só é aplicado se for MAIOR que o SL atual (proteção de lucro)
                if novo_sl > sl_atual:
                    request = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "symbol": ativo,
                        "sl": novo_sl,
                        "tp": pos.tp,
                        "position": ticket
                    }
                    resultado = mt5.order_send(request)
                    if resultado.retcode == mt5.TRADE_RETCODE_DONE:
                        print(f"📈 [TRAILING BUY] Novo SL definido para: {novo_sl:.5f}")

        # LÓGICA PARA POSIÇÃO DE VENDA (SELL)
        elif tipo == mt5.POSITION_TYPE_SELL:
            # Verifica se o preço já caiu o suficiente para ativar o trailing
            if (preco_abertura - preco_atual) > (pontos_ativacao * point):
                novo_sl = preco_atual + (pontos_distancia * point)
                
                # O novo SL só é aplicado se for MENOR que o SL atual ou se for zero
                if novo_sl < sl_atual or sl_atual == 0:
                    request = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "symbol": ativo,
                        "sl": novo_sl,
                        "tp": pos.tp,
                        "position": ticket
                    }
                    resultado = mt5.order_send(request)
                    if resultado.retcode == mt5.TRADE_RETCODE_DONE:
                        print(f"📉 [TRAILING SELL] Novo SL definido para: {novo_sl:.5f}")