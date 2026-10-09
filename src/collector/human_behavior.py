import time
import random
import logging
from typing import Dict, Any, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    WebDriverException,
    StaleElementReferenceException,
    ElementNotInteractableException,
    NoSuchElementException
)

# Configuração de Logging estruturado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("HumanNavigator")

class HumanNavigator:
    """
    Controlador de emulação de comportamento humano para o navegador (Issue #10).
    Simula padrões de rolagem, pausas gaussianas, movimentação de cursor e cliques exploratórios.
    """

    def __init__(self, driver, enable_clicks: bool = True):
        self.driver = driver
        self.enable_clicks = enable_clicks

    def human_delay(self, min_sec: float = 1.2, max_sec: float = 3.5, gaussian: bool = True) -> float:
        """Gera uma pausa com distribuição gaussiana ou uniforme para mimetizar tempo de reação humano."""
        if gaussian:
            mean = (min_sec + max_sec) / 2.0
            std_dev = (max_sec - min_sec) / 6.0  # 99.7% dentro do intervalo
            delay = random.gauss(mean, std_dev)
            delay = max(min_sec, min(delay, max_sec))
        else:
            delay = random.uniform(min_sec, max_sec)
        
        time.sleep(delay)
        return delay

    def smooth_scroll(self, min_step: int = 150, max_step: int = 550) -> int:
        """Executa rolagem gradual com comportamento dinâmico (85% para baixo, 15% para cima)."""
        # 15% de chance de rolar um pouco para cima (comportamento de releitura de odds/notícias)
        if random.random() < 0.15:
            step = -random.randint(100, 300)
        else:
            step = random.randint(min_step, max_step)

        try:
            self.driver.execute_script(f"window.scrollBy({{top: {step}, behavior: 'smooth'}});")
        except WebDriverException as e:
            logger.debug(f"Erro ao executar scroll: {e}")
            step = 0
        return step

    def simulate_hover(self) -> bool:
        """Move o cursor para um elemento visível aleatório para emular atenção visual."""
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a, button, div, span, p, tr")
            if not elements:
                return False

            # Escolhe um subconjunto aleatório para inspecionar
            candidate = random.choice(elements[:30])
            if candidate.is_displayed():
                actions = ActionChains(self.driver)
                actions.move_to_element(candidate).perform()
                return True
        except Exception as e:
            logger.debug(f"Hover ignorado: {e}")
        return False

    def simulate_safe_click(self) -> bool:
        """Executa um clique seguro em elementos de navegação/abas evitando botões de ação sensíveis."""
        if not self.enable_clicks:
            return False

        try:
            # Busca abas, botões informativos ou links neutros
            candidates = self.driver.find_elements(
                By.CSS_SELECTOR,
                "nav a, .tab, .menu-item, [role='tab'], header a, button[type='button']"
            )
            # Filtra palavras-chave arriscadas
            safe_candidates = []
            risky_words = ["submit", "login", "cadastr", "entrar", "deposit", "pagar", "buy", "cart"]

            for el in candidates[:15]:
                try:
                    if not el.is_displayed():
                        continue
                    text = (el.text or "").lower()
                    tag_id = (el.get_attribute("id") or "").lower()
                    if any(w in text or w in tag_id for w in risky_words):
                        continue
                    safe_candidates.append(el)
                except Exception:
                    continue

            if safe_candidates:
                target = random.choice(safe_candidates)
                target.click()
                return True
        except Exception as e:
            logger.debug(f"Clique seguro ignorado: {e}")
        return False

    def run_session(self, url: str, duration_seconds: int = 45) -> Dict[str, Any]:
        """
        Executa a sessão completa de navegação sintética humana durante o tempo configurado.
        """
        logger.info(f"Acessando plataforma alvo: {url}...")
        self.driver.get(url)
        
        # Pausa inicial de carregamento e 'primeira leitura' da página
        self.human_delay(2.0, 4.0)

        logger.info(f"Emulando navegação humana (scroll, hover, delay) por {duration_seconds}s...")
        start_time = time.time()
        scroll_count = 0
        hover_count = 0
        click_count = 0

        while (time.time() - start_time) < duration_seconds:
            # 1. Rolagem de página
            self.smooth_scroll()
            scroll_count += 1
            self.human_delay(1.0, 2.5)

            # 2. Movimentação de cursor / Hover (40% de chance)
            if random.random() < 0.40:
                if self.simulate_hover():
                    hover_count += 1
                self.human_delay(0.5, 1.5)

            # 3. Pausa longa para leitura/análise de conteúdo (25% de chance)
            if random.random() < 0.25:
                self.human_delay(2.0, 4.5)

            # 4. Clique seguro de navegação (10% de chance se habilitado)
            if self.enable_clicks and random.random() < 0.10:
                if self.simulate_safe_click():
                    click_count += 1
                self.human_delay(1.5, 3.0)

        elapsed = round(time.time() - start_time, 2)
        logger.info(
            f"[OK] Sessão interativa concluída para {url} ({elapsed}s decorridos | "
            f"{scroll_count} scrolls, {hover_count} hovers, {click_count} clicks)."
        )

        return {
            "url": url,
            "duration_seconds": elapsed,
            "scroll_count": scroll_count,
            "hover_count": hover_count,
            "click_count": click_count,
            "completed": True
        }


def simulate_human_session(driver, url: str, duration_seconds: int = 45) -> Dict[str, Any]:
    """Função utilitária de conveniência para execução direta da sessão."""
    navigator = HumanNavigator(driver)
    return navigator.run_session(url, duration_seconds)


if __name__ == "__main__":
    import sys
    from src.collector.stealth_config import create_stealth_driver
    # Parsing flexível de argumentos CLI
    target_url = "https://example.com"
    target_duration = 20

    if len(sys.argv) > 1:
        if sys.argv[1].isdigit():
            target_duration = int(sys.argv[1])
            if len(sys.argv) > 2:
                target_url = sys.argv[2]
        else:
            target_url = sys.argv[1]
            if len(sys.argv) > 2 and sys.argv[2].isdigit():
                target_duration = int(sys.argv[2])

    print("=========================================================")
    print("👤 Teste de Lógica de Navegação Humana (Issue #10)")
    print("=========================================================")
    
    driver, ua = create_stealth_driver(headless=True)
    try:
        results = simulate_human_session(driver, target_url, duration_seconds=target_duration)
        print("=========================================================")
        print("📊 Estatísticas da Sessão:")
        for k, v in results.items():
            print(f"   └─ {k}: {v}")
        print("=========================================================")
    finally:
        driver.quit()
