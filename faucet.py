import concurrent.futures
import requests
import capsolver
from dotenv import load_dotenv
import os
from random import randint
from time import sleep
from loguru import logger

load_dotenv()


class Faucet:
    @staticmethod
    def get_captcha(api_key: str) -> str:
        capsolver.api_key = api_key
        capsolver_data = {
            "type": "ReCaptchaV3TaskProxyLess",
            "websiteURL": "https://artio.faucet.berachain.com/",
            "websiteKey": "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH",
            "pageAction": "submit",
        }
        solution = capsolver.solve(capsolver_data)
        return solution["gRecaptchaResponse"]

    @staticmethod
    def dripFaucet(address: str, proxy: dict, token: str) -> dict:
        url = f"https://artio-80085-ts-faucet-api-2.berachain.com/api/claim?address={address}"
        headers = {
            "Host": "artio-80085-ts-faucet-api-2.berachain.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://artio.faucet.berachain.com/",
            "Authorization": f"Bearer {token}",
            "Content-Type": "text/plain;charset=UTF-8",
            "Content-Length": "56",
            "Origin": "https://artio.faucet.berachain.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "TE": "trailers",
        }

        data = {"address": address}

        response = requests.post(url, json=data, headers=headers, proxies=proxy)

        return response


def process_wallet(wallet, proxy):
    api_key = os.getenv("CAPSOLVER_KEY")
    token = Faucet.get_captcha(api_key)
    result = Faucet.dripFaucet(wallet, {"http": proxy, "https": proxy}, token)

    wallet = wallet.strip()

    if result.status_code == 200:
        logger.success(f"Wallet: {wallet} successfully claimed from faucet")
    else:
        logger.warning(f"Wallet {wallet} error, {result.text}")
    sleep(randint(20, 50))


if __name__ == "__main__":
    wallets_file = "./data/wallets.txt"
    proxies_file = "./data/proxies.txt"

    wallets = [line.strip() for line in open(wallets_file, "r")]
    proxies = [line.strip() for line in open(proxies_file, "r")]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_wallet, wallets, proxies)
