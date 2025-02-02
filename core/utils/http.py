import http.client
import ssl
from contextlib import contextmanager


@contextmanager
def https_connection(url: str, port: int, ctx: ssl.SSLContext | None = None):
    conn = http.client.HTTPSConnection(host=url, port=port, context=ctx)
    try:
        yield conn
    finally:
        conn.close()
