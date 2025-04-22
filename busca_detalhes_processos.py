
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def buscar_detalhes_processos(links):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    resultados = []

    for link in links:
        dados = {
            "numero_processo": link.split("processo.codigo=")[-1] if "processo.codigo=" in link else "Desconhecido",
            "classe": "Não disponível",
            "assunto": "Não disponível",
            "foro": "Não disponível",
            "vara": "Não disponível",
            "valor_acao": "Não disponível",
            "partes": []
        }

        try:
            driver.get(link)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "classeProcesso"))
            )

            def get_text(selector):
                try:
                    return driver.find_element(By.CSS_SELECTOR, selector).text.strip()
                except:
                    return "Não disponível"

            dados.update({
                "classe": get_text("#classeProcesso"),
                "assunto": get_text("#assuntoProcesso"),
                "foro": get_text("#foroProcesso"),
                "vara": get_text("#varaProcesso"),
                "valor_acao": get_text("#valorAcaoProcesso")
            })

            partes = driver.find_elements(By.CSS_SELECTOR, ".nomeParteEAdvogado")
            tipos = driver.find_elements(By.CSS_SELECTOR, ".tipoDeParticipacao")

            for tipo, parte in zip(tipos, partes):
                dados["partes"].append({
                    "tipo": tipo.text.strip(),
                    "nome": parte.text.strip()
                })

        except Exception as e:
            print("Erro ao buscar detalhes:", e)

        resultados.append(dados)

    driver.quit()
    return resultados

# if __name__ == "__main__":
#     from pprint import pprint

#     # Cole aqui alguns links reais obtidos no buscar_links.py
#     links_exemplo = [
#         "https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=110000GA40000&processo.foro=37&paginaConsulta=3&paginaConsulta=2&conversationId=&cbPesquisa=NMPARTE&dadosConsulta.valorConsulta=natura&cdForo=-1",
#         "https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=120000IE30000&processo.foro=38&paginaConsulta=3&paginaConsulta=2&conversationId=&cbPesquisa=NMPARTE&dadosConsulta.valorConsulta=natura&cdForo=-1",
#         "https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=4200004YI0000&processo.foro=146&paginaConsulta=3&paginaConsulta=2&conversationId=&cbPesquisa=NMPARTE&dadosConsulta.valorConsulta=natura&cdForo=-1",
#         "https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=9P0000CMS0000&processo.foro=349&paginaConsulta=3&paginaConsulta=2&conversationId=&cbPesquisa=NMPARTE&dadosConsulta.valorConsulta=natura&cdForo=-1",
#             ]

#     print(f"🔍 Buscando detalhes para {len(links_exemplo)} processo(s)...")
#     resultados = buscar_detalhes_processos(links_exemplo)

#     for i, processo in enumerate(resultados, start=1):
#         print(f"📄 Processo {i}:")
#         pprint(processo)
#         print("-" * 60)

#     print(f"✅ Total de processos com detalhes coletados: {len(resultados)}")
