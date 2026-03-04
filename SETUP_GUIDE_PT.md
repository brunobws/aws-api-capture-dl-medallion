"""
Setup and deployment instructions for Breweries Dashboard.

Este documento fornece instruções passo a passo para configurar e executar
a aplicação Streamlit localmente.

Author: Data Team
Version: 1.0.0
"""

# GUIA DE CONFIGURAÇÃO - BREWERIES DASHBOARD


## ⚙️ CONFIGURAÇÃO INICIAL

### 1. Instalar Dependências

```bash
# Navegar até o diretório do projeto
cd bws-breweries-pipeline

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Ativar ambiente virtual (macOS/Linux)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```


### 2. Configurar AWS Credentials

**Opção 1: AWS CLI (Recomendado)**
```bash
aws configure
# Preencha com seus dados:
# AWS Access Key ID
# AWS Secret Access Key
# Default region (sa-east-1)
# Default output format (json)
```

**Opção 2: Variáveis de Ambiente**
```bash
# Windows (PowerShell)
$env:AWS_ACCESS_KEY_ID="seu_access_key"
$env:AWS_SECRET_ACCESS_KEY="seu_secret_key"
$env:AWS_DEFAULT_REGION="sa-east-1"

# macOS/Linux
export AWS_ACCESS_KEY_ID="seu_access_key"
export AWS_SECRET_ACCESS_KEY="seu_secret_key"
export AWS_DEFAULT_REGION="sa-east-1"
```

**Opção 3: Arquivo .aws/credentials**
```
[default]
aws_access_key_id = seu_access_key
aws_secret_access_key = seu_secret_key
```

**Verificar Configuração:**
```bash
aws sts get-caller-identity
# Deve retornar suas informações de conta AWS
```


### 3. Verificar Acesso ao Athena

```bash
# Listar databases no Athena
aws athena list-databases --region sa-east-1

# Deve incluir o database 'gold'
```


## 🚀 EXECUTAR A APLICAÇÃO

### Iniciar o Streamlit

```bash
# Windows
streamlit run streamlit_app/main.py

# macOS/Linux
streamlit run streamlit_app/main.py
```

A aplicação abrirá automaticamente no navegador:
```
Local URL: http://localhost:8501
```


## 📋 ESTRUTURA DE ARQUIVOS CRIADOS

```
streamlit_app/
├── main.py                              # Aplicação principal
├── config.py                            # Configurações
├── utils/
│   ├── __init__.py
│   ├── athena_connector.py             # Conexão com Athena
│   └── data_processing.py              # Processamento de dados
├── .streamlit/
│   └── config.toml                     # Config do Streamlit
└── assets/                             # Pasta para imagens/logos
```


## 🔧 CUSTOMIZAÇÃO

### 1. Alterar Configurações da Aplicação

Editar `streamlit_app/config.py`:

```python
# Banco de dados (se mudou o nome)
ATHENA_DATABASE = "gold"

# Tabela principal
ATHENA_TABLE = "tb_ft_breweries_agg"

# Output do Athena (S3)
ATHENA_S3_OUTPUT = "s3://bws-dl-logs-sae1-prd/athena/query_results/"

# Número padrão de linhas
DEFAULT_ROWS_TO_DISPLAY = 1000

# Tema
STREAMLIT_THEME = "light"
```

### 2. Adicionar Queries de Amostra

Em `streamlit_app/config.py`, na seção `SAMPLE_QUERIES`:

```python
SAMPLE_QUERIES = {
    "Minha Query Customizada": """
    SELECT *
    FROM gold.tb_ft_breweries_agg
    WHERE state = 'CA'
    LIMIT 100
    """
}
```

### 3. Personalizar Nomes de Colunas

Em `streamlit_app/config.py`:

```python
COLUMN_DISPLAY_NAMES = {
    "brewery_id": "ID da Cervejaria",
    "brewery_name": "Nome da Cervejaria",
    # Continue conforme necessário
}
```


## 📊 USANDO A APLICAÇÃO

### Consultar Dados

1. **Query Editor**: Digite sua consulta SQL
2. **Sample Queries**: Selecione uma query pronta
3. **Run Query**: Execute a query
4. **Ver Resultados**: Análise dos dados retornados


### Exportar Dados

Depois de executar uma query:
- 📥 Download CSV
- 📥 Download JSON
- 📥 Download Parquet


### Análise de Dados

A aplicação fornece:
- Total de linhas e colunas
- Uso de memória
- Tipos de dados
- Valores ausentes
- Distribuição de valores únicos


## ⚠️ SOLUÇÃO DE PROBLEMAS

### Erro: "Connection Error: An error occurred"

**Causa**: Credenciais AWS não configuradas
**Solução**:
```bash
aws configure
# ou
aws sts get-caller-identity
```


### Erro: "Table not found"

**Verificar**:
1. Nome da tabela: `gold.tb_ft_breweries_agg`
2. Database: `gold`
3. Região AWS: `sa-east-1`


### Erro: "Permission denied"

**Solução**: Verificar permissões IAM:
- `athena:StartQueryExecution`
- `athena:GetQueryExecution`
- `athena:GetQueryResults`
- `s3:GetObject` (para S3 de resultado)


### Aplicação lenta

**Otimizações**:
1. Usar LIMIT nas queries
2. Adicionar WHERE clauses
3. Selecionar apenas colunas necessárias
4. Evitar JOIN complexos


## 🔐 SEGURANÇA

- ✅ Nunca commitar credenciais no Git
- ✅ Usar IAM roles em produção
- ✅ Implementar autenticação Streamlit (produção)
- ✅ Usar HTTPS em produção


## 📚 DOCUMENTAÇÃO

- `STREAMLIT_README.md` - Documentação completa
- `streamlit_app/config.py` - Configurações comentadas
- `streamlit_app/main.py` - Código da aplicação com docstrings


## 🆘 SUPORTE

Para problemas ou dúvidas:
1. Verificar logs do Streamlit
2. Consultar documentação do Athena
3. Verificar credenciais AWS

---

**Data Team**
**Versão: 1.0.0**
**Data de Atualização: 2026-03-02**
