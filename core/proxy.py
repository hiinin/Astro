import httpx
from fastapi import HTTPException


async def proxy(url: str, params: dict | None = None) -> dict:
    """Realiza uma requisição GET ao serviço externo e repassa a resposta JSON."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params or {})
            response.raise_for_status()
            return response.json()

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="O serviço externo não respondeu dentro do tempo esperado.",
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
