# Spaceflight News Proxy API

## Visão geral

API em FastAPI que consome a [Spaceflight News API (SNAPI)](https://spaceflightnewsapi.net/)
e devolve as últimas notícias sobre voos espaciais em um formato enxuto.

## Como executar

- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json
- Health check: http://localhost:8000/health

## Endpoints

### `GET /health`

Verifica se o serviço está no ar (usado pelos probes do Kubernetes).

```bash
curl http://localhost:8000/health
```

### `GET /articles`

Lista as últimas notícias. Aceita os parâmetros `limit` (1 a 50) e `search` (texto opcional).

```bash
# últimas 3 notícias
curl "http://localhost:8000/articles?limit=3"

# filtrando por texto
curl "http://localhost:8000/articles?limit=5&search=NASA"
```
