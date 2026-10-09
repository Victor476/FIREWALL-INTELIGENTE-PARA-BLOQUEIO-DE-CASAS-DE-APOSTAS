import random
import shutil
from typing import Optional, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

try:
    from selenium_stealth import stealth
    HAS_SELENIUM_STEALTH = True
except ImportError:
    HAS_SELENIUM_STEALTH = False

# Lista diversificada de User-Agents reais e modernos (Windows, macOS e Linux)
USER_AGENTS = [
    # Windows 10/11 - Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    # macOS - Chrome
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    # Linux - Chrome
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]

# Resoluções comuns de tela para variação de viewport
VIEWPORTS = [
    (1920, 1080),
    (1366, 768),
    (1536, 864),
    (1440, 900),
    (1280, 720)
]

def get_random_user_agent() -> str:
    """Retorna um User-Agent aleatório a partir do pool diversificado."""
    return random.choice(USER_AGENTS)

def get_platform_from_ua(user_agent: str) -> str:
    """Extrai a plataforma correspondente para o navigator.platform."""
    if "Macintosh" in user_agent:
        return "MacIntel"
    elif "Windows" in user_agent:
        return "Win32"
    return "Linux x86_64"

def get_stealth_options(
    user_agent: Optional[str] = None,
    window_size: Optional[Tuple[int, int]] = None,
    headless: bool = True
) -> Tuple[Options, str, Tuple[int, int]]:
    """
    Constrói as opções do Chrome com remoção de flags de automação
    e cabeçalhos realistas.
    """
    ua = user_agent or get_random_user_agent()
    width, height = window_size or random.choice(VIEWPORTS)

    options = Options()
    
    if headless:
        options.add_argument("--headless=new")
        
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument(f"user-agent={ua}")
    
    # Mascarar cabeçalhos de idioma e recursos de automação
    options.add_argument("--lang=pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Remove flags e variáveis que identificam o WebDriver
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Identificar binário do Chromium no container Linux
    chrome_bin = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
    if chrome_bin:
        options.binary_location = chrome_bin

    return options, ua, (width, height)

def create_stealth_driver(
    user_agent: Optional[str] = None,
    window_size: Optional[Tuple[int, int]] = None,
    headless: bool = True
) -> Tuple[webdriver.Chrome, str]:
    """
    Instancia e retorna um WebDriver com todas as técnicas anti-bot e anti-detecção
    configuradas (Issue #09).
    """
    options, ua, (width, height) = get_stealth_options(user_agent, window_size, headless)
    platform_name = get_platform_from_ua(ua)

    chromedriver_bin = shutil.which("chromedriver") or "/usr/bin/chromedriver"
    service = Service(executable_path=chromedriver_bin) if shutil.which("chromedriver") else None

    if service:
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    # 1. Aplicar selenium-stealth se disponível
    if HAS_SELENIUM_STEALTH:
        stealth(
            driver,
            languages=["pt-BR", "pt", "en-US", "en"],
            vendor="Google Inc.",
            platform=platform_name,
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

    # 2. Injeção direta via Chrome DevTools Protocol (CDP) para garantir máxima evasão anti-bot
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                // 1. Remove qualquer resquício de webdriver no objeto e protótipos
                try {
                    delete Object.getPrototypeOf(navigator).webdriver;
                } catch (e) {}
                
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });

                // 2. Simula window.chrome completo e runtime
                window.chrome = {
                    runtime: {
                        OnInstalledReason: {
                            CHROME_UPDATE: "chrome_update",
                            INSTALL: "install",
                            SHARED_MODULE_UPDATE: "shared_module_update",
                            UPDATE: "update"
                        },
                        OnRestartRequiredReason: {
                            APP_UPDATE: "app_update",
                            OS_UPDATE: "os_update",
                            PERIODIC: "periodic"
                        },
                        PlatformArch: {
                            ARM: "arm",
                            ARM64: "arm64",
                            MIPS: "mips",
                            MIPS64: "mips64",
                            X86_32: "x86-32",
                            X86_64: "x86-64"
                        },
                        PlatformNaclArch: {
                            ARM: "arm",
                            MIPS: "mips",
                            MIPS64: "mips64",
                            X86_32: "x86-32",
                            X86_64: "x86-64"
                        },
                        PlatformOs: {
                            ANDROID: "android",
                            CROS: "cros",
                            LINUX: "linux",
                            MAC: "mac",
                            OPENBSD: "openbsd",
                            WIN: "win"
                        }
                    },
                    loadTimes: function() {},
                    csi: function() {},
                    app: {}
                };

                // 3. Simula permissões de notificações realistas
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );

                // 4. Simula linguagens do sistema
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['pt-BR', 'pt', 'en-US', 'en']
                });
            """
        }
    )

    return driver, ua
