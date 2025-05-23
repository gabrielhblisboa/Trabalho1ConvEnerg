import numpy as np
import matplotlib.pyplot as plt

def calcular_amplitudes_harmonicos_vs_angulo_disparo(
    lista_ordens_harmonicas,
    array_angulos_disparo_rad,
    tensao_base=221.11
):
    todas_amplitudes_harmonicos = []
    amplitudes_em_pi_div_dois_rad = []

    for ordem_harmonica in lista_ordens_harmonicas:
        amplitudes_para_harmonica_atual = []
        for angulo_rad in array_angulos_disparo_rad:
            if ordem_harmonica == 1:
                componente_b = (tensao_base / np.pi) * (np.pi - angulo_rad + np.sin(2 * angulo_rad) / 2)
                componente_a = (tensao_base / (2 * np.pi)) * (1 - np.cos(2 * angulo_rad))
            else:
                componente_b = (2 * tensao_base / np.pi) * (
                    (np.sin((ordem_harmonica + 1) * angulo_rad) / (ordem_harmonica + 1)) -
                    (np.sin((ordem_harmonica - 1) * angulo_rad) / (ordem_harmonica - 1))
                )
                termo1_num = np.cos((1 - ordem_harmonica) * np.pi) - np.cos((1 - ordem_harmonica) * angulo_rad)
                termo1_den = ordem_harmonica - 1
                
                termo2_num = np.cos((ordem_harmonica + 1) * angulo_rad) - np.cos((ordem_harmonica + 1) * np.pi)
                termo2_den = ordem_harmonica + 1

                componente_a = (tensao_base / np.pi) * ((termo1_num / termo1_den) - (termo2_num / termo2_den))

            amplitude_atual = np.sqrt(componente_b**2 + componente_a**2)
            amplitudes_para_harmonica_atual.append(amplitude_atual)

            if abs(angulo_rad - np.pi / 2) < 1e-9:
                amplitudes_em_pi_div_dois_rad.append((ordem_harmonica, amplitude_atual))
        
        todas_amplitudes_harmonicos.append(amplitudes_para_harmonica_atual)

    print(amplitudes_em_pi_div_dois_rad)

    return todas_amplitudes_harmonicos


def converter_radianos_para_graus(lista_angulos_rad):
    return [angulo_rad * 180.0 / np.pi for angulo_rad in lista_angulos_rad]

def plotar_dados_harmonicos(
    lista_angulos_graus,
    dados_amplitudes_harmonicos,
    ordens_harmonicas,            
    cores_grafico,                  
    titulo_grafico='Harmônicos de Tensão X Ângulo de Disparo', 
    rotulo_x='Ângulo de Disparo (°)',
    rotulo_y='Amplitude (V)',      
    nome_arquivo_salvar="Grafico_Harmonicos.png"
):
    """Plota as amplitudes dos harmônicos em função dos ângulos de disparo."""
    plt.figure(figsize=(10, 6))

    for i, amplitudes_para_uma_harmonica in enumerate(dados_amplitudes_harmonicos):
        ordem_harmonica_atual = ordens_harmonicas[i]
        plt.plot(
            lista_angulos_graus,
            amplitudes_para_uma_harmonica,
            label=f"{ordem_harmonica_atual}º Harmônico",
            color=cores_grafico[i % len(cores_grafico)]
        )
    
    plt.title(titulo_grafico)
    plt.xlabel(rotulo_x)
    plt.ylabel(rotulo_y)
    plt.legend()
    plt.grid(True)
    if nome_arquivo_salvar:
        plt.savefig(nome_arquivo_salvar)
        print(f"Gráfico salvo como {nome_arquivo_salvar}")
    plt.show()

def principal():
    """
    Função principal para definir parâmetros, calcular amplitudes harmônicas
    e plotar os resultados.
    """
    numero_pontos_angulo = 100
    angulos_disparo_rad = np.linspace(0, np.pi / 2, num=numero_pontos_angulo)
    
    ordens_harmonicas_para_analisar = [1, 3, 5, 7, 9, 11, 13]
    parametro_tensao_base = 221.11

    lista_cores_grafico = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink', 'gray']

    print(f"Calculando amplitudes para os harmônicos: {ordens_harmonicas_para_analisar}")
    print(f"Para ângulos de disparo de 0 a {np.pi/2:.4f} rad ({numero_pontos_angulo} pontos).")

    amplitudes_calculadas = calcular_amplitudes_harmonicos_vs_angulo_disparo(
        lista_ordens_harmonicas=ordens_harmonicas_para_analisar,
        array_angulos_disparo_rad=angulos_disparo_rad,
        tensao_base=parametro_tensao_base
    )

    angulos_disparo_graus = converter_radianos_para_graus(angulos_disparo_rad)

    plotar_dados_harmonicos(
        lista_angulos_graus=angulos_disparo_graus,
        dados_amplitudes_harmonicos=amplitudes_calculadas,
        ordens_harmonicas=ordens_harmonicas_para_analisar,
        cores_grafico=lista_cores_grafico,
        nome_arquivo_salvar="Grafico_Harmonicos.png"
    )

if __name__ == '__main__':
    principal()