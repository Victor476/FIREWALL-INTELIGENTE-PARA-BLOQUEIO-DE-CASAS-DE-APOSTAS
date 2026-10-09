#!/bin/bash
set -e

# Configura alternativas do iptables para legacy se necessario
update-alternatives --set iptables /usr/sbin/iptables-legacy 2>/dev/null || true
update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy 2>/dev/null || true

# Habilita roteamento no Kernel (caso sysctl permita ou ja esteja ativo)
sysctl -w net.ipv4.ip_forward=1 2>/dev/null || true

# Limpa regras previas do iptables
iptables -F 2>/dev/null || true
iptables -t nat -F 2>/dev/null || true

# Configura NAT (MASQUERADE) para pacotes que saem pela interface de internet (eth0)
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE 2>/dev/null || iptables-legacy -t nat -A POSTROUTING -o eth0 -j MASQUERADE 2>/dev/null || true

echo "========================================================="
echo "🛡️  Gateway Firewall ativo (IP: 172.20.0.254)"
echo "   NAT MASQUERADE e Roteamento IP habilitados no Netfilter"
echo "========================================================="

if [ "$#" -gt 0 ]; then
  exec "$@"
else
  exec tail -f /dev/null
fi
