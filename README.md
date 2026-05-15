# Instalar as bibliotecas

No terminal:
```bash
pip install -r requirements.txt
```

# Inicializar o alembic
No terminal:
```bash
python -m alembic init migrations
```

# Editar o arquivo alembic init -  na linha 89:
sqlalchemy.url = 

# Gerar a migration
no terminal:
```bash
python -m alembic revision --autogenerate -m "Criar a tabela usuarios"
```

# Aplicar a migration no banco
```bash
python -m alembic upgrade head
```



