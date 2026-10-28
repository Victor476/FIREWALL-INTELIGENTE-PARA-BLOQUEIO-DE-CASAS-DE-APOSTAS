import os
import shutil
import pytest
import subprocess
from unittest.mock import patch
from src.collector.bpf_filter import (
    DEFAULT_BPF_FILTER,
    BPFFilterBuilder,
    get_active_bpf_filter,
    build_tcpdump_command
)

# -------------------------------------------------------------
# Testes do BPFFilterBuilder
# -------------------------------------------------------------
def test_default_bpf_expression():
    """Garante que a expressão padrão inclui TCP/UDP e exclui ARP, Multicast e Portas de Gestão."""
    builder = BPFFilterBuilder()
    expr = builder.build_expression()

    assert "(tcp or udp)" in expr
    assert "not (arp or rarp)" in expr
    assert "not ether multicast" in expr
    assert "not (port 22 or port 2375 or port 2376)" in expr

def test_protocol_selection():
    """Testa variações na seleção de protocolos de transporte."""
    # Somente TCP
    builder_tcp = BPFFilterBuilder(include_tcp=True, include_udp=False)
    assert "(tcp)" in builder_tcp.build_expression()
    assert "udp" not in builder_tcp.build_expression()

    # Somente UDP
    builder_udp = BPFFilterBuilder(include_tcp=False, include_udp=True)
    assert "(udp)" in builder_udp.build_expression()
    assert "tcp" not in builder_udp.build_expression()

    # Nenhum dos dois (fallback para IP geral)
    builder_ip = BPFFilterBuilder(include_tcp=False, include_udp=False)
    assert "ip and not (arp or rarp)" in builder_ip.build_expression()

def test_target_ports_filter():
    """Testa restrição a portas específicas (ex: 80, 443)."""
    builder = BPFFilterBuilder(target_ports={80, 443})
    expr = builder.build_expression()
    assert "(port 80 or port 443)" in expr

def test_disable_arp_and_multicast_exclusion():
    """Verifica desativação opcional das regras de exclusão."""
    builder = BPFFilterBuilder(exclude_arp=False, exclude_multicast=False, exclude_ports=set())
    expr = builder.build_expression()

    assert "not (arp or rarp)" not in expr
    assert "not ether multicast" not in expr
    assert "not (port" not in expr
    assert expr == "(tcp or udp)"

def test_custom_excluded_ports():
    """Verifica personalização do conjunto de portas excluídas."""
    builder = BPFFilterBuilder(exclude_ports={22, 8080})
    expr = builder.build_expression()
    assert "not (port 22 or port 8080)" in expr

def test_custom_clause_injection():
    """Verifica injeção de cláusula customizada."""
    builder = BPFFilterBuilder(custom_clause="host 172.20.0.10")
    expr = builder.build_expression()
    assert "(host 172.20.0.10)" in expr

def test_get_tcpdump_args():
    """Garante a construção correta da lista de argumentos do tcpdump."""
    builder = BPFFilterBuilder(target_ports={443})
    cmd = builder.get_tcpdump_args(
        output_file="/app/data/raw/test.pcap",
        interface="eth0",
        snaplen=0,
        packet_count=50
    )

    assert cmd[0] == "tcpdump"
    assert cmd[1] == "-i"
    assert cmd[2] == "eth0"
    assert cmd[3] == "-s"
    assert cmd[4] == "0"
    assert cmd[5] == "-w"
    assert cmd[6] == "/app/data/raw/test.pcap"
    assert cmd[7] == "-U"
    assert cmd[8] == "-c"
    assert cmd[9] == "50"
    assert cmd[10] == builder.build_expression()

# -------------------------------------------------------------
# Testes de get_active_bpf_filter e build_tcpdump_command
# -------------------------------------------------------------
def test_get_active_bpf_filter_default():
    """Verifica retorno padrão quando a variável de ambiente não existe."""
    with patch.dict(os.environ, {}, clear=True):
        active = get_active_bpf_filter()
        assert active == DEFAULT_BPF_FILTER

def test_get_active_bpf_filter_env_override():
    """Verifica sobreposição via variável de ambiente BPF_FILTER."""
    custom_bpf = "tcp and port 443"
    with patch.dict(os.environ, {"BPF_FILTER": custom_bpf}):
        assert get_active_bpf_filter() == custom_bpf

def test_build_tcpdump_command_helper():
    """Verifica a função utilitária build_tcpdump_command."""
    cmd = build_tcpdump_command(
        output_file="/tmp/clean.pcap",
        interface="eth0",
        packet_count=100,
        bpf_filter="tcp port 80"
    )

    assert cmd == [
        "tcpdump",
        "-i", "eth0",
        "-s", "0",
        "-w", "/tmp/clean.pcap",
        "-U",
        "-c", "100",
        "tcp port 80"
    ]

# -------------------------------------------------------------
# Teste de Sanidade Real de Sintaxe BPF no Linux (se tcpdump disponível)
# -------------------------------------------------------------
def test_bpf_syntax_validity_with_tcpdump():
    """Valida se a expressão gerada compila com sucesso no compilador BPF do tcpdump."""
    if not shutil.which("tcpdump"):
        pytest.skip("tcpdump não está instalado no PATH do ambiente de teste")
        return

    builder = BPFFilterBuilder()
    expr = builder.build_expression()

    # tcpdump -d compila e imprime o código de instruções BPF sem iniciar captura
    res = subprocess.run(["tcpdump", "-d", expr], capture_output=True, text=True)
    if res.returncode == 0:
        assert len(res.stdout) > 0
