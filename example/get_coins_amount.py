import asyncio

from mexc_api.clients.mexc import MEXCClient
from mexc_api.methods.spot_v3.marked_data import MarkedData


async def main() -> None:
    client = MEXCClient()

    marked_data = MarkedData(client)

    request = await marked_data.api_default_symbol()

    coin_amount = len(request.data)

    print(f"Coins amount = {coin_amount}")

    await client.close_session()

if __name__ == "__main__":
    asyncio.run(main())
