#!/bin/bash

# install.sh - Cai dat BizMaC N8N Manager

# --- Dinh nghia mau sac va bien ---
RED='\e[1;31m'
GREEN='\e[1;32m'
YELLOW='\e[1;33m'
CYAN='\e[1;36m'
NC='\e[0m'

BRAND_NAME="BizMaC"
REPOSITORY_RAW_URL="https://raw.githubusercontent.com/davidthuong/n8n-panel/main"
SCRIPT_NAME="bizmac-n8n"
LEGACY_SCRIPT_NAME="n8n-host"
SCRIPT_URL="${REPOSITORY_RAW_URL}/n8n-host.sh"
TEMPLATE_FILE_NAME="import-workflow-credentials.json"
TEMPLATE_URL="${REPOSITORY_RAW_URL}/templates/${TEMPLATE_FILE_NAME}"

# Khuyen nghi dung /usr/local/bin cho script tuy chinh
INSTALL_DIR="/usr/local/bin"
INSTALL_PATH="${INSTALL_DIR}/${SCRIPT_NAME}"
LEGACY_INSTALL_PATH="${INSTALL_DIR}/${LEGACY_SCRIPT_NAME}"
TEMP_SCRIPT="/tmp/${SCRIPT_NAME}.sh.$$"

# --- Ham kiem tra quyen root ---
check_root() {
  if [[ $EUID -ne 0 ]]; then
    echo -e "\n${RED}[!] Loi: Ban can chay script cai dat nay voi quyen root (sudo).${NC}\n"
    exit 1
  fi
}

# --- Ham kiem tra lenh (curl hoac wget) ---
check_downloader() {
    if command -v curl &> /dev/null; then
        DOWNLOADER="curl"
    elif command -v wget &> /dev/null; then
        DOWNLOADER="wget"
    else
        echo -e "${RED}[!] Loi: Khong tim thay 'curl' hoac 'wget'. Vui long cai dat mot trong hai cong cu nay.${NC}"
        exit 1
    fi
    echo -e "${GREEN}[*] Su dung '$DOWNLOADER' de tai file.${NC}"
}

# --- Ham tai script ---
download_script() {
    echo -e "${YELLOW}[*] Dang tai script tu: ${SCRIPT_URL}${NC}"
    if [[ "$DOWNLOADER" == "curl" ]]; then
        # Tai file bang curl, theo doi redirect (-L), bao loi neu fail (-f), im lang (-s), output vao file tam (-o)
        curl -fsSL -o "$TEMP_SCRIPT" "$SCRIPT_URL"
        local download_status=$?
    else # wget
        # Tai file bang wget, output vao file tam (-O), im lang (-q)
        wget -qO "$TEMP_SCRIPT" "$SCRIPT_URL"
        local download_status=$?
    fi

    if [[ $download_status -ne 0 ]]; then
        echo -e "${RED}[!] Loi: Tai script that bai (kiem tra URL hoac ket noi mang).${NC}"
        rm -f "$TEMP_SCRIPT" # Xoa file tam neu co loi
        exit 1
    fi

    # Kiem tra xem file tai ve co noi dung khong
    if [[ ! -s "$TEMP_SCRIPT" ]]; then
        echo -e "${RED}[!] Loi: File tai ve rong (kiem tra URL).${NC}"
        rm -f "$TEMP_SCRIPT"
        exit 1
    fi

    echo -e "${GREEN}[+] Tai script thanh cong.${NC}"
}

# --- Ham cai dat ---
install_script() {
    echo -e "${YELLOW}[*] Cong cu ${BRAND_NAME} N8N Manager - bat dau cai dat...${NC}"

    # 1. Kiem tra quyen root
    check_root

    # 2. Kiem tra cong cu tai file
    check_downloader

    # 3. Tai script ve file tam
    download_script

    # 4. Tao thu muc cai dat neu chua co
    if [[ ! -d "$INSTALL_DIR" ]]; then
        echo -e "${YELLOW}[*] Tao thu muc cai dat: ${INSTALL_DIR}${NC}"
        # Su dung sudo vi tao thu muc trong he thong
        if ! sudo mkdir -p "$INSTALL_DIR"; then
            echo -e "${RED}[!] Loi: Khong the tao thu muc ${INSTALL_DIR}.${NC}"
            rm -f "$TEMP_SCRIPT"
            exit 1
        fi
    fi

    # 5. Di chuyen script vao thu muc cai dat
    echo -e "${YELLOW}[*] Di chuyen script den: ${INSTALL_PATH}${NC}"
    if ! sudo mv "$TEMP_SCRIPT" "$INSTALL_PATH"; then
        echo -e "${RED}[!] Loi: Khong the di chuyen script den ${INSTALL_PATH}.${NC}"
        rm -f "$TEMP_SCRIPT" # Van co gang xoa file tam
        exit 1
    fi

    # 6. Cap quyen thuc thi cho script
    echo -e "${YELLOW}[*] Cap quyen thuc thi cho script...${NC}"
    if ! sudo chmod +x "$INSTALL_PATH"; then
        echo -e "${RED}[!] Loi: Khong the cap quyen thuc thi cho ${INSTALL_PATH}.${NC}"
        exit 1
    fi

    # 7. Giu alias n8n-host de tuong thich voi ban cai dat cu
    echo -e "${YELLOW}[*] Tao alias tuong thich: ${LEGACY_INSTALL_PATH}${NC}"
    if ! sudo ln -sfn "$INSTALL_PATH" "$LEGACY_INSTALL_PATH"; then
        echo -e "${RED}[!] Loi: Khong the tao alias ${LEGACY_INSTALL_PATH}.${NC}"
        exit 1
    fi

    # 8. Tao thu muc n8n-templates ngang hang voi root va tai ve file template
    echo -e "${YELLOW}[*] Tao thu muc n8n-templates...${NC}"
    if [[ ! -d "/n8n-templates" ]]; then
        sudo mkdir -p "/n8n-templates"
        if [[ $? -ne 0 ]]; then
            echo -e "${RED}[!] Loi: Khong the tao thu muc /n8n-templates.${NC}"
            exit 1
        fi
    fi
    echo -e "${YELLOW}[*] Tai ve file template...${NC}"

    curl -fsSL -o "/n8n-templates/${TEMPLATE_FILE_NAME}" "${TEMPLATE_URL}"
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}[!] Loi: Khong the tai ve file template.${NC}"
        exit 1
    fi
    
    # 9. Kiem tra lai
    if [[ -f "$INSTALL_PATH" && -x "$INSTALL_PATH" && -L "$LEGACY_INSTALL_PATH" ]]; then
        echo -e "\n${GREEN}[+++] Cai dat thanh cong! ${NC}"
        echo -e "Lenh chinh: ${CYAN}${SCRIPT_NAME}${NC}"
        echo -e "Alias tuong thich: ${CYAN}${LEGACY_SCRIPT_NAME}${NC}"
        echo -e "De go bo, chay lenh: ${CYAN}${SCRIPT_NAME} --uninstall${NC}"
    else
        echo -e "\n${RED}[!] Cai dat that bai. Khong tim thay file thuc thi tai ${INSTALL_PATH}.${NC}"
        exit 1
    fi
}

# Kiem tra xem script da duoc cai dat chua
if [[ -f "$INSTALL_PATH" ]]; then
    echo -e "${YELLOW}[!] Cong cu '${SCRIPT_NAME}' duong nhu da duoc cai dat tai '${INSTALL_PATH}'.${NC}"
    echo -e "Neu ban muon cai dat lai, hay chay: ${CYAN}bash $0 --uninstall${NC}"
    echo -e "Sau do chay lai lenh hien tai."
    exit 1
else
    # Neu chua cai dat, tien hanh cai dat
    install_script
fi

exit 0
