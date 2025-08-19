from bs4 import BeautifulSoup
import requests

def ipAddressChecker(ipAdd: str) -> str:
    URI: str = f"https://blacklistchecker.com/check?input={ipAdd}"
    response = requests.get(URI)

    if response.status_code == 200:
        htmlText = response.text
        bs4Obj = BeautifulSoup(htmlText, "html.parser")
        print(htmlText)
    
print(ipAddressChecker("209.85.220.48"))