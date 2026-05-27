#!/bin/bash
# ─── Dork Hunter - Termux Kurulum Scripti ────────────────────────────────────

R="\033[91m"
G="\033[92m"
Y="\033[93m"
C="\033[96m"
W="\033[97m"
RST="\033[0m"

echo -e "\n${C}╔══════════════════════════════════════════╗${RST}"
echo -e "${C}║${RST}   ${W}Dork Hunter - Termux Kurulum Scripti${RST}   ${C}║${RST}"
echo -e "${C}╚══════════════════════════════════════════╝${RST}\n"

echo -e "${Y}[1/4]${RST} ${W}Paket listesi güncelleniyor...${RST}"
pkg update -y 2>/dev/null && pkg upgrade -y 2>/dev/null

echo -e "${Y}[2/4]${RST} ${W}Python yükleniyor...${RST}"
pkg install python -y 2>/dev/null

echo -e "${Y}[3/4]${RST} ${W}pip güncelleniyor...${RST}"
pip install --upgrade pip 2>/dev/null

echo -e "${Y}[4/4]${RST} ${W}Python bağımlılıkları yükleniyor...${RST}"
pip install requests beautifulsoup4 2>/dev/null

echo -e "\n${G}[✔] Kurulum tamamlandı!${RST}"
echo -e "${C}[i]${RST} ${W}Aracı başlatmak için:${RST}"
echo -e "    ${G}python dork_tool.py${RST}\n"
