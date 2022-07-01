from PyRoxy import Proxy, ProxyChecker, ProxyType, ProxyUtiles
from requests import get, exceptions
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Set, Any
from secrets import choice as randchoice
from contextlib import suppress
from json import load
from pathlib import Path
from colorama import Fore, init
from datetime import datetime
from pytz import timezone
import random
import pyfiglet
import os
import requests

__dir__: Path = Path(__file__).parent
init(autoreset=True)

red = Fore.LIGHTRED_EX
white = Fore.WHITE
green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
CHUNK_PARRENT = 1

with open(__dir__ / "config.json") as f:
    con = load(f)

class ProxyManager:

    @staticmethod
    def DownloadFromConfig(cf, Proxy_type: int) -> Set[Proxy]:
        providrs = [
            provider for provider in cf["proxy-providers"]
            if provider["type"] == Proxy_type or Proxy_type == 0
        ]
        proxes: Set[Proxy] = set()

        with ThreadPoolExecutor(len(providrs)) as executor:
            future_to_download = {
                executor.submit(
                    ProxyManager.download, provider,
                    ProxyType.stringToProxyType(str(provider["type"])))
                for provider in providrs
            }
            for future in as_completed(future_to_download):
                for pro in future.result():
                    proxes.add(pro)
        return proxes

    @staticmethod
    def download(provider, proxy_type: ProxyType) -> Set[Proxy]:
        proxes: Set[Proxy] = set()
        with suppress(TimeoutError, exceptions.ConnectionError,
                      exceptions.ReadTimeout):
            data = get(provider["url"], timeout=provider["timeout"]).text
            try:
                for proxy in ProxyUtiles.parseAllIPPort(
                        data.splitlines(), proxy_type):
                    proxes.add(proxy)
            except Exception as e:
                pass
        return proxes

def randomProxy():
    proxy_file = open("proxy.txt", "r").readlines()
    proxy_data = random.choice(proxy_file)
    return {
        "http": "http://" + proxy_data.replace("http://", "").replace("https://", "").strip(),
        "https": "http://" + proxy_data.replace("http://", "").replace("https://", "").strip()
    }

def logTime():
    now_utc = datetime.now(timezone('UTC'))
    now_pacific = now_utc.astimezone(timezone("Asia/Jakarta"))
    return now_pacific.strftime("%H:%M:%S")

def banner(str):
    os.system("cls||clear")
    my_banner = pyfiglet.figlet_format(str, font="slant", justify="center")
    print(red + my_banner)
    print(f"\t\t\t{red}[ {white}Created By X-MrG3P5 {red}]\n")

def generateDeviceID():
    string = "qwertyuiopasdfghjklzxcvbnm1234567890"
    random_str = "".join(random.sample(string, 8))
    return random_str + "-6cfe-4156-ae34-268fadf064a3"

class SpamNGL:

    @staticmethod
    def starts(username, total_spam: int, thread: int, message):
        print(f"{red}[{white}{logTime()}{red}] {white}Start Spamming...")

        with ThreadPoolExecutor(thread) as executor:
            executor.submit(SpamNGL.start, username, total_spam, message)

    @staticmethod
    def start(username, total_spam: int, message):
        global CHUNK_PARRENT
        while CHUNK_PARRENT <= total_spam:
            try:
                randomProxies = randomProxy()
                session = requests.Session()
                session.proxies.setdefault('http', 'http://127.0.0.1:9009')
                session.proxies.update(randomProxies)

                req = session.post(f"https://ngl.link/{username}", data={
                    "question": message,
                    "deviceId": generateDeviceID()
                }, proxies=randomProxies, timeout=3)

                if req.status_code == 200:
                    print(f"{red}[{white}{logTime()}{red}] {white}Spamming Ke {green}{CHUNK_PARRENT}")
                    for j in range(12):
                        reqs = session.post(f"https://ngl.link/{username}", data={
                            "question": message,
                            "deviceId": generateDeviceID()
                        }, proxies=randomProxies, timeout=3)
                        if reqs.status_code == 200:
                            print(f"{red}[{white}{logTime()}{red}] {white}Spamming Ke {green}{CHUNK_PARRENT}")
                            CHUNK_PARRENT += 1
                        else:
                            pass
                else:
                    print(f"{red}[{white}{logTime()}{red}] {white}Failed with status code {yellow}{req.status_code}")
            except:
                pass

def handleProxyList(con, proxy_li, proxy_ty):
    if proxy_ty not in {4, 5, 1, 0, 6}:
        exit("Socks Type Not Found [4, 5, 1, 0, 6]")
    if proxy_ty == 6:
        proxy_ty = randchoice([4, 5, 1])
    if not proxy_li.exists():
        proxy_li.parent.mkdir(parents=True, exist_ok=True)
        with proxy_li.open("w") as wr:
            Proxies: Set[Proxy] = ProxyManager.DownloadFromConfig(con, proxy_ty)
            print(f"{red}[{white}{logTime()}{red}] {green}{len(Proxies):,} {white}Proxies are getting checked, this may take a while!")
            Proxies = ProxyChecker.checkAll(Proxies, timeout=1, threads=200, url="https://ngl.link",)

            if not Proxies:
                exit(f"{red}[{yellow}!{red}] {white}Proxy Check failed, Your network may be the problem")
            stringBuilder = ""
            for proxy in Proxies:
                stringBuilder += (proxy.__str__() + "\n")
            wr.write(stringBuilder)

    proxies = ProxyUtiles.readFromFile(proxy_li)
    if proxies:
        print(f"{red}[{white}{logTime()}{red}] {white}Proxy Count: {green}{len(proxies):,}")
    else:
        print(f"{red}[{yellow}!{red}] {white}Empty Proxy File, running flood witout proxy")
        proxies = None

    return proxies

if __name__ == '__main__':
    banner("NGL - SPAM")
    input_username = input(f"{red}[{white}?{red}] {white}Username Target : ")
    input_total_spam = input(f"{red}[{white}?{red}] {white}Total Spam : ")
    input_message = input(f"{red}[{white}?{red}] {white}Message : ")
    input_thread = input(f"{red}[{white}?{red}] {white}Thread : ")
    if os.path.exists("proxy.txt"):
        print(f"{red}[{white}{logTime()}{red}] {white}Proxies File Found..")
        proxies = ProxyUtiles.readFromFile("proxy.txt")
        print(f"{red}[{white}{logTime()}{red}] {white}Proxy Count: {green}{len(proxies):,}")
        SpamNGL.starts(input_username, int(input_total_spam), int(input_thread), input_message)
    else:
        print(f"{red}[{white}{logTime()}{red}] {white}Downloading Proxies..")
        Proxies: Set[Proxy] = ProxyManager.DownloadFromConfig(con, 1)
        proxies: Any = set()
        proxy_li = Path(__dir__ / "proxy.txt")
        proxies = handleProxyList(con, proxy_li, 1)
        SpamNGL.starts(input_username, int(input_total_spam), int(input_thread), input_message)
