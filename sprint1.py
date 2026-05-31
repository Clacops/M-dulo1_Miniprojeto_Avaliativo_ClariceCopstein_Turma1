# •	Sprint 1 (Importação dos dados): Realização da importação dos dados na plataforma Kaggle para a IDE VsCode ou Colab, onde  o script  será executado.
# 01.	Importando tabela 
# 02.	Definindo apresentação das tabelas e casas decimais
# 03.	Quantidade de linhas e colunas - número de registros, colunas e tipos de dados.
# 04.	Salvando o arquivo com o novo nome e o novo separador (vírgula)
# 05.	Conexao e primeiro commit Github


import pandas as pd

print("Sprint 1 (Importação dos dados)")
# 01. Importando a tabela
print("Importando a base de dados...")
df = pd.read_csv('Base Varejo.csv', sep=';') 


# 02. Definindo a apresentação das tabelas e casas decimais
print( "Configurando a apresentação do Pandas")
pd.set_option('display.max_columns', None)       
pd.set_option('display.max_rows', 20)            
pd.set_option('display.float_format', '{:.2f}'.format) 

# 03. Quantidade de linhas e colunas - tipos de dados
print("="*65)
print("Dimensões")

# Capturando a quantidade de linhas e colunas
total_linhas, total_colunas = df.shape
print(f"-> O arquivo possui um total de: {total_linhas} linhas (registros).")
print(f"-> O arquivo possui um total de: {total_colunas} colunas (variáveis).")
print("="*65)
print("\nTipos de Dados por Coluna:")
print(df.dtypes)


# 04. Salvando o arquivo com o novo nome e o novo separador
print("\nExportando a nova base...")
novo_nome = 'base_varejo_sprint1.csv'
print(f"\nExportando a nova base como '{novo_nome}'...")
df.to_csv(novo_nome, sep=',', index=False)

print("[OK] Sprint 1 concluído! Arquivo guardado com sucesso")
print("="*65)

# %%
# Melhorando a visualização no jupyter vscode
df.head()


