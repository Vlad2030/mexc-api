import asyncio

from mexc_api.clients.mexc import MEXCClient
from mexc_api.methods.spot_v3.marked_data import MarkedData


async def main() -> None:
    client = MEXCClient()

    marked_data = MarkedData(client)

    pair_price = await marked_data.symbol_price_ticker("BTCUSDT")
    print(pair_price)

    await client.close_session()

if __name__ == "__main__":
    asyncio.run(main())
