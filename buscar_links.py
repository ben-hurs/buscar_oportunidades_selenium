
import requests
from bs4 import BeautifulSoup
import urllib.parse

TRIBUNAIS = [
    "https://esaj.tjsp.jus.br",
    "https://www2.tjal.jus.br",
    "https://esaj.tjce.jus.br"
]

def buscar_em_tribunal(nome_parte, base_url):
    session = requests.Session()
    links = []

    url_busca = base_url + "/cpopg/search.do"
    url_resultado = base_url + "/cpopg/show.do"

    # Etapa 1: acessar a página inicial para obter cookies e headers corretos
    session.get(url_busca)

    # Etapa 2: fazer o POST com os dados da parte
    data = {
        "cbPesquisa": "NMPARTE",
        "dadosConsulta.valorConsulta": nome_parte,
        "dadosConsulta.tipoNuProcesso": "UNIFICADO",
        "tipoNuProcesso": "UNIFICADO",
        "numeroDigitoAnoUnificado": "",
        "foroNumeroUnificado": "",
        "dadosConsulta.valorConsultaNuUnificado": "",
        "dadosConsulta.valorConsultaNuAntigo": "",
        "uuidCaptcha": ""
    }

    response = session.post(url_busca, data=data)
    soup = BeautifulSoup(response.text, "html.parser")

    processos = soup.select("a.linkProcesso")
    for processo in processos:
        href = processo.get("href")
        if href:
            link_completo = urllib.parse.urljoin(base_url, href)
            links.append(link_completo)

    return links
