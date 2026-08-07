#!/bin/bash
set -e

# Garante que a rota padrao de saida seja o IP do Gateway (172.20.0.254)
ip route replace default via 172.20.0.254 dev eth0 2>/dev/null || true

echo "========================================================="
echo "💻 App Client conectado ao Gateway (172.20.0.254)"
echo "   Todas as requisicoes passarao pelo firewall"
echo "========================================================="

if [ "$#" -gt 0 ]; then
  exec "$@"
else
  exec tail -f /dev/null
fi
