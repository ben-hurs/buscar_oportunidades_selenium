import requests
from bs4 import BeautifulSoup

def buscar_detalhes_processos(links):
    resultados = []

    for link in links:
        dados = {
            "numero_processo": link.split("processo.codigo=")[-1].split("&")[0] if "processo.codigo=" in link else "Desconhecido",
            "classe": "Não disponível",
            "assunto": "Não disponível",
            "foro": "Não disponível",
            "vara": "Não disponível",
            "valor_acao": "Não disponível",
            "partes": []
        }

        try:
            response = requests.get(link, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            def extrair_texto(selector):
                el = soup.select_one(selector)
                return el.get_text(strip=True) if el else "Não disponível"

            dados.update({
                "classe": extrair_texto("#classeProcesso"),
                "assunto": extrair_texto("#assuntoProcesso"),
                "foro": extrair_texto("#foroProcesso"),
                "vara": extrair_texto("#varaProcesso"),
                "valor_acao": extrair_texto("#valorAcaoProcesso"),
            })

            partes = soup.select(".nomeParteEAdvogado")
            tipos = soup.select(".tipoDeParticipacao")

            for tipo, parte in zip(tipos, partes):
                dados["partes"].append({
                    "tipo": tipo.get_text(strip=True),
                    "nome": parte.get_text(strip=True)
                })

        except Exception as e:
            dados["erro"] = str(e)

        resultados.append(dados)

    return resultados
