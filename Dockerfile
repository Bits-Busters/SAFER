# Usa a imagem oficial do Python
FROM python:3.12-slim AS builder

# Define a raiz do container
WORKDIR /app

# Instala dependências do sistema e remove cache de instalação
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry globalmente
RUN pip install --no-cache-dir poetry

# Copia os arquivos do Poetry primeiro para otimizar o cache
COPY pyproject.toml poetry.lock ./

# Baixa dependências e comprime elas em wheels
RUN poetry export -f requirements.txt --output requirements.txt \
    && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# -------------------------------------------------------------------------

FROM python:3.12-slim AS prod  

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt /wheels/requirements.txt
# Configura o Poetry para não usar virtualenvs 
RUN poetry config virtualenvs.create false 

# Instala as dependências (sem modificar o pyproject.toml)
RUN poetry install --no-interaction --no-ansi

# Copia todo o código do projeto para dentro do container
COPY . .

# Porta usada pelo container
EXPOSE 8000

# Comando padrão para rodar o Django
# CMD ["python3", "Projeto/manage.py", "runserver", "0.0.0.0:8000"]

# Comando de inicialização do Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "SAFERapp.wsgi:application"]