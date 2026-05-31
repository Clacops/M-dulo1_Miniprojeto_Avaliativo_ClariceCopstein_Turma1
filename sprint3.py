# %% [markdown]
# Sprint 3 (Limpeza de Nulos e Duplicatas): Aplicação das condicionais e funções  para identificação e substituição de valores vazios e  de str para valores de data tipo datetime, na tabela de varejo. 
# 1.	Buscando não conformidades: valores N/D
# 2.	Número e Percentual de não conformidades N/D
# 3.	Momento: Decisão de exclusão?
# 4.	Buscando não conformidades : valores duplicados
# 5.	Número e Percentual de não conformidades : valores duplicados
# 6.	Momento: Decisão de exclusão ou Ajuste?
# 7.	Buscando não conformidades: valores nulos
# 8.	Número e Percentual de não conformidades  valores nulos
# 9.	Momento: Decisão de exclusão ou Ajuste?
# 
# 

# %%

import pandas as pd
import re

print("\n" + "="*65)
print(" INVESTIGAÇÃO DE VALORES 'N/D'")
print("="*65)

#  Carregar a base do Sprint 1
print("-> Carregando a base de dados...")
df = pd.read_csv('base_varejo_sprint2.csv', sep=',')
print("-> Base de dados carregada com sucesso!")

# Definindo numero anterior de linhas para comparação
total_linhas = len(df)
print(f"-> Total de registros na base: {total_linhas}")

# Buscando a string 'N/D' nas colunas de texto
# Verificando os valores únicos na coluna PR_CAT para entender a diversidade de categorias
print('\nValores únicos na coluna PR_CAT:')
print("="*65)
print(df["PR_CAT"].unique())
print("="*65)

# Verifica em quantas linhas o PR_NOME é exatamente igual ao PR_CAT
linhas_iguais = (df['PR_NOME'] == df['PR_CAT']).sum()
print(f"-> Existem {linhas_iguais} linhas onde o Nome do Produto é uma cópia idêntica da Categoria.")

# 4. Localizando o erro '#N/D' que descobrimos na base
filtro_erro = (df['PR_CAT'] == '#N/D') | (df['PR_NOME'] == '#N/D')
linhas_com_erro = df[filtro_erro]

# Contagem exata buscando apenas o termo textual idêntico a '#N/D'
total_linhas = len(df)
total_nd_real = len(linhas_com_erro)
pct_nd_real = (total_nd_real / total_linhas) * 100

#print(f"NÚMERO E PERCENTUAL DE VALORES '#N/D' REAIS:")
print(f"   - Total de registros na base atual: {total_linhas}")
print(f"   - Linhas com o termo exato '#N/D' encontradas: {total_nd_real}")
print(f"   - Percentual real de não conformidade: {pct_nd_real:.4f}%")
print("="*65)

linhas_restantes = total_linhas - total_nd_real
print(f"   - Linhas restantes: {total_linhas - total_nd_real}")
print("="*65)

print()
print("=== LOCALIZAÇÃO DE ERROS (#N/D) ===")
print(f"Quantidade de linhas afetadas por '#N/D': {len(linhas_com_erro):,}".replace(',', '.'))

# Mostra os 10 primeiros números de linhas (índices) onde o erro aparece
print("\nPrimeiras posições (índices) com erro na tabela:PR_CAT e PR_NOME")
print(linhas_com_erro.index[:10])
print("="*65)

print("\nMOMENTO: DECISÃO DE EXCLUSÃO OU AJUSTE?")
print("   -> PARECER: Como o erro afeta exatamente 3.650 linhas e atinge")
print("      concomitantemente o nome e a categoria, o registro perdeu")
print("      totalmente a identidade. Decisão: EXCLUSÃO TOTAL dessas linhas.")




# %%

import pandas as pd

print("="*65)
print(" TRATAMENTO DE LINHAS DUPLICADAS")
print("="*65)

# Carregar a base do Sprint 2
df = pd.read_csv('base_varejo_sprint2.csv', sep=',')

# Convertendo a data de string para datetime
df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y', errors='coerce')

#  Buscando não conformidades: Número e Percentual de duplicados
total_linhas = len(df)
linhas_duplicadas = df.duplicated().sum()
percentual_duplicadas = (linhas_duplicadas / total_linhas * 100)


print(f" RELATÓRIO DE DUPLICADOS:")
print(f"   - Total de registros iniciais(na base:) {total_linhas}")
print(f"   - Quantidade de linhas duplicadas: {linhas_duplicadas}")
print(f"   - Percentual de não conformidade: {percentual_duplicadas:.4f}%")
print("="*65)

# Aplicando a exclusão dos duplicados= drop.duplicates
df = df.drop_duplicates(keep='first')# para manter a primeira e apagar as proximnas
print(f"   -> [AÇÃO] Linhas restantes após exclusão: {len(df)}") # tamanho já reduzido
print("="*65)
#total de linhas apos retirada dos duplicados

# Quantidade de linhas e colunas - tipos de dados
print("Dimensões")
# Capturando a quantidade de linhas e colunas
total_linhas, total_colunas = df.shape
print(f"-> O arquivo possui um total de: {total_linhas} linhas (registros).")
#print(f"-> O arquivo possui um total de: {total_colunas} colunas (variáveis).")
print("="*65)

print("\n MOMENTO: DECISÃO DE EXCLUSÃO OU AJUSTE?")
print("   -> PARECER: Exclusão total. Neste contexto, manter linhas idênticas inflaria")
print("      artificialmente o volume de vendas e o faturamento.")
print("="*65)

# Exportando a base final do Sprint 3
nome_ficheiro_sprint3 = 'base_varejo_sprint3.csv'
df.to_csv(nome_ficheiro_sprint3, index=False)
print(f"-> Base de dados final do Sprint 3 exportada como '{nome_ficheiro_sprint3}' com sucesso!")
print("\n" + "="*65)

# %%

print("="*65)
print(" SPRINT 3 - CONVERSÃO DE TIPOS E VALORES NULOS")
print("="*65)

# 1. Carregar a base do Sprint 3
print("-> Carregando a base de dados...")
df = pd.read_csv('base_varejo_sprint3.csv', sep=',')

# Garantir a remoção de colunas "Unnamed" se ainda persistirem no arquivo
colunas_fantasmas = [col for col in df.columns if 'Unnamed' in col]
if colunas_fantasmas:
    df = df.drop(columns=colunas_fantasmas)
    print(f"-> Colunas fantasmas limpas: {colunas_fantasmas}")

# 2. Conversão da coluna DATA de string para datetime
print("-> Convertendo a coluna 'DATA' para o tipo datetime...")
df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y', errors='coerce')

# 3. Verificação de valores nulos/vazios nas colunas reais
print("\n--- Verificação de Valores Nulos por Coluna ---")
valores_nulos = df.isnull().sum()
for col, total_nulos in valores_nulos.items():
    print(f"   - Coluna '{col}': {total_nulos} valores nulos encontrados.")

print("\n[OK] Passo 1 concluído com sucesso!")
print(f"Tipo atual da coluna DATA: {df['DATA'].dtype}")

# %%
# 03. Quantidade de linhas e colunas - tipos de dados
print("="*65)
print("Dimensões")
# Capturando a quantidade de linhas e colunas
total_linhas, total_colunas = df.shape
print(f"-> O arquivo possui um total de: {total_linhas} linhas (registros).")
print(f"-> O arquivo possui um total de: {total_colunas} colunas (variáveis).")
print("="*65)



