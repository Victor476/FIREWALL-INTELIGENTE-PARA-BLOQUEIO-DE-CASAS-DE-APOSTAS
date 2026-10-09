import pytest
from unittest.mock import MagicMock, patch, call
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException
from src.collector.human_behavior import HumanNavigator, simulate_human_session

@pytest.fixture
def mock_driver():
    driver = MagicMock()
    return driver

# -------------------------------------------------------------
# Testes de human_delay
# -------------------------------------------------------------
def test_human_delay_gaussian_formula(mock_driver):
    """Verifica se a média e desvio padrão gaussianos são calculados estritamente conforme fórmula."""
    navigator = HumanNavigator(mock_driver)
    
    with patch("time.sleep") as mock_sleep, patch("random.gauss", return_value=2.0) as mock_gauss:
        delay = navigator.human_delay(min_sec=1.0, max_sec=3.0, gaussian=True)
        # mean = (1.0 + 3.0) / 2.0 = 2.0; std_dev = (3.0 - 1.0) / 6.0 = 2.0 / 6.0
        expected_mean = (1.0 + 3.0) / 2.0
        expected_std = (3.0 - 1.0) / 6.0
        mock_gauss.assert_called_once_with(expected_mean, expected_std)
        assert delay == 2.0
        mock_sleep.assert_called_once_with(2.0)

def test_human_delay_clamping(mock_driver):
    """Garante que valores fora dos limites são devidamente limitados (clamped)."""
    navigator = HumanNavigator(mock_driver)
    
    with patch("time.sleep"):
        # Teste limite inferior
        with patch("random.gauss", return_value=0.2):
            delay_low = navigator.human_delay(min_sec=1.0, max_sec=3.0, gaussian=True)
            assert delay_low == 1.0

        # Teste limite superior
        with patch("random.gauss", return_value=9.9):
            delay_high = navigator.human_delay(min_sec=1.0, max_sec=3.0, gaussian=True)
            assert delay_high == 3.0

def test_human_delay_uniform(mock_driver):
    """Garante a chamada correta para distribuição uniforme."""
    navigator = HumanNavigator(mock_driver)
    with patch("time.sleep") as mock_sleep, patch("random.uniform", return_value=2.5) as mock_uniform:
        delay = navigator.human_delay(min_sec=2.0, max_sec=4.0, gaussian=False)
        mock_uniform.assert_called_once_with(2.0, 4.0)
        assert delay == 2.5
        mock_sleep.assert_called_once_with(2.5)

# -------------------------------------------------------------
# Testes de smooth_scroll
# -------------------------------------------------------------
def test_smooth_scroll_downward(mock_driver):
    """Testa rolagem para baixo padrão (85% das vezes)."""
    navigator = HumanNavigator(mock_driver)
    with patch("random.random", return_value=0.5), \
         patch("random.randint", return_value=350) as mock_randint:
        
        step = navigator.smooth_scroll(min_step=200, max_step=500)
        mock_randint.assert_called_once_with(200, 500)
        assert step == 350
        mock_driver.execute_script.assert_called_once_with("window.scrollBy({top: 350, behavior: 'smooth'});")

def test_smooth_scroll_upward(mock_driver):
    """Testa rolagem para cima / releitura (15% das vezes)."""
    navigator = HumanNavigator(mock_driver)
    with patch("random.random", return_value=0.05), \
         patch("random.randint", return_value=180) as mock_randint:
        
        step = navigator.smooth_scroll(min_step=200, max_step=500)
        mock_randint.assert_called_once_with(100, 300)
        assert step == -180
        mock_driver.execute_script.assert_called_once_with("window.scrollBy({top: -180, behavior: 'smooth'});")

def test_smooth_scroll_handles_exception(mock_driver):
    """Garante que exceções de WebDriver no scroll não quebram o fluxo."""
    mock_driver.execute_script.side_effect = WebDriverException("Script error")
    navigator = HumanNavigator(mock_driver)
    step = navigator.smooth_scroll()
    assert step == 0

# -------------------------------------------------------------
# Testes de simulate_hover
# -------------------------------------------------------------
def test_simulate_hover_success(mock_driver):
    """Testa a movimentação de cursor para elemento visível."""
    mock_element = MagicMock(spec=WebElement)
    mock_element.is_displayed.return_value = True
    mock_driver.find_elements.return_value = [mock_element]

    navigator = HumanNavigator(mock_driver)
    with patch("src.collector.human_behavior.ActionChains") as mock_action_chains:
        mock_actions = MagicMock()
        mock_action_chains.return_value = mock_actions
        mock_actions.move_to_element.return_value = mock_actions
        
        result = navigator.simulate_hover()
        assert result is True
        mock_actions.move_to_element.assert_called_once_with(mock_element)
        mock_actions.perform.assert_called_once()

def test_simulate_hover_element_not_displayed(mock_driver):
    """Testa quando o elemento candidato não está visível."""
    mock_element = MagicMock(spec=WebElement)
    mock_element.is_displayed.return_value = False
    mock_driver.find_elements.return_value = [mock_element]

    navigator = HumanNavigator(mock_driver)
    assert navigator.simulate_hover() is False

def test_simulate_hover_empty_elements(mock_driver):
    """Testa retorno False quando nenhum elemento é encontrado."""
    mock_driver.find_elements.return_value = []
    navigator = HumanNavigator(mock_driver)
    assert navigator.simulate_hover() is False

def test_simulate_hover_exception(mock_driver):
    """Garante captura de exceção durante hover."""
    mock_driver.find_elements.side_effect = WebDriverException("DOM detached")
    navigator = HumanNavigator(mock_driver)
    assert navigator.simulate_hover() is False

# -------------------------------------------------------------
# Testes de simulate_safe_click
# -------------------------------------------------------------
@pytest.mark.parametrize("risky_keyword", [
    "submit", "login", "cadastr", "entrar", "deposit", "pagar", "buy", "cart"
])
def test_simulate_safe_click_filters_all_risky_words(mock_driver, risky_keyword):
    """Garante que TODAS as palavras-chave arriscadas são bloqueadas por texto ou id."""
    risky_by_text = MagicMock(spec=WebElement)
    risky_by_text.is_displayed.return_value = True
    risky_by_text.text = f"Clique para {risky_keyword}"
    risky_by_text.get_attribute.return_value = "safe-id"

    risky_by_id = MagicMock(spec=WebElement)
    risky_by_id.is_displayed.return_value = True
    risky_by_id.text = "Texto Neutro"
    risky_by_id.get_attribute.return_value = f"btn-{risky_keyword}-now"

    safe_element = MagicMock(spec=WebElement)
    safe_element.is_displayed.return_value = True
    safe_element.text = "Ver Estatísticas"
    safe_element.get_attribute.return_value = "stats-tab"

    mock_driver.find_elements.return_value = [risky_by_text, risky_by_id, safe_element]

    navigator = HumanNavigator(mock_driver, enable_clicks=True)
    result = navigator.simulate_safe_click()
    
    assert result is True
    safe_element.click.assert_called_once()
    risky_by_text.click.assert_not_called()
    risky_by_id.click.assert_not_called()

def test_simulate_safe_click_disabled(mock_driver):
    """Verifica comportamento quando cliques estão desabilitados."""
    navigator = HumanNavigator(mock_driver, enable_clicks=False)
    assert navigator.simulate_safe_click() is False

def test_simulate_safe_click_no_safe_elements(mock_driver):
    """Verifica quando apenas elementos arriscados ou não exibidos estão presentes."""
    risky = MagicMock(spec=WebElement)
    risky.is_displayed.return_value = True
    risky.text = "Login"
    risky.get_attribute.return_value = "login-id"
    mock_driver.find_elements.return_value = [risky]

    navigator = HumanNavigator(mock_driver, enable_clicks=True)
    assert navigator.simulate_safe_click() is False

def test_simulate_safe_click_exception_on_click(mock_driver):
    """Garante que erro durante o click não quebra o script."""
    safe_element = MagicMock(spec=WebElement)
    safe_element.is_displayed.return_value = True
    safe_element.text = "Menu"
    safe_element.get_attribute.return_value = "menu-id"
    safe_element.click.side_effect = WebDriverException("Click intercepted")

    mock_driver.find_elements.return_value = [safe_element]

    navigator = HumanNavigator(mock_driver, enable_clicks=True)
    assert navigator.simulate_safe_click() is False

# -------------------------------------------------------------
# Testes de run_session
# -------------------------------------------------------------
def test_run_session_full_lifecycle(mock_driver):
    """Valida a execução de uma sessão completa com todos os gatilhos ativados."""
    navigator = HumanNavigator(mock_driver, enable_clicks=True)
    
    current_time = [100.0]
    def fake_time():
        current_time[0] += 1.0
        return current_time[0]

    with patch.object(navigator, "human_delay") as mock_delay, \
         patch.object(navigator, "smooth_scroll", return_value=300) as mock_scroll, \
         patch.object(navigator, "simulate_hover", return_value=True) as mock_hover, \
         patch.object(navigator, "simulate_safe_click", return_value=True) as mock_click, \
         patch("random.random", side_effect=[0.1, 0.1, 0.05, 0.9, 0.9, 0.9]), \
         patch("time.time", side_effect=fake_time):
        
        result = navigator.run_session(url="https://bet365.com", duration_seconds=2)
        
        assert result["url"] == "https://bet365.com"
        assert result["completed"] is True
        assert result["scroll_count"] >= 1
        assert result["hover_count"] >= 1
        assert result["click_count"] >= 1
        assert "duration_seconds" in result
        mock_driver.get.assert_called_once_with("https://bet365.com")

def test_simulate_human_session_convenience(mock_driver):
    """Testa a função de conveniência simulate_human_session."""
    with patch("src.collector.human_behavior.HumanNavigator.run_session") as mock_run:
        mock_run.return_value = {"completed": True, "url": "https://example.com"}
        res = simulate_human_session(mock_driver, "https://example.com", duration_seconds=10)
        assert res["completed"] is True
        mock_run.assert_called_once_with("https://example.com", 10)
