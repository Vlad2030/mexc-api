from mexc_api.clients.core.http_async import ApiClient
from mexc_api.status_codes import MEXC_ERROR_CODES
from mexc_api.types.mexc import MexcApiError
from mexc_api.utils.signature import signature
from mexc_api.utils.time import timestamp
from mexc_api.utils.urls import urlencode


class MEXCClient(ApiClient):
    def __init__(
            self,
            mexc_key: str | None = None,
            mexc_secret: str | None = None,
            logging: bool = False,
            save_logs: bool = False,
            proxy: str = None,
    ) -> None:
        self.base_url = "https://api.mexc.com"
        self.mexc_allowed_methods = [
            "GET",
            "POST",
            "DELETE",
        ]
        self.mexc_api_rate_limits = 20
        self.mexc_header = None
        self.mexc_error_codes = MEXC_ERROR_CODES
        self.mexc_error_schema = MexcApiError
        self.mexc_key = mexc_key
        self.mexc_secret = mexc_secret
        self.logging = logging
        self.save_logs = save_logs
        self.proxy = proxy

        self.signature = signature
        self.timestamp = timestamp
        self.urlencode = urlencode

        if self.mexc_key is not None:
            self.mexc_header = {"X-MEXC-APIKEY": self.mexc_key}

        super().__init__(
            base_url=self.base_url,
            custom_header=self.mexc_header,
            allowed_methods=self.mexc_allowed_methods,
            rate_limits=self.mexc_api_rate_limits,
            enable_logging=self.logging,
            save_logs=self.save_logs,
            custom_error_status_codes=self.mexc_error_codes,
            custom_error_schema=self.mexc_error_schema,
            proxy=self.proxy,
        )
