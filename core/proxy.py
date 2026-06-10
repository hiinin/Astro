import json
import time

import httpx
from fastapi import HTTPException

_client: httpx.AsyncClient | None = None
_cache: dict[str, tuple[float, dict | list]] = {}

CACHE_TTL_SECONDS = 300
CACHE_MAX_ENTRIES = 200


async def init_client() -> None:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, connect=10.0),
            limits=httpx.Limits(max_connections=50, max_keepalive_connections=20),
            headers={"Accept": "application/json", "User-Agent": "Lunar-Engine/1.0"},
            follow_redirects=True,
        )


async def close_client() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None
    _cache.clear()


def _cache_key(url: str, params: dict | None) -> str:
    if not params:
        return url
    query = "&".join(f"{key}={params[key]}" for key in sorted(params))
    return f"{url}?{query}"


def _get_cached(key: str) -> dict | list | None:
    entry = _cache.get(key)
    if entry is None:
        return None
    expires_at, data = entry
    if time.monotonic() >= expires_at:
        del _cache[key]
        return None
    return data


def _set_cached(key: str, data: dict | list, ttl: int) -> None:
    if ttl <= 0:
        return
    if len(_cache) >= CACHE_MAX_ENTRIES:
        del _cache[next(iter(_cache))]
    _cache[key] = (time.monotonic() + ttl, data)


async def proxy(url: str, params: dict | None = None, *, ttl: int = CACHE_TTL_SECONDS) -> dict | list:
    """Realiza uma requisição GET ao serviço externo e repassa a resposta JSON."""
    key = _cache_key(url, params)
    cached = _get_cached(key)
    if cached is not None:
        return cached

    if _client is None:
        await init_client()

    try:
        response = await _client.get(url, params=params or {})
        response.raise_for_status()
        data = response.json()
        _set_cached(key, data, ttl)
        return data

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="O serviço externo não respondeu dentro do tempo esperado.",
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="Resposta inválida do serviço externo.",
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Erro retornado pela API externa: {exc.response.text}",
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Não foi possível conectar ao serviço externo: {exc}",
        )
