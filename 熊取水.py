import requests
import capsolver

# Proxy configuration
PROXIES = {"http": "127.0.0.1:7890", "https": "127.0.0.1:7890"}
address = "0x7fed8d3000b3EB6c3bd27B584D78Da75a9B67266"


def get_captcha():
    capsolver.api_key = "自己去花钱买!!!"  # capsolver.com
    capsolver_data = {
        "type": "ReCaptchaV3TaskProxyLess",
        "websiteURL": "https://artio.faucet.berachain.com/",
        "websiteKey": "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH",
        "pageAction": 'submit'
    }
    solution = capsolver.solve(capsolver_data)
    return solution['gRecaptchaResponse']


token = get_captcha()
print(token)


def get_token(address):
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

    response = requests.post(url, json=data, headers=headers, proxies=PROXIES)

    print(response.status_code)
    print(response.text)


get_token(address)
