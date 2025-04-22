
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

TRIBUNAIS = [
    "https://esaj.tjsp.jus.br",
    "https://www2.tjal.jus.br",
    "https://esaj.tjce.jus.br"
]

def buscar_em_tribunal(nome_parte, base_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    links = []

    try:
        driver.get(base_url + "/cpopg/search.do")
        time.sleep(random.uniform(2, 3))

        Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cbPesquisa"))
        )).select_by_value("NMPARTE")

        input_element = driver.find_element(By.ID, "campo_NMPARTE")
        input_element.send_keys(nome_parte)
        input_element.submit()
        time.sleep(5)

        while True:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.linkProcesso"))
            )

            processos = driver.find_elements(By.CSS_SELECTOR, "a.linkProcesso")
            for processo in processos:
                href = processo.get_attribute("href")
                if href:
                    link_absoluto = href if href.startswith("http") else base_url + href
                    links.append(link_absoluto)

            try:
                proxima = driver.find_element(By.CSS_SELECTOR, "a.unj-pagination__next")
                href = proxima.get_attribute("href")
                if href:
                    next_page = href if href.startswith("http") else base_url + href
                    driver.get(next_page)
                    time.sleep(random.uniform(2, 3))
                else:
                    break
            except:
                break

    except Exception as e:
        print("Erro ao buscar:", e)
    finally:
        driver.quit()

    return links

# if __name__ == "__main__":
#     nome_parte = "natura"

#     for base_url in TRIBUNAIS:
#         print(f"🔍 Buscando processos para: {nome_parte} em {base_url}")
#         links = buscar_em_tribunal(nome_parte, base_url)

#         for link in links:
#             print(link)

#         print(f"✅ Total de links encontrados em {base_url}: {len(links)}")
#         print("-" * 50)
