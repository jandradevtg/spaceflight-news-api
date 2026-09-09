"""
Spaceflight News Proxy API
==========================

API simples (FastAPI) que consome a API pública Spaceflight News (SNAPI v4)
e devolve as últimas notícias sobre voos espaciais.

Documentação da API pública: https://spaceflightnewsapi.net/
"""

import os

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

# Base da API pública. Pode ser sobrescrita via variável de ambiente.
SNAPI_BASE_URL = os.getenv(
    "SNAPI_BASE_URL", "https://api.spaceflightnewsapi.net/v4"
)
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "10"))

app = FastAPI(
    title="Spaceflight News Proxy API",
    description="Projeto de teste que consome a Spaceflight News API (SNAPI).",
    version="1.0.0",
)

# Habilita CORS para que o Swagger UI (e chamadas feitas pelo navegador)
# consigam consumir a API. Em ambiente de teste liberamos todas as origens.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Informações básicas do serviço."""
    return {
        "service": "spaceflight-news-proxy",
        "status": "ok",
        "endpoints": ["/health", "/articles", "/docs"],
    }


@app.get("/health")
def health():
    """Health check usado pelos probes do Kubernetes."""
    return {"status": "healthy"}


@app.get("/articles")
def articles(
    limit: int = Query(5, ge=1, le=50, description="Quantidade de notícias"),
    search: str | None = Query(None, description="Filtro opcional por texto"),
):
    """
    Busca as últimas notícias na Spaceflight News API e retorna uma versão
    enxuta (título, resumo, fonte, data e link).
    """
    params: dict[str, object] = {"limit": limit, "ordering": "-published_at"}
    if search:
        params["search"] = search

    try:
        response = httpx.get(
            f"{SNAPI_BASE_URL}/articles/",
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Falha ao consultar a Spaceflight News API: {exc}",
        ) from exc

    data = response.json()
    results = [
        {
            "id": item.get("id"),
            "title": item.get("title"),
            "summary": item.get("summary"),
            "news_site": item.get("news_site"),
            "published_at": item.get("published_at"),
            "url": item.get("url"),
        }
        for item in data.get("results", [])
    ]

    return {"count": len(results), "articles": results}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
    )
