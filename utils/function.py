from urllib.parse import urlparse


class Function:
    @staticmethod
    def get_domain(url: str):
        url = urlparse(url).netloc
        return url
