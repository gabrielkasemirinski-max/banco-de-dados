bateria_atual = 100
bola_em_jogo = True

)
if bateria_atual < 15 and bola_em_jogo:
    print("ALERTA MÁXIMO: Bateria baixa! Substitua a bola na próxima paralisação.")

elif bateria_atual < 15 and not bola_em_jogo:
    print("Aviso: Bateria baixa")

else:
    print("Sistema Trionda operando normalmente. Bateria ok.")
