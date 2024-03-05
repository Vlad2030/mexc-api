import asyncio

import orjson
from aiohttp import ClientSession

from mexc_api.clients.core.exceptions import ForbiddenMethod
from mexc_api.types.http import ApiResponse
from mexc_api.utils.logging import Logging
from mexc_api.utils.rate_limits import RateLimits


class ApiClient:
    def __init__(
            self,
            base_url: str,
            custom_header: dict | None = None,
            allowed_methods: list[str] | None = None,
            rate_limits: int | None = None,
            enable_logging: bool = True,
            save_logs: bool = False,
    ) -> None:
        self.base_url = base_url
        self.custom_header = custom_header
        self.allowed_methods = allowed_methods
        self.rate_limits_amount = rate_limits if rate_limits is not None else 10000
        self.rate_limits_cool_down = 1.00
        self.enable_logging = enable_logging
        self.save_logs = save_logs
        self.header = {}
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
        self.rate_limits = RateLimits(max_rps=self.rate_limits_amount)
        self.logging = Logging(save_logs=self.save_logs)

        if self.custom_header is not None:
            self.header.update(custom_header)

        if self.allowed_methods is None:
            self.allowed_methods = self.default_allowed_methods

        self.session = ClientSession(
            base_url=self.base_url,
            headers=self.header,
            json_serialize=(lambda x: orjson.dumps(x).decode()),
        )

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
                    self.logging.warning(
                        mes=f"Your request reached rate limits! sleeping for {self.rate_limits_cool_down} secs..",
                    )
                await asyncio.sleep(self.rate_limits_cool_down)

        if self.enable_logging:
            self.logging.info(
                f"RPS: {self.rate_limits.amount}\t| {method}\t| {self.base_url}{endpoint}",
            )

        async with self.session.request(
            method=method,
            url=endpoint,
            params=params,
            json=json,
        ) as request:
            status_code = request.status
            response = await request.json(
                encoding="utf-8",
                loads=orjson.loads,
                content_type="application/json",
            )

        if self.rate_limits_amount is not None:
            self.rate_limits.new

            return ApiResponse(
                response=response,
                status_code=status_code,
            )
