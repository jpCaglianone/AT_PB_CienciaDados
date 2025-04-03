# Usa uma imagem base do Python
FROM python:3.10

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia todos os arquivos Python para o container
COPY . .

# Comando para encontrar todos os arquivos .py e executá-los
CMD find . -name "*.py" | sort | xargs python

