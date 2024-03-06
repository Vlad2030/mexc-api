import uvicorn
from fastapi import FastAPI
from fastapi import status
from pydantic import BaseModel

from mexc_api.clients.mexc import MEXCClient
from mexc_api.methods.spot_v3.marked_data import MarkedData


app = FastAPI(
    title="MEXC API example app",
    version="0.0.1",
    docs_url="/docs"
)


class RequestSymbols(BaseModel):
    symbols: str | list[str] = "ETH"


class Pair(BaseModel):
    pair: str = "USDT"
    price: float | int = 3262.198


class Symbol(BaseModel):
    symbol: str = "ETH"
    availble_pairs: list[str] = ["USDT"]
    pairs: list[Pair]


class ResponseSymbols(BaseModel):
    symbols: list[Symbol]


@app.post(
    path="/price/",
    response_model=ResponseSymbols,
    status_code=status.HTTP_200_OK,
)
async def get_prices(symbol: RequestSymbols) -> ResponseSymbols:
    client = MEXCClient(logging=True)
    marked_data = MarkedData(client)

    symbols = symbol.symbols if isinstance(symbol.symbols, list) else [symbol.symbols]
    symbols_list = []
    pairs = ("USDT", "USDC", "ETH", "BTC", "TUSD")

    ticker_prices = await marked_data.symbol_price_ticker()

    for symbol in symbols:
        symbol_dict_schema = {
            "symbol": symbol,
            "availble_pairs": [],
            "pairs": [],
        }

        for ticker_price in ticker_prices:
            if ticker_price.symbol.startswith(symbol):
                availble_pair = ticker_price.symbol.split(symbol)[1]
                if availble_pair.startswith(pairs):
                    symbol_dict_schema["availble_pairs"].append(availble_pair)
                    symbol_dict_schema["pairs"].append(
                        Pair(pair=availble_pair, price=float(ticker_price.price)),
                    )
        symbols_list.append(Symbol(**symbol_dict_schema))

    await client.close_session()

    return ResponseSymbols(symbols=symbols_list)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)