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


RUN poetry self add poetry-plugin-export


# Copia os arquivos do Poetry primeiro para otimizar o cache
COPY pyproject.toml poetry.lock ./

# Baixa dependências e comprime elas em wheels
RUN poetry export -f requirements.txt --without-hashes --output requirements.txt \
    && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# -------------------------------------------------------------------------

FROM python:3.12-slim AS prod  

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala depedências pré-compiladas
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt /wheels/requirements.txt
RUN pip install --no-index --find-links=/wheels -r /wheels/requirements.txt


# Copia todo o código do projeto para dentro do container
COPY ./Projeto ./Projeto

# Porta usada pelo container
EXPOSE 8000
RUN python Projeto/manage.py collectstatic --noinput


# Comando de inicialização do Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Projeto.wsgi:application"]