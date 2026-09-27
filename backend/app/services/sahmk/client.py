from typing import Any
import httpx
from app.core.config import get_settings


class SahmkError(RuntimeError):
    pass


class SahmkClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def configured(self) -> bool:
        return bool(self.settings.sahmk_api_key.strip())

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        if not self.configured:
            raise SahmkError("SAHMK_API_KEY is not configured")

        url = f"{self.settings.sahmk_base_url.rstrip('/')}/{path.lstrip('/')}"
        headers = {
            "X-API-Key": self.settings.sahmk_api_key,
            "Accept": "application/json",
        }
        timeout = httpx.Timeout(self.settings.sahmk_timeout_seconds)

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, headers=headers, params=params)

        if response.status_code == 401:
            raise SahmkError("SAHMK authentication failed")
        if response.status_code == 403:
            raise SahmkError("SAHMK plan/permission does not allow this endpoint")
        if response.status_code == 404:
            raise SahmkError("SAHMK resource was not found")
        if response.status_code == 429:
            raise SahmkError("SAHMK rate limit reached")

        response.raise_for_status()
        return response.json()

    async def get_company(self, symbol: str) -> Any:
        return await self._get(f"company/{symbol}/")

    async def get_quote(self, symbol: str) -> Any:
        return await self._get(f"quote/{symbol}/")

    async def get_historical(self, symbol: str, period: str = "1y") -> Any:
        return await self._get(f"historical/{symbol}/", params={"period": period})

    async def get_financials(self, symbol: str) -> Any:
        return await self._get(f"financials/{symbol}/")


sahmk_client = SahmkClient()
