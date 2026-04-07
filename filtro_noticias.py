from datetime import datetime, time

def mercado_seguro_para_operar():
    """
    Bloqueia a negociação durante os horários de maior volatilidade macroeconômica.
    Baseado no fuso horário de Brasília (BRT).
    """
    agora = datetime.now().time()

    # Zonas de Perigo (Cisnes Negros e Alta Volatilidade Institucional)
    zonas_de_perigo = [
        (time(9, 20), time(9, 45)),   # Abertura de NY e Divulgação de Dados (CPI/Payroll)
        (time(14, 50), time(15, 40)), # Discursos do FED (FOMC) e Taxas de Juros
        (time(17, 00), time(18, 30))  # Fechamento de mercado e leilões de liquidez (Spread altíssimo)
    ]

    for inicio, fim in zonas_de_perigo:
        if inicio <= agora <= fim:
            return False, f"ZONA VERMELHA: Risco de Notícia Macro. Aguardando até {fim.strftime('%H:%M')}."

    return True, "Caminho limpo."