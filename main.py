import asyncio
from tqdm.asyncio import tqdm_asyncio
import aiohttp
from better_proxy import Proxy
from aiohttp_socks import ProxyConnector
import os
from dotenv import load_dotenv

load_dotenv()

failed = 0

async def requets_tokens(wallet: str, proxy: str) -> int:
    global failed
    
    api_key = os.getenv("CAPSOLVER_KEY")
    proxy = Proxy.from_str(proxy)
    connector = ProxyConnector.from_url(proxy.as_url)

    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.post(
            "https://api.capsolver.com/createTask",
            json={
                "clientKey": api_key,
                "task": {
                    "type": "ReCaptchaV3TaskProxyLess",
                    "websiteURL": "https://artio.faucet.berachain.com/",
                    "websiteKey": "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH",
                    "pageAction": "submit",
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
                        captcha_token = captcha_solve_status["solution"][
                            "gRecaptchaResponse"
                        ]
                        break

        async with session.post(
            f"https://artio-80085-faucet-api-recaptcha.berachain.com/api/claim?address={wallet}",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Authorization": f"Bearer {captcha_token}",
            },
            json={"address": wallet},
        ) as response:
            
            if response.status != 200:
                failed += 1
            
            return response.status


async def main():
    wallets_file = "./data/wallets.txt"
    proxies_file = "./data/proxies.txt"

    wallets = [line.strip() for line in open(wallets_file, "r")]
    proxies = [line.strip() for line in open(proxies_file, "r")]

    tasks = []
    for wallet, proxy in zip(wallets, proxies):
        tasks.append(requets_tokens(wallet, proxy))

    await tqdm_asyncio.gather(*tasks, desc=f"Processing", unit=" accs")

    print(f"Requests done.")
    print(f"Failed Requests: {failed}")


if __name__ == "__main__":
    asyncio.run(main())
