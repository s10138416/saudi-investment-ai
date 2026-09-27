from __future__ import annotations

from typing import Any

import httpx

from app.core.config import get_settings


class SahmkError(RuntimeError):
    """Normalized SAHMK API error used by the FastAPI layer."""

    def __init__(self, message: str, *, status_code: int | None = None, code: str | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code


class SahmkClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def configured(self) -> bool:
        return bool(self.settings.sahmk_api_key.strip())

    @staticmethod
    def _error_details(response: httpx.Response) -> tuple[str | None, str | None]:
        try:
            payload = response.json()
        except ValueError:
            return None, None

        if not isinstance(payload, dict):
            return None, None

        error = payload.get("error")
        if isinstance(error, dict):
            return error.get("message"), error.get("code")

        detail = payload.get("detail")
        if isinstance(detail, dict):
            return detail.get("message"), detail.get("code")
        if isinstance(detail, str):
            return detail, None

        message = payload.get("message")
        return (message if isinstance(message, str) else None), None

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        if not self.configured:
            raise SahmkError("SAHMK_API_KEY is not configured", code="NO_KEY")

        url = f"{self.settings.sahmk_base_url.rstrip('/')}/{path.lstrip('/')}"
        headers = {
            "X-API-Key": self.settings.sahmk_api_key,
            "Accept": "application/json",
        }
        timeout = httpx.Timeout(self.settings.sahmk_timeout_seconds)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url, headers=headers, params=params)
        except httpx.TimeoutException as exc:
            raise SahmkError("SAHMK request timed out", code="TIMEOUT") from exc
        except httpx.HTTPError as exc:
            raise SahmkError(f"SAHMK network error: {exc}", code="NETWORK_ERROR") from exc

        if response.is_success:
            try:
                return response.json()
            except ValueError as exc:
                raise SahmkError(
                    "SAHMK returned a non-JSON response",
                    status_code=response.status_code,
                    code="INVALID_RESPONSE",
                ) from exc

        api_message, api_code = self._error_details(response)
        fallback = {
            400: "SAHMK rejected the request parameters",
            401: "SAHMK authentication failed",
            403: "SAHMK plan/permission does not allow this endpoint",
            404: "SAHMK resource was not found",
            429: "SAHMK rate limit reached",
        }.get(response.status_code, f"SAHMK API error {response.status_code}")

        raise SahmkError(
            api_message or fallback,
            status_code=response.status_code,
            code=api_code,
        )

    async def get_company(self, symbol: str) -> Any:
        return await self._get(f"company/{symbol}/")

    async def get_quote(self, symbol: str, data_mode: str | None = None) -> Any:
        params = {"data_mode": data_mode} if data_mode else None
        return await self._get(f"quote/{symbol}/", params=params)

    async def get_historical(
        self,
        symbol: str,
        *,
        interval: str = "1d",
        date_from: str | None = None,
        date_to: str | None = None,
        limit: int = 500,
        offset: int = 0,
    ) -> Any:
        # SAHMK uses from/to/interval/limit/offset. It does not use period=1y.
        params: dict[str, Any] = {
            "interval": interval,
            "limit": max(1, min(limit, 2000)),
            "offset": max(0, offset),
        }
        if date_from:
            params["from"] = date_from
        if date_to:
            params["to"] = date_to
        return await self._get(f"historical/{symbol}/", params=params)

    async def get_financials(
        self,
        symbol: str,
        *,
        statement_type: str = "all",
        period: str = "quarterly",
        history: str = "5y",
        metrics: str = "extended",
        result: str = "series",
        limit: int = 20,
        include_partial: bool = True,
    ) -> Any:
        params: dict[str, Any] = {
            "type": statement_type,
            "period": period,
            "history": history,
            "metrics": metrics,
            "result": result,
            "limit": max(1, min(limit, 20)),
        }
        if include_partial:
            params["include_partial"] = 1
        return await self._get(f"financials/{symbol}/", params=params)

    async def get_ratios(
        self,
        symbol: str,
        *,
        history: str = "5y",
        period: str = "quarterly",
        metrics: str = "extended",
        meta: str = "extended",
    ) -> Any:
        return await self._get(
            f"analytics/ratios/{symbol}/",
            params={
                "history": history,
                "period": period,
                "metrics": metrics,
                "meta": meta,
            },
        )

    async def get_trades(self, symbol: str, *, limit: int = 50) -> Any:
        return await self._get(
            f"market/trades/{symbol}/",
            params={"limit": max(1, min(limit, 200))},
        )


sahmk_client = SahmkClient()
