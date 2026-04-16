import requests
from urllib3.util.ssl_ import create_urllib3_context
from requests.adapters import HTTPAdapter

class LegacyAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.options |= 0x4  # Enable legacy renegotiation
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)


session = requests.Session()
session.mount("https://", LegacyAdapter())