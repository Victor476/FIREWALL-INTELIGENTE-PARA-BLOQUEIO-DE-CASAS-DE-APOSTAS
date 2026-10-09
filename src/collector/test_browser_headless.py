import sys
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def test_headless_browser(target_url: str = "https://example.com") -> bool:
    """
    Testa a inicialização e execução do navegador Chromium em modo Headless via Selenium.
    Atende aos critérios de aceitação da Issue #08.
    """
    print("=========================================================")
    print("🌐 Teste de Sanidade do Navegador Headless (Issue #08)")
    print("=========================================================")
    
    # Identificar binários disponíveis no sistema
    chrome_bin = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
    chromedriver_bin = shutil.which("chromedriver") or "/usr/bin/chromedriver"
    
    print(f"🔍 Binário do Chromium : {chrome_bin or 'PATH Padrão'}")
    print(f"🔍 Binário ChromeDriver : {chromedriver_bin}")

    options = Options()
    # Modo Headless moderno
    options.add_argument("--headless=new")
    # Argumentos críticos para execução estável em container Docker
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    
    if chrome_bin:
        options.binary_location = chrome_bin

    service = None
    if shutil.which("chromedriver"):
        service = Service(executable_path=shutil.which("chromedriver"))
    
    driver = None
    try:
        print("🚀 Inicializando sessão do Selenium WebDriver...")
        if service:
            driver = webdriver.Chrome(service=service, options=options)
        else:
            driver = webdriver.Chrome(options=options)
            
        print(f"🌍 Acessando URL: {target_url}...")
        driver.set_page_load_timeout(30)
        driver.get(target_url)
        
        page_title = driver.title
        current_url = driver.current_url
        print(f"✅ [OK] Navegação concluída com sucesso!")
        print(f"   └─ Título da página : {page_title}")
        print(f"   └─ URL Final        : {current_url}")
        print("=========================================================")
        return True
    except Exception as e:
        print(f"❌ [ERRO] Falha ao executar navegador headless: {e}")
        print("=========================================================")
        return False
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    success = test_headless_browser(url)
    sys.exit(0 if success else 1)
