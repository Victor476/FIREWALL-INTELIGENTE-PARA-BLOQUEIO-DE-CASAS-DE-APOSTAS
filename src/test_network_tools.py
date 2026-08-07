import os
from scapy.all import sniff, IP, conf

conf.iface = 'eth0'

def packet_callback(pkt):
    if pkt.haslayer(IP):
        print(f"  └─ 📡 [Scapy] Pacote Capturado: {pkt[IP].src} -> {pkt[IP].dst}")

def test_tools():
    print("=========================================================")
    print("🔍 Teste de Sanidade das Ferramentas de Rede (Issue #06)")
    print("=========================================================")
    
    # 1. Testar tshark
    exit_tshark = os.system("tshark -v > /dev/null 2>&1")
    if exit_tshark == 0:
        print("✅ [OK] Tshark instalado e operacional.")
    else:
        print("❌ [ERRO] Tshark nao encontrado.")

    # 2. Testar tcpdump
    exit_tcpdump = os.system("tcpdump --version > /dev/null 2>&1")
    if exit_tcpdump == 0:
        print("✅ [OK] Tcpdump instalado e operacional.")
    else:
        print("❌ [ERRO] Tcpdump nao encontrado.")

    # 3. Testar Scapy (captura passiva)
    print("📡 Executando escuta com Scapy na interface eth0...")
    packets = sniff(iface="eth0", count=1, prn=packet_callback, timeout=4)
    if len(packets) > 0:
        print(f"✅ [OK] Scapy interceptou {len(packets)} pacote(s) em tempo real!")
    else:
        print("ℹ️ [INFO] Scapy pronto (nenhum pacote recebido no timeout).")
    print("=========================================================")

if __name__ == "__main__":
    test_tools()

