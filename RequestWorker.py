import urllib.request
from settings import PROXY_ADDRESS

class RequestWorker:
    opener = None
    def __init__(self):
        proxyAddr=PROXY_ADDRESS
        proxy_values = "%(ip)s" % {'ip': proxyAddr}
        proxies = {"http": proxy_values, "https": proxy_values}
        handler = urllib.request.ProxyHandler(proxies)
        self.opener = urllib.request.build_opener(handler)

    def get(self, url):
        req = urllib.request.Request(url)
        return self.opener.open(req)

