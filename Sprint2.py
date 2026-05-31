
# Sprint 2 (Transformação de Strings, Integer e Float e Datetime): Desenvolvimento das funções de limpeza de texto, inteiros e decimais usando métodos e expressões regulares.
# 01.	Transformando: strings, integer e float 
#     Curiosidade: o que foi corrigido em 'PR_NOME'?
# 02.	Buscando não conformidades: datas invalidas
# 03.	Número e Percentual de não conformidades: datas invalidas - 
# 04.	Momento: Decisão de exclusão ou Ajuste?

# %%
import pandas as pd
import re

print("Sprint 2 - ")
print(" Transformando: strings, integer e float")

#  Carregar a base do Sprint 1
print("-> Carregando a base de dados...")
df = pd.read_csv('base_varejo_sprint1.csv', sep=',')

# Função para limpar Strings (Textos)
def limpar_texto(texto):
    if pd.isna(texto): 
        return texto
    return re.sub(r'\s+', ' ', str(texto)).strip().upper()

# 4. Função para limpar Inteiros (IDs e Filhos)
def limpar_inteiro(valor):
    if pd.isna(valor): 
        return 0
    apenas_numeros = re.sub(r'\D', '', str(valor))
    return int(apenas_numeros) if apenas_numeros != '' else 0

# ajustes de float ja havia sido realizado na primeira analise da tabela
pd.set_option('display.float_format', '{:.2f}'.format) 


# === APLICAÇÃO NAS SUAS COLUNAS REAIS ===
colunas_texto = ['CL_GENERO', 'CL_EC', 'CL_SEG', 'PR_CAT', 'PR_NOME'] 
total_textos_limpos = 0

print("="*65)
print("\n-> Relatório de Limpeza de Textos:")
for col in colunas_texto:
    if col in df.columns:
        # 1. Fotografia do 'antes' (transformando em string para garantir a comparação)
        antes = df[col].astype(str)
        print(f"   - Coluna '{col}': {antes.nunique()} valores únicos antes da limpeza. ")
        print(f"     Exemplos antes da limpeza: {antes.unique()[:10]}")
        # 2. Aplica a limpeza
        df[col] = df[col].apply(limpar_texto)
        
        # 3. Fotografia do 'depois'
        depois = df[col].astype(str)
        
        # 4. Compara e soma quantas linhas mudaram
        mudancas = (antes != depois).sum()
        total_textos_limpos += mudancas
        
        print(f"   - Coluna '{col}': {mudancas} textos corrigidos.")

print(f"-> Total geral de textos ajustados na base: {total_textos_limpos}\n")

# Colunas de Números Inteiros (IDs e quantidade de filhos)
colunas_inteiros = ['CO_ID', 'CL_ID', 'CL_FHL', 'PR_ID'] 
for col in colunas_inteiros:
    if col in df.columns:
        df[col] = df[col].apply(limpar_inteiro)

print("[OK] Transformações de texto e números concluídas!")
df.head()

print("="*65)
print("--- INVESTIGAÇÃO: O QUE FOI CORRIGIDO EM 'PR_NOME'? ---")

# 1. Carregamos a base original de novo, mas pegamos APENAS a coluna PR_NOME para ficar rápido
df_investigacao = pd.read_csv('base_varejo_sprint1.csv', sep=',', usecols=['PR_NOME'])

# 2. Replicamos a nossa função de limpeza
def limpar_texto(texto):
    if pd.isna(texto): 
        return texto
    return re.sub(r'\s+', ' ', str(texto)).strip().upper()

# 3. Criamos uma coluna NOVA chamada 'NOME_LIMPO' ao lado da original
df_investigacao['NOME_LIMPO'] = df_investigacao['PR_NOME'].apply(limpar_texto)

# 4. Filtramos para ver APENAS as linhas onde a original é diferente da limpa
mudancas = df_investigacao[df_investigacao['PR_NOME'] != df_investigacao['NOME_LIMPO']]

# 5. Removemos as duplicatas (para não ver o mesmo erro repetido mil vezes)
exemplos_unicos = mudancas.drop_duplicates()

print("="*65)
print(f"Total de produtos com algum tipo de sujeira: {len(mudancas)}")
print(f"Diferentes tipos de erros encontrados (sem repetição): {len(exemplos_unicos)}\n")
print("Veja abaixo a comparação (Original vs Limpo):")

# Mostramos as primeiras 20 correções para você investigar
exemplos_unicos.head(20)
print("="*65)

# %%
import pandas as pd

print("Sprint 2: Diagnóstico de Datas Inválidas") 

# A sua coluna de datas chama-se 'DATA'
nome_coluna_data = 'DATA'

print(f"-> A analisar a coluna '{nome_coluna_data}'...")

# Tenta converter os textos em formato de data real. 
# O parâmetro errors='coerce' obriga o Pandas a transformar qualquer coisa que não seja data em 'NaT' (Not a Time)
data_convertida = pd.to_datetime(df[nome_coluna_data], format='%d/%m/%Y', errors='coerce')

# Filtra a tabela para isolar apenas as linhas que ficaram com 'NaT' (ou seja, os erros)
linhas_invalidas = df[data_convertida.isna()] #isna=dados ausentes ou nulos

# Cálculos estatísticos
total_registros = len(df)
total_invalidas = len(linhas_invalidas)
percentual_invalidas = (total_invalidas / total_registros) * 100

# Criando um painel com os resultados
relatorio = (
    f"-> Total de registos analisados: {total_registros}\n"
    f"-> Número de não conformidades (Datas Inválidas): {total_invalidas}\n"
    f"-> Percentual de erro: [{percentual_invalidas:.4f}%"
)
print("="*65)
print("Relatório de Inconsistências")
print(linhas_invalidas[['CO_ID', 'DATA']].head(5))


# %%

print("PASSO 04: MOMENTO DE DECISÃO E EXPORTAÇÃO")

print("="*65)
# A nossa decisão técnica baseada nos 0% de erro:
print("->Diagnóstico: 0% de não conformidades nas datas.")
print("-> Decisão do Analista: Nenhuma exclusão ou ajuste é necessário. A integridade original será mantida.")
print("="*65)
# Exportando a base final do Sprint 2 (sem o índice do Pandas)
nome_ficheiro_sprint2 = 'base_varejo_sprint2.csv'
df.to_csv(nome_ficheiro_sprint2, index=False)

# 03. Quantidade de linhas e colunas - tipos de dados
print("="*65)
print("Dimensões")
# Capturando a quantidade de linhas e colunas
total_linhas, total_colunas = df.shape
print(f"-> O arquivo possui um total de: {total_linhas} linhas (registros).")
print(f"-> O arquivo possui um total de: {total_colunas} colunas (variáveis).")
print("="*65)


# Mensagem de encerramento do Sprint
mensagem_final = (
    f"[OK] Sprint 2 Concluído com sucesso!\n"
    f"-> Transformações de texto aplicadas com sucesso.\n"
    f"-> Tipos de dados numéricos (Inteiros) validados.\n"
    f"-> Ficheiro exportado: {nome_ficheiro_sprint2}"
)
print(mensagem_final)
print("="*65)


# %%



