import requests
from app.config import API_URL, API_KEY, API_GITHUB_URL


class APIClient:
    def __init__(self):
        self.base_url = API_URL
        self.url_git = API_GITHUB_URL
        self.headers = {
            "apikey": f"{API_KEY}",
            "Content-Type": "application/json",
        }

    def chamar_endpoint(self, endpoint: str, urls_params: dict | None = None, *, use_github: bool = False):
        """Chama um endpoint formatado no Nexus (padrão) ou no GitHub (quando use_github=True)."""

        endpoint_str = endpoint.format(**(urls_params or {}))

        if use_github:
            url = f"{self.url_git}/{endpoint_str}"
            headers = {"Accept": "application/vnd.github.v3+json"}
        else:
            url = f"{self.base_url}/{endpoint_str}"
            headers = self.headers

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
