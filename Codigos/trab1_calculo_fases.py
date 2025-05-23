import numpy as np

# ====================== CONFIGURAÇÃO DO SISTEMA ELÉTRICO ======================
def configurar_tensoes():
    """Cria as tensões trifásicas balanceadas"""
    tensao_fase = 127  # Tensão eficaz por fase
    return [
        converter_polar_para_retangular(tensao_fase, 0),
        converter_polar_para_retangular(tensao_fase, 120),
        converter_polar_para_retangular(tensao_fase, 240),
        0  # Referência para o chuveiro
    ]

# ====================== DEFINIÇÃO DOS COMPONENTES ======================
def carregar_dispositivos():
    """Retorna todos os dispositivos elétricos da instalação"""
    return [
        # Fase A
        ['A', 332.56],       # TV 1
        ['A', 332.56],       # TV 2
        ['A', 3291.63],      # Lâmpada 4
        ['A', 3291.63],      # Lâmpada 5
        ['A', 13.44],        # Cooktop 1
        ['A', 13.44],        # Microondas
        ['A', 0.89 + 2.83j], # Ar-condicionado 1
        ['A', 0.89 + 2.83j], # Ar-condicionado 2
        
        # Fase B
        ['B', 10.75],        # Airfryer
        ['B', 13.44],        # Cooktop 2
        ['B', 3291.63],      # Lâmpada 1
        
        # Fase C
        ['C', 13.44],        # Cooktop 3
        ['C', 21.51],        # Computador
        ['C', 3291.63],      # Lâmpada 2
        ['C', 3291.63],      # Lâmpada 3
        ['C', 22.58]         # Geladeira
    ]

# ====================== CÁLCULOS ELÉTRICOS ======================
def determinar_impedancias(dispositivos):
    """Calcula a impedância equivalente para cada fase"""
    condutancia = {'A': 0, 'B': 0, 'C': 0}
    
    for fase, Z in dispositivos:
        condutancia[fase] += 1 / Z
        
    return {fase: 1/condutancia[fase] for fase in ['A', 'B', 'C']}

def montar_matriz_impedancias(Z, Zf, Zc):
    """Constroi a matriz do sistema para cálculo das correntes"""
    return np.array([
        [Z['A']+2*Zf, Zf,       Zf,       Z['A']    ],
        [Zf,       Z['B']+2*Zf, Zf,       0         ],
        [Zf,       Zf,       Z['C']+2*Zf, -Z['C']   ],
        [Z['A'],   0,        -Z['C'],   Zc+Z['B']+Z['C']]
    ], dtype='complex')

# ====================== FUNÇÕES AUXILIARES ======================
def converter_polar_para_retangular(modulo, angulo):
    """Converte coordenadas polares para retangulares"""
    return modulo * np.exp(1j * np.radians(angulo))

# def mostrar_resultados(Z, I, Vn, Vc):
#     """Exibe os resultados formatados"""
#     print("\nIMPEDÂNCIAS EQUIVALENTES:")
#     for fase in ['A', 'B', 'C']:
#         print(f"Z{fase}: {np.abs(Z[fase]):.2f}Ω ∠ {np.angle(Z[fase], deg=True):.2f}°")
    
#     print("\nCORRENTES:")
#     for nome, valor in zip(['Fase A', 'Fase B', 'Fase C', 'Chuveiro'], I):
#         print(f"{nome}: {np.abs(valor):.2f}A ∠ {np.angle(valor, deg=True):.2f}°")
    
#     print(f"\nQueda de tensão no neutro: {np.abs(Vn):.2f}V ∠ {np.angle(Vn, deg=True):.2f}°")
#     print(f"Tensão no chuveiro: {np.abs(Vc):.2f}V ∠ {np.angle(Vc, deg=True):.2f}°")

# # ====================== EXECUÇÃO PRINCIPAL ======================
# if __name__ == "__main__":
    # # Parâmetros do sistema
    # impedancia_fio = 0.086 + 0.38j
    # impedancia_chuveiro = 12.1
    
    # # Configuração do sistema
    # dispositivos = carregar_dispositivos()
    # Z = determinar_impedancias(dispositivos)
    # tensoes = configurar_tensoes()
    
    # # Montagem e solução do sistema
    # matriz_Z = montar_matriz_impedancias(Z, impedancia_fio, impedancia_chuveiro)
    # correntes = np.linalg.solve(matriz_Z, tensoes)
    
    # # Cálculos adicionais
    # corrente_neutro = sum(correntes[:3])
    # queda_tensao_neutro = -impedancia_fio * corrente_neutro
    # tensao_do_chuveiro = impedancia_chuveiro * correntes[3]
    
    # # Apresentação dos resultados
    # mostrar_resultados(Z, correntes, queda_tensao_neutro, tensao_do_chuveiro)

def mostrar_resultados_completos(Z_eq, I_total, V_neutro, dispositivos):
    """Exibe todos os parâmetros elétricos do sistema de forma detalhada"""
    
    print("\n\n================ RELATÓRIO COMPLETO DO SISTEMA ================")
    
    # Seção 1: Impedâncias Equivalentes
    print("\n[1] IMPEDÂNCIAS EQUIVALENTES POR FASE:")
    for fase in ['A', 'B', 'C']:
        print(f"• Z{fase}: {np.abs(Z_eq[fase]):.2f} Ω \t∠ {np.angle(Z_eq[fase], deg=True):.2f}°")
    
    # Seção 2: Análise de Correntes
    print("\n[2] DISTRIBUIÇÃO DE CORRENTES:")
    print(f"• Neutro: {np.abs(I_total['In']):.2f} A \t∠ {np.angle(I_total['In'], deg=True):.2f}°")
    for fase in ['A', 'B', 'C']:
        print(f"• Fase {fase}: {np.abs(I_total[fase]):.2f} A \t∠ {np.angle(I_total[fase], deg=True):.2f}°")
    print(f"• Chuveiro: {np.abs(I_total['Chuveiro']):.2f} A \t∠ {np.angle(I_total['Chuveiro'], deg=True):.2f}°")
    
    # Seção 3: Análise de Tensões
    print("\n[3] DISTRIBUIÇÃO DE TENSÕES:")
    print(f"• Queda no Neutro: {np.abs(V_neutro):.2f} V \t∠ {np.angle(V_neutro, deg=True):.2f}°")
    for fase in ['A', 'B', 'C']:
        V_fase = dispositivos[fase]['Z'] * I_total[fase]
        print(f"• Fase {fase}: {np.abs(V_fase):.2f} V \t∠ {np.angle(V_fase, deg=True):.2f}°")
    print(f"• Chuveiro: {np.abs(dispositivos['Chuveiro']['V']):.2f} V \t∠ {np.angle(dispositivos['Chuveiro']['V'], deg=True):.2f}°")

# Modificação na execução principal
if __name__ == "__main__":
        # Parâmetros do sistema
    impedancia_fio = 0.086 + 0.38j
    impedancia_chuveiro = 12.1
    
    # Configuração do sistema
    dispositivos = carregar_dispositivos()
    Z = determinar_impedancias(dispositivos)
    tensoes = configurar_tensoes()
    
    # Montagem e solução do sistema
    matriz_Z = montar_matriz_impedancias(Z, impedancia_fio, impedancia_chuveiro)
    correntes = np.linalg.solve(matriz_Z, tensoes)
    
    # Cálculos adicionais
    corrente_neutro = sum(correntes[:3])
    queda_tensao_neutro = -impedancia_fio * corrente_neutro
    tensao_do_chuveiro = impedancia_chuveiro * correntes[3]
    
    # Preparação dos dados para exibição
    resultados = {
        'Z_eq': Z,
        'I_total': {
            'A': correntes[0],
            'B': correntes[1],
            'C': correntes[2],
            'Chuveiro': correntes[3],
            'In': corrente_neutro
        },
        'V_neutro': queda_tensao_neutro,
        'dispositivos': {
            'A': {'Z': Z['A']},
            'B': {'Z': Z['B']},
            'C': {'Z': Z['C']},
            'Chuveiro': {'V': tensao_do_chuveiro}
        }
    }
    
    mostrar_resultados_completos(**resultados)