import asyncio

from mexc_api.clients.mexc import MEXCClient
from mexc_api.methods.spot_v3.marked_data import MarkedData


async def main() -> None:
    client = MEXCClient(logging=True)

    marked_data = MarkedData(client)

    pair_name = "TONUSDT"

    average_price = await marked_data.current_average_price(pair_name)

    print(f"{pair_name} price: {average_price.price}")

    await client.close_session()

if __name__ == "__main__":
    asyncio.run(main())
