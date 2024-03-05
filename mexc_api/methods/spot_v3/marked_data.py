import typing

from mexc_api.clients.mexc import MEXCClient
from mexc_api.enums import KlineInterval
from mexc_api.types.marked_data import (
    ApiDefaultSymbol,
    CheckServerTime,
    CompressedAggregateTradesList,
    CurrentAveragePrice,
    DayTickerPriceChangeStatistics,
    ExchangeInformation,
    OrderBook,
    RecentTradesList,
    SymbolOrderBookTicker,
    SymbolPriceTicker,
)
from mexc_api.utils.case import to_snake_case


class MarkedData:
    def __init__(self, client: MEXCClient) -> None:
        self.client = client

    async def __aexit__(self) -> None:
        return await self.client.close_session()

    async def test_connectivity(self) -> dict:
        request = await self.client.request(
            method="GET",
            endpoint="/api/v3/ping",
            params={},
        )
        return request.response

    async def check_server_time(self) -> CheckServerTime:
        request =  await self.client.request(
            method="GET",
            endpoint="/api/v3/time",
            params={},
        )
        return CheckServerTime(**to_snake_case(request.response))

    async def api_default_symbol(self, symbol: str = None) -> ApiDefaultSymbol:
        request = await self.client.request(
            method="GET",
            endpoint="/api/v3/defaultSymbols",
            params={"symbol": symbol,} if symbol is not None else None,
        )
        return ApiDefaultSymbol(**to_snake_case(request.response))

    async def exchange_information(self, symbols: str = None) -> ExchangeInformation:
        if symbols is not None:
            symbol = "symbols" if len(symbols.split(",")) > 1 else "symbol"
        request = await self.client.request(
            method="GET",
            endpoint="/api/v3/exchangeInfo",
            params={
                symbol: symbols if symbol is not None else None,
            } if symbols is not None else {},
        )
        return ExchangeInformation(**to_snake_case(request.response))

    async def order_book(self, symbol: str, limit: int = 100) -> OrderBook:
        limit = 100 if limit > 5000 else limit
        request = await self.client.request(
            method="GET",
            endpoint="/api/v3/depth",
            params={
                "symbol": symbol,
                "limit": limit,
            },
        )
        return OrderBook(**to_snake_case(request.response))

    async def recent_trades_list(
            self,
            symbol: str,
            limit: int = 100,
    ) -> list[RecentTradesList]:
        list = []
        limit = 100 if limit > 1000 else limit
        request = await self.client.request(
            method="GET",
            endpoint="/api/v3/trades",
            params={
                "symbol": symbol,
                "limit": limit,
            },
        )
        for item in request.response:
            list.append(RecentTradesList(**to_snake_case(item)))
        return list

    async def compressed_aggregate_trades_list(
            self,
            symbol: str,
            start_time: int = None,
            end_time: int = None,
            limit: int = 500,
    ) -> list[CompressedAggregateTradesList]:
        list = []
        limit = 500 if limit > 1000 else limit
        params_dict = {
            "symbol": symbol,
            "limit": limit,
        }
        if start_time is not None:
            params_dict["startTime"] = start_time
        if end_time is not None:
            params_dict["endTime"] = end_time
        request = await self.client.request(
            method="GET",
            endpoint="/api/v3/aggTrades",
            params=params_dict,
        )
        for item in request.response:
            list.append(CompressedAggregateTradesList(**item))
        return list

    async def kline_candlestick_data(
            self,
            symbol: str,
            interval: KlineInterval = KlineInterval.d1,
            start_time: float = None,
            end_time: float = None,
            limit: int = 500,
    ) -> list[list]:
        limit = 500 if limit > 1000 else limit
        params_dict = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
        }
        if start_time is not None:
            params_dict["startTime"] = start_time
        if end_time is not None:
            params_dict["endTime"] = end_time
        request = await self.client.request(
            method="GET",
            endpoint="/api/v3/klines",
            params=params_dict,
        )
        return request.response

    async def current_average_price(self, symbol: str) -> CurrentAveragePrice:
        request = await self.client.request(
            method="GET",
            endpoint="/api/v3/avgPrice",
            params={
                "symbol": symbol,
            },
        )
        return CurrentAveragePrice(**to_snake_case(request.response))

    async def day_ticker_price_change_statistics(
            self,
            symbol: str = None,
    ) -> DayTickerPriceChangeStatistics | list[DayTickerPriceChangeStatistics]:
        list = []
        symbol = symbol if symbol is not None else ""
        request = await self.client.request(
            method="GET",
            endpoint="/api/v3/ticker/24hr",
            params={
                "symbol": symbol,
            },
        )
        if symbol == "":
            for item in request.response:
                list.append(DayTickerPriceChangeStatistics(**to_snake_case(item)))
            return list
        return DayTickerPriceChangeStatistics(**to_snake_case(request.response))

    async def symbol_price_ticker(
            self,
            symbol: str = None,
    ) -> SymbolPriceTicker | list[SymbolPriceTicker]:
        list = []
        symbol = symbol if symbol is not None else ""
        request = await self.client.request(
            method="GET",
            endpoint="/api/v3/ticker/price",
            params={
                "symbol": symbol,
            },
        )
        if symbol == "":
            for item in request.response:
                list.append(SymbolPriceTicker(**to_snake_case(item)))
            return list
        return SymbolPriceTicker(**to_snake_case(request.response))

    async def symbol_order_book_ticker(
            self,
            symbol: str = None,
    ) -> SymbolOrderBookTicker | list[SymbolOrderBookTicker]:
        list = []
        symbol = symbol if symbol is not None else ""
        request = await self.client.request(
            method="GET",
            endpoint="/api/v3/ticker/bookTicker",
            params={
                "symbol": symbol,
            },
        )
        if symbol == "":
            for item in request.response:
                list.append(SymbolOrderBookTicker(**to_snake_case(item)))
            return list
        return SymbolOrderBookTicker(**to_snake_case(request.response))
