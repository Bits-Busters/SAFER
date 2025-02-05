# Usa a imagem oficial do Python
FROM python:3.12

# Define a raiz do container
WORKDIR /app

# Instala o Poetry globalmente
RUN pip install --no-cache-dir poetry

# Copia os arquivos do Poetry primeiro para otimizar o cache
COPY pyproject.toml poetry.lock ./

# Configura o Poetry para não usar virtualenvs 
RUN poetry config virtualenvs.create false 

# Instala as dependências (sem modificar o pyproject.toml)
RUN poetry install --no-interaction --no-ansi

# Copia todo o código do projeto para dentro do container
COPY . .

# Porta usada pelo container
EXPOSE 8000

# Faz migrações
RUN python3 Projeto/manage.py makemigrations
RUN python3 Projeto/manage.py migrate

# Comando padrão para rodar o Django
CMD ["python3", "Projeto/manage.py", "runserver", "0.0.0.0:8000"]
