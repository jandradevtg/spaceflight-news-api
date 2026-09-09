# Imagem base enxuta com Python
FROM python:3.12-slim

# Boas práticas: não gerar .pyc e log sem buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala as dependências primeiro (melhor uso de cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o único arquivo Python do projeto
COPY app.py .

# Roda como usuário não-root
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# Inicia a API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
