import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def contar_ocorrencias(data):
    # Inicializa um dicionário para armazenar o número de ocorrências por variável
    ocorrencias_por_variavel = {}

    # Itera sobre cada coluna (variável)
    for coluna in data.columns:
        # Conta as ocorrências de cada símbolo (valor único) na coluna
        valores_unicos, contagem = np.unique(data[coluna], return_counts=True)
        # Armazena no dicionário o resultado da coluna
        ocorrencias = {valor: count for valor, count in zip(valores_unicos, contagem) if count != 0}
        ocorrencias_por_variavel[coluna] = ocorrencias
    
    return ocorrencias_por_variavel

def main():

    # Load the Excel file
    exelFile = "CarDataset.xlsx"
    data = pd.read_excel(exelFile)

    varNames = data.columns.values.tolist()

    j = 0


    for i in varNames:
        if i != "MPG":
            plt.subplot(3, 2, j+1)
            plt.plot(data[i], data["MPG"], ".m")
            plt.title(f"MPG vs {i}")
            plt.xlabel(i)
            plt.ylabel("MPG")
            j += 1
            
        if j >= 6:
            break

    # Ajustar layout
    plt.subplots_adjust(hspace=1.4)
    plt.subplots_adjust(wspace=0.5)

    plt.show()

    # Converter dados para uint16
    data_uint16 = data.astype(np.uint16)

    # Converter o DataFrame para um array NumPy
    array_data = data_uint16.to_numpy()

    # Inicializar conjunto para o alfabeto geral
    alfabeto_geral = set()

    #criar o alfabeto
    for i in range(pow(2, 16) -1):
        alfabeto_geral.update([i])
    
    print(alfabeto_geral)

    # Iterar sobre cada coluna e obter os valores únicos
    #for coluna in range(array_data.shape[1]):  # Itera sobre as colunas
    #    valores_unicos = np.unique(array_data[:, coluna])
    #    alfabeto_geral.update(valores_unicos)

    # Converter o alfabeto para uma lista
    alfabeto_geral = list(alfabeto_geral)
    

    # Obter o número de ocorrências para cada variável
    ocorrencias = contar_ocorrencias(data_uint16)

    # Imprimir o resultado
    for variavel, ocor in ocorrencias.items():
        print(f"Ocorrências para {variavel}:")
        for valor, contagem in ocor.items():
            print(f"  Valor {valor}: {contagem} ocorrências")
        
    
        # Criar gráfico de barras somente com ocorrências diferentes de 0
        plt.bar(list(ocor.keys()), list(ocor.values()), color="red", align="center")
        plt.xlabel(variavel)
        plt.ylabel("Contagem")
        
        # Centralizar os ticks do eixo x
        plt.xticks(ticks=list(ocor.keys()), labels=list(ocor.keys()))
        plt.tight_layout()
        
        plt.show()



if __name__ == "__main__":
    main()
