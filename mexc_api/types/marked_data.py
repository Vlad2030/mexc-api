from mexc_api.types.base_schema import BaseSchema


class CheckServerTime(BaseSchema):
    server_time: int


class ApiDefaultSymbol(BaseSchema):
    code: int
    data: list[str]
    msg: str | None


class SymbolExchangeInformation(BaseSchema):
    symbol: str
    status: str
    base_asset: str
    base_asset_precision: int | str
    quote_asset: str
    quote_precision: int
    quote_asset_precision: int
    base_commission_precision: int
    quote_commission_precision: int
    order_types: list[str]
    is_spot_trading_allowed: bool
    is_margin_trading_allowed: bool
    quote_amount_precision: float | int
    base_size_precision: int | float
    permissions: list[str]
    filters: list
    max_quote_amount: float | int
    maker_commission: float | int
    taker_commission: float | int
    quote_amount_precision_market: float | int
    max_quote_amount_market: float | int
    full_name: str


class ExchangeInformation(BaseSchema):
    timezone: str
    server_time: int
    rate_limits: list
    exchange_filters: list
    symbols: list[SymbolExchangeInformation]


class OrderBook(BaseSchema):
    last_update_id: int
    bids: list[list[str]]
    asks: list[list[str]]
    timestamp: int


class RecentTradesList(BaseSchema):
    id: int | None
    price: str
    qty: str
    quote_qty: str
    time: int
    is_buyer_maker: bool
    is_best_match: bool
    trade_type: str


class CompressedAggregateTradesList(BaseSchema):
    a: int | None
    f: int | None
    l: int | None
    p: str
    q: str
    T: int
    m: bool
    M: bool


class CurrentAveragePrice(BaseSchema):
    mins: int
    price: str


class DayTickerPriceChangeStatistics(BaseSchema):
    symbol: str
    price_change: str
    price_change_percent: str
    prev_close_price: str
    last_price: str
    last_price: str
    bid_price: str
    bid_qty: str
    ask_price: str
    ask_qty: str
    open_price: str
    high_price: str
    low_price: str
    volume: str
    quote_volume: str
    open_time: int
    close_time: int
    count: int | None


class SymbolPriceTicker(BaseSchema):
    symbol: str
    price: str


class SymbolOrderBookTicker(BaseSchema):
    symbol: str
    bid_price: str
    bid_qty: str
    ask_price: str
    ask_qty: str










