import asyncio

from typing import Any

import orjson
from aiohttp import ClientSession

from mexc_api.clients.core.exceptions import ForbiddenMethod, ErrorStatusCode
from mexc_api.clients.core.rate_limits import RateLimits
from mexc_api.status_codes import BAD_STATUS_CODES
from mexc_api.types.http import ApiResponse
from mexc_api.utils.logging import Logging


class ApiClient:
    def __init__(
            self,
            base_url: str,
            custom_header: dict | None = None,
            allowed_methods: list[str] | None = None,
            rate_limits: int = None,
            enable_logging: bool = True,
            save_logs: bool = False,
            custom_error_status_codes: list[int] | None = None,
            custom_error_schema: Any | None = None,
            proxy: str | None = None,
    ) -> None:
        self.base_url = base_url
        self.custom_header = custom_header
        self.allowed_methods = allowed_methods
        self.rate_limits_amount = rate_limits
        self.rate_limits_cool_down = 1.00
        self.enable_logging = enable_logging
        self.save_logs = save_logs
        self.custom_error_status_codes = custom_error_status_codes
        self.custom_error_schema = custom_error_schema
        self.proxy = proxy
        self.header = {}
        self.error_codes = BAD_STATUS_CODES
        self.default_allowed_methods = [
            "GET",
            "HEAD",
            "POST",
            "PUT",
            "DELETE",
            "CONNECT",
            "OPTIONS",
            "TRACE",
            "PATCH",
        ]
        self.rate_limits = RateLimits(self.rate_limits_amount)
        self.logging = Logging(save_logs=self.save_logs)

        if self.custom_header is not None:
            self.header.update(custom_header)

        if self.allowed_methods is None:
            self.allowed_methods = self.default_allowed_methods

        if self.custom_error_status_codes is None:
            self.error_codes.append(self.custom_error_status_codes)

        self.session = ClientSession(
            base_url=self.base_url,
            headers=self.header,
            json_serialize=(lambda x: orjson.dumps(x).decode()),
        )

    async def __aenter__(self) -> "ApiClient":
        return self

    async def __aexit__(self) -> None:
        return await self.close_session()

    async def close_session(self) -> None:
        return await self.session.close()

    async def request(
            self,
            method: str,
            endpoint: str,
            params: dict = None,
            json: dict = None,
    ) -> ApiResponse:
        if method not in self.allowed_methods:
            error_text = f"Allowed only {', '.join(self.allowed_methods)} methods!"
            if self.enable_logging:
                self.logging.error(mes=error_text)
            raise ForbiddenMethod(error_text)

        if self.rate_limits_amount is not None:
            if self.rate_limits.is_limited:
                if self.enable_logging:
                    warning_text = (
                        f"Your request reached rate limits! "
                        f"sleeping for {self.rate_limits_cool_down} secs.."
                    )
                    self.logging.warning(mes=warning_text)
                await asyncio.sleep(self.rate_limits_cool_down)

        if self.enable_logging:
            self.logging.info(
                f"RPS: {self.rate_limits.amount}\t| {method}\t| {self.base_url}{endpoint}",
            )

        request = await self.session.request(
            method=method,
            url=endpoint,
            params=params,
            json=json,
            proxy=self.proxy,
        )

        status_code = request.status
        response = await request.json(
            encoding="utf-8",
            loads=orjson.loads,
            content_type="application/json",
        )

        if status_code in self.error_codes:
            error_text = f"Error status code ({status_code})!"

            if self.custom_error_schema is not None:
                error_text = self.custom_error_schema(**response)

            if self.enable_logging:
                self.logging.error(mes=error_text)

            await self.close_session()
            raise ErrorStatusCode(error_text)

        self.rate_limits.new if self.rate_limits_amount is not None else ...

        return ApiResponse(
            response=response,
            status_code=status_code,
        )
