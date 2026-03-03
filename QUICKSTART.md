# 🚀 QUICK START - Breweries Dashboard

## ⚡ 5 Minutos para começar

### 1️⃣ Setup Automático (Recomendado)

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

---

### 2️⃣ Setup Manual

```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar AWS (se necessário)
aws configure
```

---

### 3️⃣ Iniciar Dashboard

```bash
streamlit run streamlit_app/main.py
```

**O dashboard abrirá em:** http://localhost:8501

---

## 📊 Usando o Dashboard

### 1. Fazer uma Query Simples

Na área principal, copie e execute:

```sql
SELECT *
FROM gold.tb_ft_breweries_agg
LIMIT 100
```

### 2. Usar Sample Query

No menu lateral, selecione uma query pronta no dropdown "Sample Queries"

### 3. Exportar Dados

Depois de executar uma query, clique em:
- 📥 Download CSV
- 📥 Download JSON
- 📥 Download Parquet

---

## 🛠️ Comandos Úteis

```bash
# Usar Makefile (se tiver make instalado)
make help           # Ver todos os comandos
make run            # Iniciar app
make test           # Rodar testes
make lint           # Verificar código
make format         # Formatar código

# Verificar AWS
aws sts get-caller-identity

# Limpar cache
streamlit run streamlit_app/main.py --logger.level=debug
```

---

## ❌ Problemas Comuns

### "AWS connection failed"
```bash
aws configure
```

### "Table not found"
- Verificar: `gold.tb_ft_breweries_agg`
- Testar acesso: `aws athena list-databases --region sa-east-1`

### "Port 8501 in use"
```bash
streamlit run streamlit_app/main.py --server.port 8502
```

### "Module not found"
```bash
# Ativar venv e reinstalar
source venv/bin/activate  # ou venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📚 Documentação Completa

- **[README Principal](./README.md)** - Overview do projeto
- **[Documentação Streamlit](./STREAMLIT_README.md)** - Guia completo
- **[Setup Guide (PT)](./SETUP_GUIDE_PT.md)** - Instruções detalhadas em português

---

## 🎯 Próximas Ações

✅ Setup completo
✅ Dashboard rodando
✅ Conectado ao Athena

**Agora você pode:**
1. Explorar os dados da tabela gold.tb_ft_breweries_agg
2. Criar suas próprias queries SQL
3. Exportar dados em múltiplos formatos
4. Analisar estatísticas dos dados

---

## 💡 Dicas

- **Slow queries?** Use LIMIT para reduzir resultados
- **Need help?** Veja STREAMLIT_README.md
- **Want samples?** Check "Sample Queries" na sidebar
- **Export data?** Download buttons aparecem após query

---

**Enjoy! 🍺📊**

Para mais informações, veja a documentação completa.
