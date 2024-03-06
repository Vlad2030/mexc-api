import asyncio

from mexc_api.clients.mexc import MEXCClient
from mexc_api.methods.spot_v3.marked_data import MarkedData

SYMBOL_PAIR = "USDT"
MIN_PRICE = 1
MIN_VOLUME = 1_000_000


async def main() -> None:
    client = MEXCClient()
    marked = MarkedData(client)

    pair_symbols: list[str] = []
    price_symbols: list[list[str]] = []
    volume_symbols: list = []

    print(
        f"MEXC spot analyze\n\n",
        f"Settings",
        f"Symbol pair:\t{SYMBOL_PAIR}",
        f"Min price:\t{MIN_PRICE:.10f} {SYMBOL_PAIR}",
        f"Min 24h volume:\t{MIN_VOLUME} {SYMBOL_PAIR}",
        sep="\n",
        end="\n\n",
    )

    print(f"Getting all spot symbols...")

    symbols = (await marked.api_default_symbol()).data

    print(f"Found {len(symbols)} symbols!", end="\n\n")

    print(f"Starting sorting by {SYMBOL_PAIR} symbol pair...")

    for count, symbol in enumerate(symbols, start=1):
        if symbol.endswith(SYMBOL_PAIR):
            pair_symbols.append(symbol)

        print(f"Sorted {count} pairs!", end="\r")

    print(f"Found {len(pair_symbols)} {SYMBOL_PAIR} symbol pairs!", end="\n\n")

    print(f"Starting sorting by price...")

    symbol_prices = await marked.symbol_price_ticker()

    for count, symbol in enumerate(pair_symbols, start=1):
        for symbol_price in symbol_prices:
            _symbol = symbol_price.symbol
            _price = float(symbol_price.price)

            if symbol == _symbol:
                if _price >= MIN_PRICE:
                    price_symbols.append([symbol, _price])

                    print(f"Sorted {count} pairs", end="\r")

    print(f"Found {len(price_symbols)} pairs with {MIN_PRICE:.6f}+ price!", end="\n\n")

    print(f"Starting sorting by 24h {SYMBOL_PAIR} volume...")

    trades = await marked.day_ticker_price_change_statistics()

    for count, pair_symbol in enumerate(price_symbols, start=1):
        symbol = pair_symbol[0]
        price = pair_symbol[1]

        for trade_symbol in trades:
            _symbol = trade_symbol.symbol
            _volume = float(trade_symbol.volume)

            if _symbol == symbol:
                volume = _volume * price

                if volume >= MIN_VOLUME:
                    volume_symbols.append([symbol, price, volume])

                    print(f"Sorted {count} pairs", end="\r")

    print(f"Found {len(volume_symbols)} pairs with {MIN_VOLUME}+ {SYMBOL_PAIR} volume!", end="\n\n")

    volume_symbols.sort(key=lambda x: x[-1], reverse=True)


    print(f"COUNT\t\tCOIN PAIR\tPRICE\t\t24H VOLUME ({SYMBOL_PAIR})")
    for count, pair in enumerate(volume_symbols, start=1):
        symbol = pair[0]
        price = pair[1]
        volume = pair[2]
        print(f"{count}.\t\t{symbol} \t{price:.8f}\t{volume:.2f}")

    await client.close_session()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())