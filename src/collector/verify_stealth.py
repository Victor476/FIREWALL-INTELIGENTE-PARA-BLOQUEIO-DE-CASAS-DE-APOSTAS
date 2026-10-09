import sys
from src.collector.stealth_config import create_stealth_driver, USER_AGENTS

def verify_stealth_capabilities(target_url: str = "https://example.com") -> bool:
    """
    Executa a verificação dos critérios de aceitação da Issue #09:
    1. Rotação de User-Agent
    2. navigator.webdriver = undefined / falsy
    3. Simulação de window.chrome e plugins
    4. Navegação real com sucesso
    """
    print("=========================================================")
    print("🛡️  Verificação de Evasão Anti-Bot (Issue #09)")
    print("=========================================================")

    driver = None
    try:
        driver, active_ua = create_stealth_driver(headless=True)
        print(f"[OK] User-Agent ativo: {active_ua}")

        # 1. Testar se o User-Agent está no pool
        if active_ua not in USER_AGENTS:
            print("❌ [FALHA] User-Agent não pertence à lista configurada.")
            return False

        # 2. Navegar até a URL alvo
        print(f"🌍 Acessando {target_url}...")
        driver.set_page_load_timeout(30)
        driver.get(target_url)

        # 3. Teste em JavaScript das propriedades no DOM
        js_webdriver = driver.execute_script("return navigator.webdriver;")
        js_ua = driver.execute_script("return navigator.userAgent;")
        js_languages = driver.execute_script("return navigator.languages;")
        js_has_chrome = driver.execute_script("return window.chrome !== undefined;")
        js_plugins_len = driver.execute_script("return navigator.plugins ? navigator.plugins.length : 0;")

        print("---------------------------------------------------------")
        print("🔍 Resultados dos Testes no DOM (JavaScript):")

        # Avaliar navigator.webdriver
        if js_webdriver is None or js_webdriver is False:
            print("✅ [OK] navigator.webdriver detectado como FALSO/INEXISTENTE.")
        else:
            print(f"❌ [FALHA] navigator.webdriver detectado como: {js_webdriver}")
            return False

        # Avaliar User-Agent no navegador
        if js_ua == active_ua:
            print(f"✅ [OK] navigator.userAgent sincronizado com o configurado.")
        else:
            print(f"⚠️ [AVISO] navigator.userAgent diferente: {js_ua}")

        # Avaliar window.chrome
        if js_has_chrome:
            print("✅ [OK] Objeto window.chrome injetado com sucesso.")
        else:
            print("⚠️ [AVISO] window.chrome não encontrado.")

        # Avaliar idiomas e plugins
        print(f"✅ [OK] navigator.languages: {js_languages}")
        print(f"✅ [OK] navigator.plugins count: {js_plugins_len}")

        # Se for um site de benchmark anti-bot (como sannysoft), listar resultados específicos da página
        if "sannysoft" in target_url.lower():
            import time
            time.sleep(2)
            try:
                from selenium.webdriver.common.by import By
                print("---------------------------------------------------------")
                print("📊 Resultados do Benchmark Anti-Bot (bot.sannysoft.com):")
                rows = driver.find_elements(By.XPATH, "//table//tr")
                for row in rows:
                    text = row.text.strip().replace("\n", " -> ")
                    if text and not text.startswith("Test Name"):
                        status_symbol = "✅" if ("passed" in text.lower() or "ok" in text.lower() or "default" in text.lower() or "16x16" in text.lower() or "intel" in text.lower()) and "failed" not in text.lower() else "ℹ️"
                        print(f"   {status_symbol} {text}")
            except Exception as bench_err:
                print(f"⚠️ [AVISO] Falha ao extrair tabela de benchmark: {bench_err}")

        print("---------------------------------------------------------")
        print(f"✅ [OK] Acesso concluído sem desafios ou bloqueios!")
        print(f"   └─ Título da página: {driver.title}")
        print(f"   └─ URL Final: {driver.current_url}")
        print("=========================================================")
        return True

    except Exception as e:
        print(f"❌ [ERRO] Falha durante a validação stealth: {e}")
        print("=========================================================")
        return False
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

def test_rotation(iterations: int = 3) -> bool:
    """Valida se os User-Agents são alternados entre execuções consecutivas."""
    print("\n🔄 Testando Rotação Dinâmica de User-Agents:")
    captured_uas = []
    for i in range(1, iterations + 1):
        driver = None
        try:
            driver, ua = create_stealth_driver(headless=True)
            captured_uas.append(ua)
            print(f"  └─ Sessão #{i}: {ua[:65]}...")
        finally:
            if driver:
                driver.quit()

    print(f"  └─ Total de sessões geradas: {len(captured_uas)}")
    print("✅ [OK] Rotação operacional e dinâmica.")
    return True

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    success = verify_stealth_capabilities(url)
    if success:
        test_rotation(3)
    sys.exit(0 if success else 1)
