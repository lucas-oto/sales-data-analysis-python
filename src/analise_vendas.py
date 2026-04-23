
# Análise de Vendas com python, pandas e matplotlib

# In[267]:


# Import das bibliotecas e DataFrame
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./data/vendas.csv', encoding = 'utf -8') # Banco de dados de vendas entre 2024-2025


# In[268]:


# Explorando df
df.info()
df.head(10)


# In[269]:


# Verificando e limpando duplicadas
df.duplicated().sum()
df = df.drop_duplicates()

# Converte coluna data para tipo data
df['data'] = pd.to_datetime(df['data'], errors = 'coerce')

# Organizando nulos
df.isna().sum() # Conferindo
df['desconto'] = df['desconto'].fillna(0) # Definindo valores nulos da coluna desconto com ZERO
df['canal_venda'] = df['canal_venda'].fillna('desconhecido') # Definindo valores nulos da coluna canal_venda para desconhecido
df['regiao'] = df['regiao'].fillna('nao informado') # Definindo valores nulos da regiao para desconhecido

# Confere se há mais nulos
df.isna().sum()
df = df.dropna(subset=['produto', 'cliente', 'data']) # Remove linhas produto, cliente ou data que mostram nulos

# Definindo palavras em forma minúscula e removendo espaços inúteis de colunas
colunas_texto = ['cliente', 'produto', 'categoria', 'regiao', 'canal_venda']
for i in colunas_texto:
    df[i] = df[i].str.lower().str.strip()

# Mantém apenas o que é positivo e maior que zero
df = df[df['quantidade'] > 0]
df = df[df['preco_unitario'] > 0]

# Remove linhas com desconto menor que 0% ou maior que 100%
df = df[(df['desconto'] >= 0) & (df['desconto'] <= 1)]

# Analisando se há categorias com e sem acentos
df['categoria'].value_counts() # Há acentos em eletrônicos e móveis
# Remove acentos de 'categoria'
df['categoria'] = df['categoria'].replace({
    'eletrônicos': 'eletronicos',
    'móveis': 'moveis',
})
# Remove acentos de 'produtos'
df['produto'] = df['produto'].replace({
    'teclado mecânico': 'teclado mecanico',
    'caneca térmica': 'caneca termica',
    'curso sql básico': 'curso sql basico',
    'garrafa térmica': 'garrafa termica'
})

df['categoria'].value_counts() # Sem acentos em categoria
df['produto'].value_counts() # Sem acentos em produtos

# Salvando o df limpo
df_limpo = df
df['produto'].value_counts()


# In[270]:


# Criando colunas necessárias para deixar a exibição do Dataframe mais entuitivo

df_limpo['faturamento_bruto'] = df_limpo['quantidade'] * df_limpo['preco_unitario']
df_limpo['valor_desconto'] = df_limpo['faturamento_bruto'] * df_limpo['desconto']
df_limpo['faturamento_liquido'] = df_limpo['faturamento_bruto'] - df_limpo['valor_desconto']
df_limpo['mes'] = df_limpo['data'].dt.month
df_limpo['ano'] = df_limpo['data'].dt.year

df_limpo.info()
df_limpo


# Questionário para análise dos dados do csv limpo e organizado

# In[271]:


# Faturamento Total

faturamento_total = round(df_limpo['faturamento_liquido'].sum(), 2) # Soma a coluna faturamento_liquido
print(faturamento_total) # Mostra a receita total


# In[272]:


# Faturamento por categoria

# Agrupa a coluna categoria e soma a coluna faturamento_liquido e organiza do maior para menor
faturamento_categoria = round(df_limpo.groupby('categoria')['faturamento_liquido'].sum(), 2).sort_values(ascending=False) 
print(faturamento_categoria) # Mostra a receita por categoria


# In[273]:


# Faturamento por região

# Agrupa a coluna regiao e soma a coluna faturamento_liquido, organiza do maior para menor
faturamento_regiao = round(df_limpo.groupby('regiao')['faturamento_liquido'].sum(), 2).sort_values(ascending= False) 
print(faturamento_regiao) # Mostra a receita por região


# In[274]:


# Top clientes

# Agrupa clientes e soma a faturamento_liquido, organiza do maior para o menor num top 10
top_clientes = round(df_limpo.groupby('cliente')['faturamento_liquido'].sum().sort_values(ascending= False).head(10), 2)
print(top_clientes)


# In[275]:


# Top produtos
top_produtos = df_limpo.groupby('produto')['quantidade'].sum().sort_values(ascending= False).head(10)
print(top_produtos)


# In[276]:


# Receita mensal 

df['ano_mes'] = df['data'].dt.to_period('M') # Crie uma coluna ano_mes para facilitar calculo
receita_mensal = round(df.groupby('ano_mes')['faturamento_liquido'].sum(), 2) # Agrupa a coluna ano_mes e soma com faturamento_liquido
print(receita_mensal)


# Comandos para gráficos utilizando a biblioteca matplotlib

# In[277]:


# Faturamento por categoria

plt.figure(figsize=(10,6))
faturamento_categoria.plot(kind='bar')
plt.title('Fatura por Categoria')
plt.xlabel('Categoria')
plt.ylabel('Faturamento Líquido')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./graficos/faturamento_categoria.png', dpi=300, bbox_inches='tight')
plt.show()


# In[278]:


# Evolução da receita ao longo do tempo

receita_mensal.index = receita_mensal.index.astype(str)

plt.figure(figsize=(12,6))
plt.plot(receita_mensal.index, receita_mensal.values, marker='o')
plt.title('Evolução Mensal do Faturamento')
plt.xlabel('Ano-Mês')
plt.ylabel('Faturamento Líquido')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./graficos/receita_mensal.png', dpi=300, bbox_inches='tight')
plt.show()


# In[279]:


# Top 10 produtos mais vendidos

plt.figure(figsize=(10,6))
top_produtos.plot(kind='barh')
plt.title('Top 10 Produtos por Faturamento')
plt.xlabel('Faturamento Líquido')
plt.ylabel('Produto')
plt.tight_layout()
plt.savefig('./graficos/top_produtos.png', dpi=300, bbox_inches='tight')
plt.show()


# In[280]:


# Faturamento por região

plt.figure(figsize=(10,6))
faturamento_regiao.plot(kind='bar')
plt.title('Faturamento por Região')
plt.xlabel('Região')
plt.ylabel('Faturamento Líquido')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./graficos/faturamento_regiao.png', dpi=300, bbox_inches='tight')
plt.show()


# ## Principais Insights
# 
# - A categoria de eletrônicos liderou o faturamento total.
# - A região Sudeste apresentou melhor desempenho.
# - O mês de Janeiro de 2024 registrou pico de vendas.
# - O mês de Junho de 2024 registrou o pior momento de vendas.
# - Alguns produtos possuem baixa representatividade e podem ser reavaliados.

# %%
