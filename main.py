import asyncio
from tqdm.asyncio import tqdm_asyncio
import aiohttp
from better_proxy import Proxy
from aiohttp_socks import ProxyConnector
import os
from dotenv import load_dotenv
from prettytable import PrettyTable

load_dotenv()

successful_request = {}
cooldown_request = {}
error_request = {}


async def requets_tokens(wallet: str, proxy: str) -> int:
    global overloaded_request, successful_request, error_request, cooldown_request

    api_key = os.getenv("CAPSOLVER_KEY")
    str_proxy = Proxy.from_str(proxy)
    connector = ProxyConnector.from_url(str_proxy.as_url)

    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.post(
            "https://api.capsolver.com/createTask",
            json={
                "clientKey": api_key,
                "task": {
                    "type": "AntiTurnstileTaskProxyLess",
                    "websiteURL": "https://bartio.faucet.berachain.com/",
                    "websiteKey": "0x4AAAAAAARdAuciFArKhVwt",
                },
            },
        ) as response:
            captcha_task = await response.json()

            while True:
                async with session.post(
                    "https://api.capsolver.com/getTaskResult",
                    json={
                        "clientKey": api_key,
                        "taskId": captcha_task["taskId"],
                    },
                ) as response:
                    captcha_solve_status = await response.json()
                    if captcha_solve_status["status"] == "ready":
                        captcha_token = captcha_solve_status["solution"]["token"]
                        break

        async with session.post(
            f"https://bartio-faucet.berachain-devnet.com/api/claim?address={wallet}",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Authorization": f"Bearer {captcha_token}",
            },
            json={"address": wallet},
        ) as response:
            if response.status == 200:
                successful_request[wallet] = "Success"
            elif response.status == 429:
                cooldown_request[wallet] = "Wallet in cooldown, try again later"
            else:
                error_request[wallet] = f"Failed request, reason: {response.text}"

            return response.status


async def main():
    wallets_file = "./data/wallets.txt"
    proxies_file = "./data/proxies.txt"

    wallets = [line.strip() for line in open(wallets_file, "r")]
    proxies = [line.strip() for line in open(proxies_file, "r")]

    if len(wallets) != len(proxies):
        print("Wallets and proxies amount are not equal!")
        return

    tasks = []
    for wallet, proxy in zip(wallets, proxies):
        if len(wallet) > 42:
            error_request[wallet] = "Wrong wallet format"
        else:
            tasks.append(requets_tokens(wallet, proxy))

    await tqdm_asyncio.gather(*tasks, desc=f"Requesting", unit=" accs", colour="CYAN")

    table = PrettyTable()

    table.field_names = [
        "Wallets",
        "Successful",
        "Cooldown ",
        "Failed",
    ]

    table.add_row(
        [
            len(wallets),
            len(successful_request.keys()),
            len(cooldown_request.keys()),
            len(error_request.keys()),
        ]
    )

    table.align["Wallets"] = "r"
    table.align["Successful"] = "r"
    table.align["Cooldown"] = "r"
    table.align["Failed"] = "r"
    print(table)

    if len(error_request.keys()) > 0:
        print("Failed wallets:")
        for wallet, reason in error_request.items():
            print(f"{wallet}: {reason}")


if __name__ == "__main__":
    asyncio.run(main())
