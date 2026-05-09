from __future__ import annotations

import os
from typing import Any

import httpx

BASE_URL = "https://dev.to/api"
API_KEY_ENV = "DEVTO_API_KEY"


class DevToError(Exception):
    """Raised when the dev.to API returns a non-2xx response."""


class DevToClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = BASE_URL,
        timeout: float = 10.0,
    ) -> None:
        self.api_key = api_key or os.environ.get(API_KEY_ENV)
        self._http = httpx.Client(base_url=base_url, timeout=timeout)

    def __enter__(self) -> "DevToClient":
        return self

    def __exit__(self, *_exc: object) -> None:
        self._http.close()

    def _headers(self, *, require_auth: bool) -> dict[str, str]:
        headers = {"Accept": "application/vnd.forem.api-v1+json"}
        if self.api_key:
            headers["api-key"] = self.api_key
        elif require_auth:
            raise DevToError(
                f"This endpoint requires an API key. Set ${API_KEY_ENV} or pass --api-key."
            )
        return headers

    def _get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        require_auth: bool = False,
    ) -> Any:
        response = self._http.get(path, params=params, headers=self._headers(require_auth=require_auth))
        if response.status_code >= 400:
            raise DevToError(f"GET {path} failed: {response.status_code} {response.text}")
        return response.json()

    # --- Articles ---

    def list_articles(
        self,
        *,
        username: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {}
        if username:
            params["username"] = username
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        return self._get("/articles", params=params)

    def get_article(self, article_id: int) -> dict[str, Any]:
        return self._get(f"/articles/{article_id}")

    def get_article_by_slug(self, username: str, slug: str) -> dict[str, Any]:
        return self._get(f"/articles/{username}/{slug}")

    def list_my_articles(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        return self._get("/articles/me", params=params, require_auth=True)

    # --- Users ---

    def get_user(self, user_id: int) -> dict[str, Any]:
        return self._get(f"/users/{user_id}")

    def get_user_by_username(self, username: str) -> dict[str, Any]:
        return self._get("/users/by_username", params={"url": username})
