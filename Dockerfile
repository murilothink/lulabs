# Usa a imagem base oficial do Python
FROM python:3.10

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY ./src /app
COPY requirements.txt /app

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Define a porta que o contêiner irá expor
EXPOSE 5000

# Comando para rodar o servidor Flask
CMD ["python", "app.py"]
