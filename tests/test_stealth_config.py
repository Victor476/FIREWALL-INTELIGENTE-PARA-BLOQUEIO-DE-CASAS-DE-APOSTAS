import pytest
from unittest.mock import MagicMock, patch
from src.collector.stealth_config import (
    USER_AGENTS,
    VIEWPORTS,
    get_random_user_agent,
    get_platform_from_ua,
    get_stealth_options,
    create_stealth_driver
)

def test_user_agents_list_structure():
    """Garante que a lista de User-Agents é não-vazia e contém strings válidas."""
    assert len(USER_AGENTS) >= 9
    for ua in USER_AGENTS:
        assert isinstance(ua, str)
        assert "Mozilla/5.0" in ua
        assert "AppleWebKit/537.36" in ua

def test_viewports_list_structure():
    """Garante que a lista de viewports contém tuplas válidas."""
    assert len(VIEWPORTS) >= 5
    for w, h in VIEWPORTS:
        assert isinstance(w, int) and isinstance(h, int)
        assert w >= 1280 and h >= 720

def test_get_random_user_agent():
    """Garante que o User-Agent sorteado pertence ao pool."""
    for _ in range(30):
        ua = get_random_user_agent()
        assert ua in USER_AGENTS

def test_get_platform_from_ua():
    """Valida a resolução correta de plataformas para Mac, Windows e Linux."""
    assert get_platform_from_ua("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...") == "MacIntel"
    assert get_platform_from_ua("Mozilla/5.0 (Windows NT 10.0; Win64; x64)...") == "Win32"
    assert get_platform_from_ua("Mozilla/5.0 (X11; Linux x86_64)...") == "Linux x86_64"
    assert get_platform_from_ua("Generic Other UA") == "Linux x86_64"

def test_get_stealth_options_all_flags():
    """Verifica se todas as flags de evasão anti-automação são injetadas nas opções."""
    custom_ua = "Custom-UA-Test-String"
    custom_size = (1920, 1080)

    options, ua, size = get_stealth_options(user_agent=custom_ua, window_size=custom_size, headless=True)

    assert ua == custom_ua
    assert size == (1920, 1080)
    
    # Flags essenciais
    assert "--headless=new" in options.arguments
    assert "--no-sandbox" in options.arguments
    assert "--disable-dev-shm-usage" in options.arguments
    assert "--disable-gpu" in options.arguments
    assert "--disable-extensions" in options.arguments
    assert f"--window-size=1920,1080" in options.arguments
    assert f"user-agent={custom_ua}" in options.arguments
    assert "--lang=pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7" in options.arguments
    assert "--disable-blink-features=AutomationControlled" in options.arguments
    
    # Experimental options
    assert options.experimental_options.get("excludeSwitches") == ["enable-automation"]
    assert options.experimental_options.get("useAutomationExtension") is False

def test_get_stealth_options_headless_false():
    """Verifica geração com headless desativado."""
    options, ua, size = get_stealth_options(headless=False)
    assert ua in USER_AGENTS
    assert size in VIEWPORTS
    assert "--headless=new" not in options.arguments

@patch("src.collector.stealth_config.shutil.which", return_value="/usr/bin/chromedriver")
@patch("src.collector.stealth_config.HAS_SELENIUM_STEALTH", False)
@patch("src.collector.stealth_config.webdriver.Chrome")
def test_create_stealth_driver_with_service(mock_chrome_cls, mock_which):
    """Testa inicialização do driver com service configurado."""
    mock_driver = MagicMock()
    mock_chrome_cls.return_value = mock_driver

    driver, ua = create_stealth_driver(user_agent="Test-UA-Win", headless=True)

    assert driver == mock_driver
    assert ua == "Test-UA-Win"
    mock_driver.execute_cdp_cmd.assert_called_once()
    cdp_call = mock_driver.execute_cdp_cmd.call_args
    assert cdp_call[0][0] == "Page.addScriptToEvaluateOnNewDocument"
    assert "webdriver" in cdp_call[0][1]["source"]
    assert "window.chrome" in cdp_call[0][1]["source"]
    assert "Notification.permission" in cdp_call[0][1]["source"]
