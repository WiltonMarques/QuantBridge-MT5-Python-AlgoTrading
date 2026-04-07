import MetaTrader5 as mt5
import time
import numpy as np
from datetime import datetime, timedelta

# Importando os nossos módulos personalizados
from cerebro_quantitativo import obter_sinal_ia
from motor_execucao import executar_ordem
from saida_inteligente import gerenciar_trailing_stop
from filtro_noticias import mercado_seguro_para_operar

# ==========================================
# CONFIGURAÇÕES GLOBAIS DO FUNDO (RISCO & ESTRATÉGIA)
# ==========================================
ATIVO = "EURUSD"
CONFIANCA_CORTE = 0.58          # 58% de certeza mínima da IA para operar
JANELA_EXECUCAO_MINUTOS = 15    # Tempo máximo de paciência do modo Sniper
DISTANCIA_TRAILING = 200        # Pontos de distância para o Stop Loss dinâmico
ATIVACAO_TRAILING = 100         # Pontos de lucro necessários para iniciar a proteção

# Parâmetros da Nova Gestão Institucional
RISCO_POR_TRADE = 1.0           # Arrisca no máx 1% do patrimônio líquido por operação
RISCO_RETORNO_RATIO = 2.5       # Para cada U$1 em risco, busca U$2.50 de lucro
STOP_LOSS_PONTOS = 150          # Tolerância máxima (Stop Loss inicial curto)

# ==========================================
# MÓDULO DE EXECUÇÃO SNIPER (SPREAD DYNAMICS)
# ==========================================
def obter_spread_medio(ativo, amostras=30):
    """ Calcula a média do spread nos últimos segundos para definir o que é um custo 'barato' """
    spreads = []
    for _ in range(amostras):
        tick = mt5.symbol_info_tick(ativo)
        if tick:
            spreads.append(tick.spread)
        time.sleep(0.1) # Coleta rápida
    return np.mean(spreads) if spreads else 999

def aguardar_melhor_spread(ativo, direcao, tempo_limite_min=15):
    """ 
    Monitoriza o custo da corretora e só dispara a ordem quando o spread estiver abaixo da média recente. 
    """
    print(f"🎯 MODO SNIPER: Caçando melhor spread para {direcao}...")
    
    spread_alvo = obter_spread_medio(ativo)
    print(f"📊 Spread Médio Atual: {spread_alvo:.1f} pontos. Alvo: <= {spread_alvo:.1f}")
    
    limite_tempo = datetime.now() + timedelta(minutes=tempo_limite_min)
    
    while datetime.now() < limite_tempo:
        tick = mt5.symbol_info_tick(ativo)
        if tick is None:
            continue
            
        spread_atual = tick.spread
        
        if spread_atual <= spread_alvo:
            print(f"⚡ Spread favorável! Atual: {spread_atual:.1f} | Disparando boleta...")
            
            # 🚨 O MOTOR RECEBE AGORA AS TRAVAS DO LOTE DINÂMICO E RISCO INVERTIDO
            return executar_ordem(
                ativo=ativo, 
                direcao=direcao, 
                risco_por_operacao_pct=RISCO_POR_TRADE, 
                sl_pontos=STOP_LOSS_PONTOS, 
                risco_retorno=RISCO_RETORNO_RATIO
            )
        
        time.sleep(2) # Aguarda antes de checar novamente
    
    print(f"⏰ Tempo limite de {tempo_limite_min}min atingido. Spread muito caro. Abortando sinal.")
    return False

# ==========================================
# ORQUESTRADOR PRINCIPAL (MAESTRO)
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print(f"🤖 ORQUESTRADOR INSTITUCIONAL V3.0 ATIVADO 🤖")
    print(f"📈 Ativo: {ATIVO} | Risco: {RISCO_POR_TRADE}% | R:R -> 1:{RISCO_RETORNO_RATIO}")
    print("=" * 60)

    if not mt5.initialize():
        print("❌ Falha crítica ao conectar com o MT5. Verifique se a plataforma está aberta.")
        quit()

    try:
        while True:
            agora = datetime.now().strftime("%H:%M:%S")
            
            # 1. VERIFICAÇÃO DE ESTADO (Gestão de Risco Contínua)
            posicoes = mt5.positions_get(symbol=ATIVO)
            
            if posicoes:
                # O Foco total passa a ser defender o patrimônio se houver operação aberta
                print(f"[{agora}] 🛡️ MONITORIZANDO LUCRO: Posição ativa em {ATIVO}. (Trailing Stop ON)")
                gerenciar_trailing_stop(ativo=ATIVO, pontos_distancia=DISTANCIA_TRAILING, pontos_ativacao=ATIVACAO_TRAILING)
                
                time.sleep(5) # Verifica o arrasto de Stop a cada 5 segundos
                continue

            # 2. FILTRO DE CISNES NEGROS (Risco Macroeconômico)
            seguro, mensagem_macro = mercado_seguro_para_operar()
            if not seguro:
                print(f"[{agora}] 🛑 {mensagem_macro}")
                time.sleep(60) # Espera 1 minuto e checa o relógio de novo
                continue

            # 3. ANÁLISE PREDITIVA (Busca por oportunidades)
            print(f"[{agora}] 🧠 Caminho limpo de notícias. Solicitando leitura à IA...")
            sinal = obter_sinal_ia(ativo=ATIVO, confianca_minima=CONFIANCA_CORTE)
            
            if sinal != "AGUARDAR":
                print(f"[{agora}] 🚨 SINAL DETECTADO: {sinal}. Iniciando modo Sniper...")
                
                # 4. EXECUÇÃO INTELIGENTE (Músculo em ação)
                sucesso = aguardar_melhor_spread(ativo=ATIVO, direcao=sinal, tempo_limite_min=JANELA_EXECUCAO_MINUTOS)
                
                if sucesso:
                    print(f"[{agora}] ✅ Executado! O monitor de Trailing Stop assumirá a defesa da posição agora.")
                    time.sleep(5) # Uma pequena pausa antes de voltar ao loop inicial de monitoramento
                    continue
            
            # Repouso para não sobrecarregar a máquina e a conexão com a corretora
            time.sleep(30) 

    except KeyboardInterrupt:
        print("\n🛑 Intervenção humana detectada. Desligando o Orquestrador com segurança...")
        mt5.shutdown()