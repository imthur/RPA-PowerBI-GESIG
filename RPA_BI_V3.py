import time
import os
import pyautogui
import psutil
import logging
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import traceback

# Configurações Globais
load_dotenv()
rpa_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(rpa_dir, "rpa.log")

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger()

pyautogui.PAUSE = 1

def wait(seconds=1):
    time.sleep(seconds)

def iniciar_driver():
    """Inicia o driver do Chrome com as opções configuradas."""
    chrome_path = os.path.join(rpa_dir, "chromedriver.exe")
    service = Service(chrome_path)
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('--enable-unsafe-swiftshader')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument('--disable-features=VoiceTranscription')
    options.add_argument('--log-level=3')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--disable-speech-api')
    return webdriver.Chrome(service=service, options=options)

def esperar_com_verificacao(total_segundos=30, tempo_parado=15):
    tempo_restante = total_segundos
    print(f"Iniciando contagem de {total_segundos} segundos...")

    while tempo_restante > 0:
        inicio = time.time()
        pos_inicial = pyautogui.position()

        # Espera 1 segundo se não houver movimento
        time.sleep(1)
        pos_atual = pyautogui.position()

        if pos_atual != pos_inicial:
            print("Movimento do mouse detectado! Pausando contagem...")
            parado_inicio = time.time()

            # Espera o mouse ficar parado por 'tempo_parado'
            while True:
                time.sleep(0.5)
                nova_pos = pyautogui.position()

                if nova_pos != pos_atual:
                    # Reinicia contagem de tempo parado se mexer
                    parado_inicio = time.time()
                    pos_atual = nova_pos
                    print("Mouse ainda se mexendo...")

                elif time.time() - parado_inicio >= tempo_parado:
                    print(f"Mouse parado por {tempo_parado} segundos. Retomando contagem.")
                    break
        else:
            tempo_passado = time.time() - inicio
            tempo_restante -= tempo_passado
            print(f"Restam {round(tempo_restante)} segundos...")

    print("Tempo finalizado!")

def fazer_login(driver, login, senha):
    """Realiza o processo de login no site e fecha o aviso de automação."""
    try:
        pyautogui.click(x=1891, y=116)
        print("Aviso de automação fechado.")
        wait(2)
        pyautogui.click(x=1000, y=188)
        print(f"Login: {login}")
        pyautogui.write(login)
        wait(2)
        pyautogui.click(x=1000, y=250)
        pyautogui.write(senha)
        wait(2)
        pyautogui.click(x=925, y=295)
        return True
    except Exception as e:
        logger.error(f"Erro ao fazer login: {e}")
        return False

def alternar_aba(driver, indice):
    """Alterna para a aba especificada."""
    try:
        if indice < len(driver.window_handles):
            driver.switch_to.window(driver.window_handles[indice])
            return True
        return False
    except Exception as e:
        logger.error(f"Erro ao alternar aba: {e}")
        return False

def atualizar_abas(driver):
    """Atualiza todas as abas abertas."""
    try:
        for i in range(len(driver.window_handles)):
            driver.switch_to.window(driver.window_handles[i])
            driver.refresh()
            wait(2)
        return True
    except Exception as e:
        logger.error(f"Erro ao atualizar abas: {e}")
        return False

for proc in psutil.process_iter(['name', 'cmdline']):
    try:
        cmdline = proc.info.get('cmdline')
        if proc.info['name'] == 'chromedriver.exe' or (
            isinstance(cmdline, (list, tuple)) and 'chromedriver' in ' '.join(cmdline)
        ):
            proc.kill()
    except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
wait(2)

driver = iniciar_driver()

links = []
for i in range(1, 5):
    link = os.getenv(f'LINK_{i}')
    if link:
        links.append(link)

if not links:
    logger.error("Nenhum link encontrado no arquivo .env")

driver.get(links[0])

login = os.getenv("USERNAME")
senha = os.getenv("PASSWORD")

if not login or not senha:
    driver.quit()
    logger.error("Login ou senha não encontrados no arquivo .env")

if not fazer_login(driver, login, senha):
    driver.quit()
    logger.error("Falha ao fazer login. Verifique as credenciais.")

for link in links[1:]:
    driver.execute_script(f"window.open('{link}', '_blank');")
    wait(5)

# Fecha a aba inicial [apenas para login]
driver.switch_to.window(driver.window_handles[0])
driver.close()

driver.switch_to.window(driver.window_handles[1])
wait(20)
pyautogui.click(x=255, y=1022)

wait(2)
driver.switch_to.window(driver.window_handles[2])

print("RPA configurado. Iniciando ciclo de visualização!")
pyautogui.press('f11')
wait(5)

try:
    ciclos = 0
    while True:
        for i in range(len(driver.window_handles)):
            if alternar_aba(driver, i):
                print(f"Visualizando aba {i + 1} de {len(driver.window_handles)}")
                esperar_com_verificacao(30, 15)
        ciclos += 1
        print(f"{ciclos}° ciclo de visualização Concluído.")
        if ciclos >= 3:
            atualizar_abas(driver)
            ciclos = 0
except Exception as e:
    logger.error(f"Erro durante o ciclo de visualização: {e}")
    traceback.print_exc()