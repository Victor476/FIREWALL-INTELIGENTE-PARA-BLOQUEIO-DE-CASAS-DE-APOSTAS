import os
import shutil
import subprocess
from typing import List, Optional, Set

# Expressão padrão BPF para eliminar ruídos de ARP, Multicast e portas administrativas
DEFAULT_BPF_FILTER = (
    "(tcp or udp) and not (arp or rarp) and not ether multicast and not (port 22 or port 2375)"
)

DEFAULT_EXCLUDED_PORTS = {22, 2375, 2376}

class BPFFilterBuilder:
    """
    Construtor e validador de expressões Berkeley Packet Filter (BPF) para tcpdump e Scapy (Issue #11).
    Permite customização modular de protocolos, exclusão de portas de ruído e foco em tráfego Web (HTTP/HTTPS/QUIC).
    """

    def __init__(
        self,
        include_tcp: bool = True,
        include_udp: bool = True,
        exclude_arp: bool = True,
        exclude_multicast: bool = True,
        exclude_ports: Optional[Set[int]] = None,
        target_ports: Optional[Set[int]] = None,
        custom_clause: Optional[str] = None
    ):
        self.include_tcp = include_tcp
        self.include_udp = include_udp
        self.exclude_arp = exclude_arp
        self.exclude_multicast = exclude_multicast
        self.exclude_ports = set(exclude_ports) if exclude_ports is not None else set(DEFAULT_EXCLUDED_PORTS)
        self.target_ports = set(target_ports) if target_ports is not None else set()
        self.custom_clause = custom_clause

    def build_expression(self) -> str:
        """Monta a string final da regra BPF parametrizada."""
        clauses = []

        # 1. Protocolos de Transporte
        proto_clauses = []
        if self.include_tcp:
            proto_clauses.append("tcp")
        if self.include_udp:
            proto_clauses.append("udp")

        if proto_clauses:
            clauses.append(f"({' or '.join(proto_clauses)})")
        else:
            clauses.append("ip")

        # 2. Portas Alvo (se especificadas)
        if self.target_ports:
            sorted_ports = sorted(self.target_ports)
            port_or = " or ".join(f"port {p}" for p in sorted_ports)
            clauses.append(f"({port_or})")

        # 3. Exclusão de ARP / RARP
        if self.exclude_arp:
            clauses.append("not (arp or rarp)")

        # 4. Exclusão de Multicast
        if self.exclude_multicast:
            clauses.append("not ether multicast")

        # 5. Exclusão de Portas de Gestão/Ruído
        if self.exclude_ports:
            sorted_excluded = sorted(self.exclude_ports)
            ports_expr = " or ".join(f"port {p}" for p in sorted_excluded)
            clauses.append(f"not ({ports_expr})")

        # 6. Cláusula personalizada adicional
        if self.custom_clause:
            clauses.append(f"({self.custom_clause})")

        return " and ".join(clauses)

    def get_tcpdump_args(
        self,
        output_file: str,
        interface: str = "eth0",
        snaplen: int = 0,
        packet_count: Optional[int] = None
    ) -> List[str]:
        """
        Gera a lista de argumentos para execução do binário tcpdump.
        Utiliza -s 0 (snaplen ilimitado) para preservar integridade total dos pacotes.
        """
        cmd = [
            "tcpdump",
            "-i", interface,
            "-s", str(snaplen),
            "-w", output_file,
            "-U"  # Gravação de pacotes em tempo real (unbuffered)
        ]

        if packet_count is not None and packet_count > 0:
            cmd.extend(["-c", str(packet_count)])

        filter_expr = self.build_expression()
        cmd.append(filter_expr)
        return cmd


def get_active_bpf_filter() -> str:
    """
    Retorna a expressão BPF ativa configurada via variável de ambiente 'BPF_FILTER'
    ou o padrão consolidado.
    """
    return os.environ.get("BPF_FILTER", DEFAULT_BPF_FILTER).strip()


def build_tcpdump_command(
    output_file: str,
    interface: str = "eth0",
    packet_count: Optional[int] = None,
    bpf_filter: Optional[str] = None
) -> List[str]:
    """Função utilitária rápida para gerar o comando tcpdump com BPF configurado."""
    active_filter = bpf_filter or get_active_bpf_filter()
    builder = BPFFilterBuilder()
    
    cmd = [
        "tcpdump",
        "-i", interface,
        "-s", "0",
        "-w", output_file,
        "-U"
    ]
    if packet_count is not None and packet_count > 0:
        cmd.extend(["-c", str(packet_count)])
        
    cmd.append(active_filter)
    return cmd


if __name__ == "__main__":
    builder = BPFFilterBuilder()
    expr = builder.build_expression()
    sample_cmd = builder.get_tcpdump_args(output_file="/data/raw/capture.pcap")
    
    print("=========================================================")
    print("🛡️  Configuração do Filtro BPF (Issue #11)")
    print("=========================================================")
    print(f"🔍 Expressão BPF Ativa:")
    print(f"   └─ {expr}")
    print("\n📦 Exemplo de Comando tcpdump:")
    print(f"   └─ {' '.join(sample_cmd)}")
    print("=========================================================")
