import asyncio
from tqdm.asyncio import tqdm_asyncio
import aiohttp
from better_proxy import Proxy
from aiohttp_socks import ProxyConnector
import os
from dotenv import load_dotenv
from prettytable import PrettyTable

load_dotenv()

overloaded_request = 0
successful_request = 0
cooldown_request = 0
error_request = 0


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
                    "type": "AntiCloudflareTask",
                    "websiteURL": "https://artio.faucet.berachain.com/",
                    "websiteKey": "0x4AAAAAAABS7vwvV6VFfMcD",
                    "proxy": f"socks5:{str_proxy.host}:{str_proxy.port}:{str_proxy.login}:{str_proxy.password}",
                },
            },
        ) as response:
            captcha_task = await response.json()

            print(captcha_task)
            return

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
            f"https://artio-80085-faucet-api-cf.berachain.com/api/claim?address={wallet}",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Authorization": f"Bearer {captcha_token}",
            },
            json={"address": wallet},
        ) as response:
            if response.status == 200:
                successful_request += 1
            elif response.status == 429:
                overloaded_request += 1
            elif response.status == 401:
                cooldown_request += 1
            else:
                error_request += 1

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
        tasks.append(requets_tokens(wallet, proxy))

    await tqdm_asyncio.gather(*tasks, desc=f"Requesting", unit=" accs", colour="CYAN")

    table = PrettyTable()

    table.field_names = [
        "Wallets",
        "Successful Requests",
        "Cooldown Requests",
        "Error Requests",
        "Overloaded Requests",
    ]

    table.add_row(
        [
            len(wallets),
            successful_request,
            cooldown_request,
            error_request,
            overloaded_request,
        ]
    )

    table.align["Wallets"] = "r"
    table.align["Successful Requests"] = "r"
    table.align["Cooldown Requests"] = "r"
    table.align["Error Requests"] = "r"
    table.align["Overloaded Requests"] = "r"

    print(table)


if __name__ == "__main__":
    asyncio.run(main())
