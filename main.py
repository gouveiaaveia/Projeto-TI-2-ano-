import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calcular_ocorrencias(data, alfabeto):
    # Obter o número de ocorrências para cada variável
    ocorrencias = contar_ocorrencias(data, alfabeto)

    # Imprimir e plotar o resultado
    for i, (variavel, ocor) in enumerate(ocorrencias.items()):
        print(f"Ocorrências para {variavel}:")
        for idx, valor in enumerate(alfabeto):
            if ocor[idx] > 0:
                print(f"  Valor {valor}: {ocor[idx]} ocorrências")
        
        # Criar gráfico de barras somente com ocorrências diferentes de 0
        valores_presentes = alfabeto[ocor > 0]  # Filtra valores presentes no alfabeto
        contagens_presentes = ocor[ocor > 0]    # Filtra as contagens diferentes de 0

        plt.bar(valores_presentes.astype(str), contagens_presentes, color="red", align="center")
        plt.xlabel(variavel)
        plt.ylabel("Contagem")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    # Adicione o retorno das ocorrências aqui
    return ocorrencias

def contar_ocorrencias(data, alfabetoGerral):
    ocorrencias_por_variavel = {}
    for coluna in data.columns:
        contagem = np.zeros(len(alfabetoGerral), dtype=np.uint16)
        valores_unicos, contagem_valores = np.unique(data[coluna], return_counts=True)

        # Adicione uma impressão para verificar os valores únicos
        print(f"Valores únicos na coluna {coluna}: {valores_unicos}")

        indices = np.searchsorted(alfabetoGerral, valores_unicos)

        # Imprima os índices correspondentes
        print(f"Índices correspondentes para {coluna}: {indices}")

        # Atualiza a contagem
        np.add.at(contagem, indices, contagem_valores)
        ocorrencias_por_variavel[coluna] = contagem
    
    return ocorrencias_por_variavel

def binning(data, coluna, alfabeto, num_simbolos, ocorrencias):
    #dividir o alfabeto em intervalos de acordo com o número de símbolos
    intervalos = np.array_split(alfabeto, len(alfabeto)/num_simbolos)
    nova_coluna = data[coluna].copy()
    
    for idx, valor_original in enumerate(data[coluna]):
        for intervalo in intervalos:
            if intervalo[0] <= valor_original <= intervalo[-1]:
                indices = np.isin(alfabeto, intervalo)
                valores_frequentes = alfabeto[indices]
                frequencias = ocorrencias[indices]

                # Imprima para verificar as frequências
                print(f"Frequências para intervalo {intervalo}: {frequencias}")

                # Verifique se frequências está vazio
                if np.any(frequencias):
                    valor_mais_frequente = valores_frequentes[np.argmax(frequencias)]
                    nova_coluna.iloc[idx] = valor_mais_frequente
                else:
                    print(f"Aviso: Nenhuma frequência encontrada para o intervalo {intervalo}")
                break

    return nova_coluna

def calculo_medio(data):

    # Calcula a entropia para cada coluna individualmente
    for coluna in data.columns:
        # Normalizar para calcular as probabilidades (soma dos valores da coluna tem que ser 1)
        valores_norm = data[coluna] / np.sum(data[coluna])
        
        # Cálculo da entropia para a coluna
        entropia_coluna = -np.sum(valores_norm * np.log2(valores_norm))
        
        print(f"Média (entropia) para {coluna}: {round(entropia_coluna, 2)}")


    # Calcula a média total considerando todas as colunas juntas
    data_flat = data.values.flatten()
    valores_totais_norm = data_flat / np.sum(data_flat)
    media_total = -np.sum(valores_totais_norm * np.log2(valores_totais_norm))

    print(f"Média total (entropia considerando todas as colunas juntas): {round(media_total, 2)}")

def huffmaan(data): 
    for coluna in data.columns:
        # Construir o codec de Huffman a partir dos dados da coluna
        codec = huffc.HuffmanCodec.from_data(data[coluna])
        
        # Obter os símbolos e comprimentos dos códigos
        symbols, lengths = codec.get_code_len() #symbols é cada numero do abcedario em cada coluna
                                                #se um simbolo tem 00 em binario a length é 2 bits
        
        # Calcular as frequências dos símbolos na coluna 
        frequencias = data[coluna].value_counts().reindex(symbols, fill_value=0).values

        # Normalizar as frequências para obter as probabilidades
        probabilidades = frequencias / np.sum(frequencias)

        # Calcular o valor médio de bits por símbolo
        L_media = np.sum(probabilidades * lengths)

        # Calcular a variância ponderada
        variancia_ponderada = np.sum(probabilidades * (lengths - L_media) ** 2)  #tem uma formula(ver)

        print(f"Coluna: {coluna}, Valor médio de bits por símbolo: {L_media:.2f} bits")
        print(f"Simbolo: {symbols}, tamanho: {lengths}")
        print(f"Variância ponderada dos comprimentos: {variancia_ponderada:.2f}\n")

def main():
    # Carregar o arquivo Excel
    exelFile = "CarDataset.xlsx"
    data = pd.read_excel(exelFile)

    varNames = data.columns.values.tolist() #[nome_coluna...]

    # Plotar gráficos MPG vs outras variáveis
    j = 0
    for i in range(len(varNames) - 1):
        plt.subplot(3, 2, j+1)
        plt.plot(data[varNames[i]], data["MPG"], ".m")
        plt.title(f"MPG vs {varNames[i]}")
        plt.xlabel(varNames[i])
        plt.ylabel("MPG")
        j += 1

    plt.subplots_adjust(hspace=1.4)
    plt.subplots_adjust(wspace=0.5)
    plt.show()

    # Converter dados para uint16
    data_uint16 = data.astype(np.uint16)

    # Criar o alfabeto como um intervalo de uint16
    alfabeto_geral = np.arange(0, 2**16 - 1, dtype=np.uint16)

    # Calcular e plotar as ocorrências
    ocorrencias_por_variavel = calcular_ocorrencias(data_uint16, alfabeto_geral)

    # Aplicar binning nas colunas e salvar as colunas binned no DataFrame
    data_uint16["Weight_binned"] = binning(data_uint16, "Weight", alfabeto_geral, 5, ocorrencias_por_variavel["Weight"])
    data_uint16["Displacement_binned"] = binning(data_uint16, "Displacement", alfabeto_geral, 5, ocorrencias_por_variavel["Displacement"])
    data_uint16["Horsepower_binned"] = binning(data_uint16, "Horsepower", alfabeto_geral, 5, ocorrencias_por_variavel["Horsepower"])

    # Calcular e plotar as ocorrências para os novos valores binned
    colunas_binned = ["Weight_binned", "Displacement_binned", "Horsepower_binned"]
    ocorrencias_binned = calcular_ocorrencias(data_uint16[colunas_binned], alfabeto_geral)

    # Calcular a média
    calculo_medio(data_uint16)
    huffmaan(data)
