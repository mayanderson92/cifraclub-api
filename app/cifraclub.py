"""CifraClub Module"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

CIFRACLUB_URL = "https://www.cifraclub.com.br/"


class CifraClub:
    """CifraClub Class"""

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1365,768")
        chrome_options.add_argument("--lang=pt-BR")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )

        self.driver = webdriver.Chrome(options=chrome_options)

    def cifra(self, artist: str, song: str) -> dict:
        """Lê a página HTML e extrai a cifra e metadados da música."""
        result = {}

        url = CIFRACLUB_URL + artist.strip("/") + "/" + song.strip("/") + "/"
        result["cifraclub_url"] = url

        try:
            self.driver.get(url)
            self.get_details(result)
            self.get_cifra(result)

        except Exception as error:
            result["error"] = str(error)

        finally:
            try:
                self.driver.quit()
            except Exception:
                pass

        return result

    def get_details(self, result):
        """Obtém os metadados da música."""
        content = self.driver.find_element(By.CLASS_NAME, "cifra").get_attribute("outerHTML")
        soup = BeautifulSoup(content, "html.parser")

        titulo = soup.find("h1", class_="t1")
        artista = soup.find("h2", class_="t3")

        result["name"] = titulo.get_text(strip=True) if titulo else ""
        result["artist"] = artista.get_text(strip=True) if artista else ""

        player = soup.find("div", class_="player-placeholder")
        img = player.find("img") if player else None

        if img and img.get("src") and "/vi/" in img["src"]:
            cod = img["src"].split("/vi/")[1].split("/")[0]
            result["youtube_url"] = f"https://www.youtube.com/watch?v={cod}"
        else:
            result["youtube_url"] = ""

    def get_cifra(self, result):
        """Obtém a cifra da música e converte para JSON."""
        content = self.driver.find_element(By.CLASS_NAME, "cifra_cnt").get_attribute("outerHTML")
        soup = BeautifulSoup(content, "html.parser")

        pre = soup.find("pre")

        if not pre:
            result["cifra"] = []
            result["error"] = "Bloco de cifra nao encontrado"
            return

        result["cifra"] = pre.get_text("\n").split("\n")
