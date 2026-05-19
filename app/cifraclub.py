"""CifraClub Module"""

import requests
from bs4 import BeautifulSoup

CIFRACLUB_URL = "https://www.cifraclub.com.br/"


class CifraClub:
    """CifraClub Class"""

    def cifra(self, artist: str, song: str) -> dict:
        result = {}

        url = CIFRACLUB_URL + artist.strip("/") + "/" + song.strip("/") + "/"
        result["cifraclub_url"] = url

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        }

        try:
            r = requests.get(url, headers=headers, timeout=30)
            result["http_status"] = r.status_code

            if r.status_code != 200:
                result["error"] = f"HTTP {r.status_code}"
                return result

            soup = BeautifulSoup(r.text, "html.parser")

            titulo = soup.find("h1", class_="t1")
            artista = soup.find("h2", class_="t3")
            pre = soup.find("pre")

            result["name"] = titulo.get_text(strip=True) if titulo else song
            result["artist"] = artista.get_text(strip=True) if artista else artist
            result["cifra"] = pre.get_text("\n").split("\n") if pre else []

            if not result["cifra"]:
                result["error"] = "Bloco de cifra nao encontrado"

            return result

        except Exception as e:
            result["error"] = str(e)
            return result
