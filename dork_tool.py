#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import requests
import re
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup

# ─── ANSI Renk Kodları ───────────────────────────────────────────────────────
R  = "\033[91m"   # Kırmızı
G  = "\033[92m"   # Yeşil
Y  = "\033[93m"   # Sarı
B  = "\033[94m"   # Mavi
M  = "\033[95m"   # Mor
C  = "\033[96m"   # Cyan
W  = "\033[97m"   # Beyaz
DG = "\033[90m"   # Koyu Gri
BLD= "\033[1m"    # Kalın
RST= "\033[0m"    # Sıfırla
BG_R = "\033[41m" # Kırmızı arka plan
BG_B = "\033[44m" # Mavi arka plan

def cls():
    os.system("clear" if os.name == "posix" else "cls")

# ─── DORK KATEGORİLERİ (100+) ────────────────────────────────────────────────
DORKS = {
    # ══════════════════════════════════════
    #  1-10 | SQL ENJEKSİYONU
    # ══════════════════════════════════════
    1:  {
        "name": "SQL Açıklı Site Bul",
        "file": "sql_acikli_siteler",
        "queries": [
            'inurl:"index.php?id="',
            'inurl:"product.php?id="',
            'inurl:"news.php?id="',
            'inurl:"page.php?id="',
            'inurl:"category.php?id="',
        ]
    },
    2:  {
        "name": "Veritabanı Hatası Olan Siteler",
        "file": "veritabani_hatali_siteler",
        "queries": [
            'intext:"mysql_fetch_array()"',
            'intext:"You have an error in your SQL syntax"',
            'intext:"Warning: mysql_" site:.com',
            'intext:"ORA-00933: SQL command not properly ended"',
            'intext:"Microsoft OLE DB Provider for ODBC Drivers"',
        ]
    },
    3:  {
        "name": "MySQL Hata Sayfaları",
        "file": "mysql_hatali_siteler",
        "queries": [
            'intext:"mysql_num_rows()" intext:"Warning"',
            'intext:"supplied argument is not a valid MySQL"',
            'intext:"Column count doesn\'t match"',
            'intext:"mysql_connect(): Access denied"',
            'intext:"mysql_query() expects parameter"',
        ]
    },
    4:  {
        "name": "MSSQL Açıklı Siteler",
        "file": "mssql_acikli_siteler",
        "queries": [
            'intext:"[Microsoft][ODBC SQL Server Driver]"',
            'intext:"Unclosed quotation mark"',
            'intext:"Microsoft SQL Native Client error"',
            'intext:"SqlException" intext:"Server Error"',
            'intext:"syntax error" intext:"mssql"',
        ]
    },
    5:  {
        "name": "PostgreSQL Açıkları",
        "file": "postgresql_acikli_siteler",
        "queries": [
            'intext:"PostgreSQL query failed"',
            'intext:"pg_query() expects parameter"',
            'intext:"ERROR: syntax error at or near"',
            'intext:"pg_exec() expects parameter"',
            'intext:"PostgreSQL ERROR"',
        ]
    },
    6:  {
        "name": "Oracle DB Açıkları",
        "file": "oracle_acikli_siteler",
        "queries": [
            'intext:"ORA-01756"',
            'intext:"ORA-00907: missing right parenthesis"',
            'intext:"ORA-00936: missing expression"',
            'intext:"Oracle Database Error"',
            'intext:"ORA-01789"',
        ]
    },
    7:  {
        "name": "SQLite Açıkları",
        "file": "sqlite_acikli_siteler",
        "queries": [
            'intext:"SQLite3::SQLException"',
            'intext:"SQLite error"',
            'intext:"sqlite3.OperationalError"',
            'intext:"SQLiteException"',
            'intext:"sqlite3" intext:"syntax error"',
        ]
    },
    8:  {
        "name": "PHP SQL Inject (GET Parametreli)",
        "file": "php_sql_inject_get",
        "queries": [
            'inurl:"?id=" inurl:".php"',
            'inurl:"?cat=" inurl:".php"',
            'inurl:"?pid=" inurl:".php"',
            'inurl:"?item=" inurl:".php"',
            'inurl:"?aid=" inurl:".php"',
        ]
    },
    9:  {
        "name": "ASP SQL Inject Sayfaları",
        "file": "asp_sql_inject",
        "queries": [
            'inurl:"?id=" inurl:".asp"',
            'inurl:"default.asp?id="',
            'inurl:"view.asp?id="',
            'inurl:"article.asp?id="',
            'inurl:"item.asp?id="',
        ]
    },
    10: {
        "name": "SQL Inject (Geniş Tarama)",
        "file": "sql_inject_genel",
        "queries": [
            'inurl:".php?id=" intext:"database"',
            'inurl:"?id=" inurl:"select" -site:youtube.com',
            'inurl:"?id=1" intitle:"index of"',
            'inurl:"shop" inurl:"?id=" inurl:".php"',
            'inurl:"?id=" inurl:".php" intext:"error"',
        ]
    },

    # ══════════════════════════════════════
    #  11-20 | ADMİN PANELLERİ
    # ══════════════════════════════════════
    11: {
        "name": "Admin Giriş Paneli Bul",
        "file": "admin_panel_siteler",
        "queries": [
            'intitle:"Admin Login" inurl:"admin"',
            'intitle:"Administrator Login" inurl:"admin"',
            'inurl:"/admin/login" intext:"username"',
            'inurl:"/admin/index.php" intitle:"login"',
            'inurl:"/administrator/index.php" intitle:"login"',
        ]
    },
    12: {
        "name": "phpMyAdmin Panelleri",
        "file": "phpmyadmin_siteler",
        "queries": [
            'intitle:"phpMyAdmin" inurl:"phpmyadmin"',
            'inurl:"/phpmyadmin/index.php"',
            'intitle:"phpMyAdmin" "Welcome to phpMyAdmin"',
            'inurl:"pma/index.php" intitle:"phpMyAdmin"',
            'inurl:"/phpMyAdmin/" intitle:"phpMyAdmin"',
        ]
    },
    13: {
        "name": "WordPress Admin Paneli",
        "file": "wordpress_admin_siteler",
        "queries": [
            'inurl:"wp-admin/admin-ajax.php"',
            'inurl:"wp-login.php" intitle:"WordPress"',
            'inurl:"wp-admin" intitle:"WordPress"',
            'inurl:"/wp-admin/options.php"',
            'site:*.com inurl:wp-login.php',
        ]
    },
    14: {
        "name": "Joomla Admin Panelleri",
        "file": "joomla_admin_siteler",
        "queries": [
            'inurl:"/administrator/" intitle:"Joomla"',
            'inurl:"/administrator/index.php" intitle:"Joomla"',
            'inurl:"/administrator/" intext:"Joomla"',
            'intitle:"Joomla! Administration Login"',
            'inurl:"administrator" intitle:"Joomla! - Administration"',
        ]
    },
    15: {
        "name": "Drupal Admin Panelleri",
        "file": "drupal_admin_siteler",
        "queries": [
            'inurl:"/user/login" intitle:"Log in | Drupal"',
            'intext:"Drupal" inurl:"/user/login"',
            'intitle:"Log in" inurl:"drupal"',
            'intext:"X-Generator: Drupal"',
            'inurl:"/admin" intext:"Drupal"',
        ]
    },
    16: {
        "name": "cPanel Panelleri",
        "file": "cpanel_siteler",
        "queries": [
            'inurl:":2082" intitle:"cPanel"',
            'inurl:":2083" intitle:"cPanel"',
            'inurl:":2086" intitle:"WHM"',
            'inurl:":2087" intitle:"WHM"',
            'intitle:"cPanel Login" inurl:"cpanel"',
        ]
    },
    17: {
        "name": "Plesk Panel Siteler",
        "file": "plesk_panel_siteler",
        "queries": [
            'intitle:"Plesk" inurl:":8443"',
            'inurl:":8443" intitle:"Plesk Parallels"',
            'intitle:"Parallels Plesk Panel"',
            'inurl:"plesk" intitle:"login"',
            'inurl:":8880" intitle:"Plesk"',
        ]
    },
    18: {
        "name": "Webmin Panel Siteler",
        "file": "webmin_panel_siteler",
        "queries": [
            'inurl:":10000" intitle:"Webmin"',
            'intitle:"Webmin" inurl:"10000"',
            'inurl:":10000/index.cgi"',
            'intitle:"Webmin Server Index"',
            'inurl:"webmin" intitle:"login"',
        ]
    },
    19: {
        "name": "Magento Admin Paneli",
        "file": "magento_admin_siteler",
        "queries": [
            'inurl:"/index.php/admin/" intitle:"Magento"',
            'inurl:"/admin/" intitle:"Magento Admin"',
            'intext:"Magento" inurl:"admin/dashboard"',
            'inurl:"/downloader/" intitle:"Magento"',
            'intitle:"Magento Admin" inurl:"admin"',
        ]
    },
    20: {
        "name": "OpenCart Admin Paneli",
        "file": "opencart_admin_siteler",
        "queries": [
            'inurl:"/admin/index.php?route=common/dashboard"',
            'intitle:"Administration | OpenCart"',
            'inurl:"route=account/login" intitle:"OpenCart"',
            'intext:"OpenCart" inurl:"/admin/"',
            'inurl:"opencart" inurl:"admin"',
        ]
    },

    # ══════════════════════════════════════
    #  21-30 | DOSYA AÇIKLARI
    # ══════════════════════════════════════
    21: {
        "name": "Local File Inclusion (LFI)",
        "file": "lfi_acikli_siteler",
        "queries": [
            'inurl:"?page=../" ',
            'inurl:"?file=../" ',
            'inurl:"?include=../" ',
            'inurl:"?lang=../"',
            'inurl:"?path=../"',
        ]
    },
    22: {
        "name": "Remote File Inclusion (RFI)",
        "file": "rfi_acikli_siteler",
        "queries": [
            'inurl:"?page=http://"',
            'inurl:"?file=http://"',
            'inurl:"?include=http://"',
            'inurl:"?src=http://"',
            'inurl:"?url=http://"',
        ]
    },
    23: {
        "name": "Açık config.php Dosyaları",
        "file": "config_php_acik",
        "queries": [
            'inurl:"config.php" intext:"password"',
            'inurl:"wp-config.php.bak"',
            'inurl:"configuration.php.bak"',
            'inurl:"config.php.old"',
            'inurl:"config.php~"',
        ]
    },
    24: {
        "name": "Backup Dosyaları",
        "file": "backup_dosyalari",
        "queries": [
            'inurl:".sql" intext:"CREATE TABLE"',
            'inurl:".bak" intitle:"Index of"',
            'inurl:".backup" intitle:"Index of"',
            'inurl:".old" intext:"password"',
            'inurl:"backup.sql" -site:github.com',
        ]
    },
    25: {
        "name": "Log Dosyaları Açık",
        "file": "log_dosyalari_acik",
        "queries": [
            'inurl:"/logs/" intitle:"Index of" "access.log"',
            'inurl:"error.log" intitle:"Index of"',
            'inurl:"/log/" intitle:"Index of"',
            'inurl:"debug.log" intitle:"Index of"',
            'inurl:"server.log" intext:"error"',
        ]
    },
    26: {
        "name": "Açık .env Dosyaları",
        "file": "env_dosyalari_acik",
        "queries": [
            'inurl:".env" intext:"DB_PASSWORD"',
            'inurl:".env" intext:"APP_KEY"',
            'inurl:".env" intext:"AWS_SECRET"',
            'inurl:".env.example" intext:"password"',
            'inurl:".env.local" intext:"SECRET"',
        ]
    },
    27: {
        "name": "phpinfo() Sayfaları",
        "file": "phpinfo_sayfalar",
        "queries": [
            'inurl:"phpinfo.php" intitle:"phpinfo()"',
            'intitle:"PHP Version" inurl:"phpinfo.php"',
            'intext:"PHP Version" intext:"Server API"',
            'inurl:"info.php" intitle:"phpinfo()"',
            'intext:"phpinfo()" intext:"PHP Extension"',
        ]
    },
    28: {
        "name": "Açık robots.txt Bilgileri",
        "file": "robots_txt_bilgileri",
        "queries": [
            'inurl:"robots.txt" intext:"Disallow: /admin"',
            'inurl:"robots.txt" intext:"Disallow: /backup"',
            'inurl:"robots.txt" intext:"Disallow: /config"',
            'inurl:"robots.txt" intext:"Disallow: /database"',
            'inurl:"robots.txt" intext:"Disallow: /private"',
        ]
    },
    29: {
        "name": "Git/SVN Deposu Açık",
        "file": "git_svn_depolar",
        "queries": [
            'inurl:"/.git/" intitle:"Index of"',
            'inurl:"/.svn/" intitle:"Index of"',
            'inurl:"/.git/config"',
            'inurl:"/.hg/" intitle:"Index of"',
            'intitle:"Index of /.git"',
        ]
    },
    30: {
        "name": "Açık Upload Dizinleri",
        "file": "upload_dizinleri_acik",
        "queries": [
            'intitle:"Index of /uploads"',
            'intitle:"Index of /upload"',
            'intitle:"Index of" inurl:"/uploads/"',
            'intitle:"Index of" inurl:"/files/uploads"',
            'intitle:"Index of /images/uploads"',
        ]
    },

    # ══════════════════════════════════════
    #  31-40 | GÜVENLİK KAMERALARI & IoT
    # ══════════════════════════════════════
    31: {
        "name": "Açık Güvenlik Kameraları",
        "file": "guvenlik_kameralari",
        "queries": [
            'inurl:"/view.shtml" intitle:"Network Camera"',
            'inurl:"/view/index.shtml"',
            'intitle:"Live View / – AXIS"',
            'inurl:"/mjpg/video.mjpg"',
            'intitle:"webcamXP" "start minimized"',
        ]
    },
    32: {
        "name": "IP Kamera Panelleri",
        "file": "ip_kamera_paneller",
        "queries": [
            'intitle:"IP Camera" inurl:"index.htm"',
            'inurl:":8080" intitle:"Security Camera"',
            'inurl:"/cgi-bin/view/index" intitle:"camera"',
            'intitle:"HIKVISION" inurl:"/doc/page/login.asp"',
            'intitle:"DVR Web Client" inurl:"login.asp"',
        ]
    },
    33: {
        "name": "Akıllı Router Panelleri",
        "file": "router_paneller",
        "queries": [
            'intitle:"Router Login" inurl:":80"',
            'intitle:"Linksys Router" inurl:"home.htm"',
            'intitle:"D-Link" inurl:"login.htm"',
            'intitle:"TP-LINK" inurl:"userRpm/LoginRpm.htm"',
            'intitle:"NETGEAR" inurl:"base.htm"',
        ]
    },
    34: {
        "name": "Yazıcı Arayüzleri",
        "file": "yazici_arayuzleri",
        "queries": [
            'intitle:"HP LaserJet" inurl:"/hp/device/this.LCDispatcher"',
            'intitle:"Xerox" inurl:"/wcd/"',
            'intitle:"Ricoh" inurl:"/web/guest/en/websys/"',
            'inurl:"/printer/main.html" intitle:"Printer Status"',
            'intitle:"Canon" inurl:"/portal_top.html"',
        ]
    },
    35: {
        "name": "SCADA / ICS Sistemleri",
        "file": "scada_ics_sistemler",
        "queries": [
            'intitle:"SCADA" inurl:"login"',
            'intitle:"Schneider Electric" inurl:"login"',
            'intitle:"Siemens" inurl:"/Portal/Portal.mwsl"',
            'inurl:"/index.aspx" intitle:"SCADA"',
            'intitle:"HMI" inurl:"login"',
        ]
    },
    36: {
        "name": "VoIP / SIP Servisleri",
        "file": "voip_sip_servisleri",
        "queries": [
            'intitle:"Asterisk Management Portal" inurl:"/index.php"',
            'intitle:"FreePBX" inurl:"/admin/"',
            'inurl:":8088" intitle:"Asterisk"',
            'intitle:"3CX" inurl:"/login"',
            'intitle:"Cisco Unified" inurl:"/ccmuser/login.asp"',
        ]
    },
    37: {
        "name": "Akıllı Ev Sistemleri",
        "file": "akilli_ev_sistemler",
        "queries": [
            'intitle:"Home Automation" inurl:"login"',
            'intitle:"Smart Home" inurl:"/index.html"',
            'inurl:":8123" intitle:"Home Assistant"',
            'intitle:"OpenHAB" inurl:"/basicui/"',
            'inurl:"/homeassistant/" intitle:"login"',
        ]
    },
    38: {
        "name": "Sanayi Kontrol Sistemleri",
        "file": "sanayi_kontrol_sistemler",
        "queries": [
            'intitle:"Building Automation" inurl:"login"',
            'inurl:"/schneider/" intitle:"login"',
            'intitle:"Allen Bradley" inurl:"login"',
            'inurl:"/geovision/" intitle:"security"',
            'intitle:"Modbus" inurl:"monitor"',
        ]
    },
    39: {
        "name": "NAS (Network Storage) Sistemleri",
        "file": "nas_sistemler",
        "queries": [
            'intitle:"QNAP" inurl:"/cgi-bin/authLogin.cgi"',
            'intitle:"Synology" inurl:"/webman/login.cgi"',
            'intitle:"Western Digital" inurl:"login"',
            'intitle:"Buffalo NAS" inurl:"/login.html"',
            'intitle:"FreeNAS" inurl:"/account/login/"',
        ]
    },
    40: {
        "name": "UPS/Güç Sistemleri",
        "file": "ups_guc_sistemler",
        "queries": [
            'intitle:"APC UPS" inurl:"/ups/Login"',
            'intitle:"Eaton" inurl:"/home.htm"',
            'inurl:"/NetworkManagementCard/"',
            'intitle:"Smart-UPS" inurl:"/index.htm"',
            'intitle:"UPS Management" inurl:"login"',
        ]
    },

    # ══════════════════════════════════════
    #  41-50 | VERİ SIZINTISI
    # ══════════════════════════════════════
    41: {
        "name": "Şifre İçeren Dosyalar",
        "file": "sifre_icerik_dosyalar",
        "queries": [
            'filetype:txt intext:"password" intext:"username"',
            'filetype:log intext:"password"',
            'filetype:csv intext:"password"',
            'intext:"pwd=" intext:"user=" filetype:txt',
            'intext:"pass=" intext:"login=" filetype:log',
        ]
    },
    42: {
        "name": "Email Listesi Sızıntısı",
        "file": "email_listesi_sizinti",
        "queries": [
            'filetype:txt intext:"@gmail.com" intext:"password"',
            'filetype:csv intext:"email" intext:"password"',
            'intext:"email" intext:"pass" filetype:txt',
            'filetype:xlsx intext:"password" intext:"email"',
            'intext:"user:pass" filetype:txt',
        ]
    },
    43: {
        "name": "Kredi Kartı Verisi (OSINT)",
        "file": "kredi_karti_veri",
        "queries": [
            'intext:"CVV" intext:"card number" filetype:txt',
            'intext:"credit card" intext:"expiry" filetype:csv',
            'intext:"ccnum" intext:"cvv" filetype:txt',
            'intext:"card_number" intext:"card_cvv" filetype:log',
            'intext:"cc:" intext:"exp:" filetype:txt',
        ]
    },
    44: {
        "name": "FTP Açık Sunucular",
        "file": "ftp_acik_sunucular",
        "queries": [
            'intitle:"Index of /" "ftp://"',
            'inurl:"ftp://" intitle:"Index of"',
            'inurl:"ftp" intitle:"Index of" "password"',
            '"ftp://" intext:"USER anonymous"',
            'inurl:"ftp://" filetype:txt',
        ]
    },
    45: {
        "name": "SSH Key Sızıntıları",
        "file": "ssh_key_sizinti",
        "queries": [
            'intext:"BEGIN RSA PRIVATE KEY" filetype:txt',
            'intext:"BEGIN DSA PRIVATE KEY" filetype:pem',
            'inurl:"id_rsa" intitle:"Index of"',
            'intext:"ssh-rsa" inurl:".pub" filetype:txt',
            'intext:"BEGIN OPENSSH PRIVATE KEY"',
        ]
    },
    46: {
        "name": "API Anahtarı Sızıntısı",
        "file": "api_anahtar_sizinti",
        "queries": [
            'intext:"api_key" intext:"secret" filetype:txt',
            'intext:"AWS_SECRET_ACCESS_KEY" filetype:env',
            'intext:"STRIPE_SECRET_KEY" filetype:txt',
            'intext:"client_secret" intext:"client_id" filetype:json',
            'intext:"api_key=" intext:"secret_key=" filetype:txt',
        ]
    },
    47: {
        "name": "Veritabanı Dump Dosyaları",
        "file": "veritabani_dump",
        "queries": [
            'inurl:".sql" intext:"INSERT INTO" -site:github.com',
            'inurl:"dump.sql" intitle:"Index of"',
            'inurl:"backup.sql" intitle:"Index of"',
            'filetype:sql intext:"password"',
            'inurl:".sql.gz" intitle:"Index of"',
        ]
    },
    48: {
        "name": "Hash Sızıntıları",
        "file": "hash_sizintilari",
        "queries": [
            'intext:"md5" intext:"sha1" intext:"password" filetype:txt',
            'intext:"$1$" intext:"password" filetype:txt',
            'intext:"$2y$" intext:"password" filetype:txt',
            'inurl:"shadow" intitle:"Index of"',
            'intext:"passwd" intext:"shadow" filetype:txt',
        ]
    },
    49: {
        "name": "Kişisel Veri Sızıntısı",
        "file": "kisisel_veri_sizinti",
        "queries": [
            'filetype:csv intext:"ssn" intext:"name"',
            'filetype:xls intext:"social security"',
            'filetype:csv intext:"date of birth" intext:"name"',
            'intext:"TC Kimlik" filetype:txt',
            'intext:"kimlik no" filetype:csv',
        ]
    },
    50: {
        "name": "Parolaları Açık Sayfalar",
        "file": "parola_acik_sayfalar",
        "queries": [
            'intext:"password" intext:"username" inurl:"login"',
            'inurl:"passwd" intext:"root"',
            'intext:"default password" intitle:"login"',
            'intext:"admin:admin" inurl:"login"',
            'intext:"username:admin password:admin"',
        ]
    },

    # ══════════════════════════════════════
    #  51-60 | WEB UYGULAMA AÇIKLARI
    # ══════════════════════════════════════
    51: {
        "name": "XSS Açıklı Sayfalar",
        "file": "xss_acikli_sayfalar",
        "queries": [
            'inurl:"search.php?q="',
            'inurl:"?q=" inurl:".php"',
            'inurl:"?search=" inurl:".php"',
            'inurl:"?keyword=" inurl:".php"',
            'inurl:"?s=" inurl:"wordpress"',
        ]
    },
    52: {
        "name": "CSRF Açıklı Formlar",
        "file": "csrf_acikli_formlar",
        "queries": [
            'inurl:"transfer.php" intext:"amount"',
            'inurl:"payment.php" intext:"amount"',
            'inurl:"send.php" intext:"to" intext:"amount"',
            'inurl:"change_password.php"',
            'inurl:"update_email.php"',
        ]
    },
    53: {
        "name": "Açık Redirect Sayfaları",
        "file": "acik_redirect_sayfalar",
        "queries": [
            'inurl:"redirect.php?url="',
            'inurl:"?next=http"',
            'inurl:"?return=http"',
            'inurl:"?goto=http"',
            'inurl:"?continue=http"',
        ]
    },
    54: {
        "name": "SSRF Açıklı Sayfalar",
        "file": "ssrf_acikli_sayfalar",
        "queries": [
            'inurl:"?url=http://"',
            'inurl:"?fetch=http://"',
            'inurl:"?load=http://"',
            'inurl:"?proxy=http://"',
            'inurl:"?dest=http://"',
        ]
    },
    55: {
        "name": "Açık API Endpoint'leri",
        "file": "acik_api_endpointler",
        "queries": [
            'inurl:"/api/v1/users" intitle:"JSON"',
            'inurl:"/api/users" intext:"password"',
            'inurl:"/rest/v1/" intext:"{\"id\":"',
            'inurl:"/api/" intext:"\"token\":"',
            'inurl:"/api/v2/admin"',
        ]
    },
    56: {
        "name": "XXE Açıklı Servisler",
        "file": "xxe_acikli_servisler",
        "queries": [
            'inurl:"?xml=" inurl:".php"',
            'inurl:"/xml/request" intext:"<?xml"',
            'inurl:"xmlrpc.php"',
            'inurl:"/api/xml"',
            'inurl:"parseXML" inurl:".php"',
        ]
    },
    57: {
        "name": "Path Traversal Açıkları",
        "file": "path_traversal_aciklar",
        "queries": [
            'inurl:"?file=../../../../"',
            'inurl:"?doc=../../../"',
            'inurl:"?download=../"',
            'inurl:"?read=../"',
            'inurl:"?view=../../"',
        ]
    },
    58: {
        "name": "Komut Enjeksiyonu (CMD İnjection)",
        "file": "cmd_injection_siteler",
        "queries": [
            'inurl:"ping.php?host="',
            'inurl:"?host=" inurl:"ping"',
            'inurl:"traceroute.php?host="',
            'inurl:"?cmd=" inurl:".php"',
            'inurl:"?command=" inurl:".php"',
        ]
    },
    59: {
        "name": "IDOR Açıklı Sayfalar",
        "file": "idor_acikli_sayfalar",
        "queries": [
            'inurl:"/account?id="',
            'inurl:"/profile?user_id="',
            'inurl:"/order?order_id="',
            'inurl:"/invoice?id="',
            'inurl:"/document?doc_id="',
        ]
    },
    60: {
        "name": "Açık Swagger / API Dökümantasyonu",
        "file": "swagger_acik_dokumanlar",
        "queries": [
            'inurl:"/swagger-ui.html"',
            'inurl:"/api-docs/" intitle:"Swagger"',
            'inurl:"/swagger/" intitle:"Swagger UI"',
            'intitle:"Swagger UI" inurl:"/docs"',
            'inurl:"/openapi.json"',
        ]
    },

    # ══════════════════════════════════════
    #  61-70 | SUNUCU & ALTYAPI
    # ══════════════════════════════════════
    61: {
        "name": "Apache Dizin Listeleme",
        "file": "apache_dizin_listele",
        "queries": [
            'intitle:"Index of /" -inurl:".html"',
            'intitle:"Index of" "Apache" inurl:"/var/www"',
            '"Apache/2" intitle:"Index of"',
            'intitle:"Apache Status" inurl:"/server-status"',
            'intitle:"Index of /" intext:"Apache Server"',
        ]
    },
    62: {
        "name": "Nginx Açık Dizinler",
        "file": "nginx_acik_dizinler",
        "queries": [
            'intitle:"Index of" intext:"nginx"',
            '"nginx" intitle:"Index of /"',
            'intitle:"Welcome to nginx" inurl:"/index.html"',
            '"nginx/1." intitle:"Index of"',
            'intext:"nginx/" intext:"server" intitle:"Index of"',
        ]
    },
    63: {
        "name": "IIS Sunucu Hataları",
        "file": "iis_sunucu_hatalar",
        "queries": [
            'intitle:"IIS Windows Server"',
            '"Microsoft-IIS" intitle:"Index of"',
            'intitle:"IIS7" inurl:"/iisstart.htm"',
            'intitle:"IIS 8.5" inurl:"/iis-85.png"',
            'intext:"Microsoft-IIS/8" intitle:"IIS"',
        ]
    },
    64: {
        "name": "Tomcat Manager Açık",
        "file": "tomcat_manager_acik",
        "queries": [
            'inurl:"/manager/html" intitle:"Tomcat"',
            'intitle:"Apache Tomcat" inurl:"/manager"',
            'intext:"Tomcat Manager Application" inurl:"/manager"',
            'inurl:"/tomcat/manager"',
            'intitle:"Tomcat Web Application Manager"',
        ]
    },
    65: {
        "name": "Jenkins Panelleri",
        "file": "jenkins_paneller",
        "queries": [
            'intitle:"Dashboard [Jenkins]"',
            'inurl:":8080" intitle:"Jenkins"',
            'inurl:"/jenkins/" intitle:"Jenkins"',
            'intitle:"Jenkins" inurl:"/job/"',
            'intext:"Jenkins" intitle:"Jenkins" inurl:"/builds"',
        ]
    },
    66: {
        "name": "Elasticsearch Açık",
        "file": "elasticsearch_acik",
        "queries": [
            'inurl:":9200/_cat/indices"',
            'inurl:":9200" intitle:"Elasticsearch"',
            'intext:"elasticsearch" inurl:":9200"',
            'inurl:":9200/_nodes" intext:"cluster"',
            'inurl:"/_search" intext:"elasticsearch"',
        ]
    },
    67: {
        "name": "MongoDB Açık Veritabanı",
        "file": "mongodb_acik",
        "queries": [
            'inurl:":27017" intitle:"MongoDB"',
            'intext:"MongoDB" inurl:":28017"',
            'inurl:":28017/" intext:"listDatabases"',
            'inurl:"mongodb://" intext:"password"',
            'intext:"MongoDB Server Information"',
        ]
    },
    68: {
        "name": "Redis Açık Servisleri",
        "file": "redis_acik_servisler",
        "queries": [
            'intext:"redis_version" inurl:":6379"',
            'intext:"redis" intext:"connected_clients"',
            'inurl:":6379" intext:"NOAUTH Authentication required"',
            'intext:"Redis" intext:"keyspace" inurl:"stats"',
            'intext:"redis-server" intext:"port 6379"',
        ]
    },
    69: {
        "name": "Memcached Açık",
        "file": "memcached_acik",
        "queries": [
            'inurl:":11211" intext:"STAT"',
            'intext:"memcached" inurl:":11211"',
            'intext:"memcached version" inurl:"stats"',
            'inurl:"memcached" intext:"get_hits"',
            'intext:"STAT curr_connections" inurl:"memcache"',
        ]
    },
    70: {
        "name": "Açık Docker API",
        "file": "docker_api_acik",
        "queries": [
            'inurl:":2375/v1/" intext:"docker"',
            'inurl:":2376/v1/" intext:"docker"',
            'inurl:":2375/containers/json"',
            'inurl:":4243/v1.16/"',
            'intext:"Docker Remote API" inurl:"containers"',
        ]
    },

    # ══════════════════════════════════════
    #  71-80 | CMS & PLATFORM AÇIKLARI
    # ══════════════════════════════════════
    71: {
        "name": "WordPress Güvenlik Açıkları",
        "file": "wordpress_aciklar",
        "queries": [
            'inurl:"/wp-content/plugins/" intext:"readme.txt"',
            'inurl:"/wp-content/uploads/" intitle:"Index of"',
            'inurl:"xmlrpc.php" intitle:"XML-RPC server"',
            'inurl:"?author=1" intext:"WordPress"',
            'inurl:"/wp-json/wp/v2/users"',
        ]
    },
    72: {
        "name": "Joomla Güvenlik Açıkları",
        "file": "joomla_aciklar",
        "queries": [
            'inurl:"/administrator/" intext:"Joomla" intext:"error"',
            'inurl:"/components/" intitle:"Index of" intext:"Joomla"',
            'intext:"Joomla! Debug Console"',
            'inurl:"/templates/" intitle:"Index of" intext:"Joomla"',
            'intext:"Joomla" inurl:"configuration.php-dist"',
        ]
    },
    73: {
        "name": "PrestaShop Açıkları",
        "file": "prestashop_aciklar",
        "queries": [
            'inurl:"/modules/" intitle:"Index of" intext:"PrestaShop"',
            'inurl:"/prestashop/admin"',
            'intext:"PrestaShop" inurl:"/config/settings.inc.php"',
            'intitle:"PrestaShop" inurl:"/admin123"',
            'inurl:"/override/" intitle:"Index of" intext:"prestashop"',
        ]
    },
    74: {
        "name": "Laravel Hata Sayfaları",
        "file": "laravel_hata_sayfalari",
        "queries": [
            'intext:"laravel" intext:"APP_DEBUG=true"',
            'intext:"Laravel" inurl:"/storage/logs"',
            'intitle:"Whoops! There was an error" intext:"laravel"',
            'intext:"ErrorException" intext:"Laravel"',
            'inurl:"telescope" intitle:"Laravel Telescope"',
        ]
    },
    75: {
        "name": "Django Hata Sayfaları",
        "file": "django_hata_sayfalari",
        "queries": [
            'intitle:"Django" intext:"DEBUG = True"',
            'intext:"Django Version:" intext:"Exception Type:"',
            'intext:"Django" inurl:"/admin/" intext:"500 Internal"',
            'intitle:"DisallowedHost at /" intext:"Django"',
            'intext:"ImproperlyConfigured" intext:"Django"',
        ]
    },
    76: {
        "name": "Ruby on Rails Açıkları",
        "file": "rails_aciklar",
        "queries": [
            'intext:"ActionView::Template::Error" intext:"Rails"',
            'intext:"Application Trace" intext:"Rails.root"',
            'intext:"ActiveRecord::StatementInvalid" intext:"Rails"',
            'intext:"Rails application started" inurl:"/development"',
            'intext:"NoMethodError in" intext:"ActionController"',
        ]
    },
    77: {
        "name": "Node.js/Express Hataları",
        "file": "nodejs_hata_sayfalari",
        "queries": [
            'intext:"Cannot GET /" intext:"Express"',
            'intext:"Error: ENOENT" intext:"node_modules"',
            'intext:"UnhandledPromiseRejection" inurl:".js"',
            'intext:"ReferenceError:" intext:"node.js"',
            'intitle:"Error" intext:"at Object.<anonymous>"',
        ]
    },
    78: {
        "name": "Spring Boot Actuator Açık",
        "file": "spring_actuator_acik",
        "queries": [
            'inurl:"/actuator" intext:"Spring"',
            'inurl:"/actuator/env" intitle:"Spring"',
            'inurl:"/actuator/beans"',
            'inurl:"/spring-security-rest/api/authentication"',
            'inurl:"/management/health" intext:"Spring"',
        ]
    },
    79: {
        "name": "Grafana Panelleri",
        "file": "grafana_paneller",
        "queries": [
            'inurl:":3000" intitle:"Grafana"',
            'intitle:"Grafana" inurl:"/login"',
            'inurl:"/grafana/" intitle:"Grafana"',
            'intitle:"Grafana" inurl:"/dashboard"',
            'inurl:":3000/d/" intitle:"Grafana"',
        ]
    },
    80: {
        "name": "Kibana Panelleri",
        "file": "kibana_paneller",
        "queries": [
            'inurl:":5601" intitle:"Kibana"',
            'intitle:"Kibana" inurl:"/app/kibana"',
            'inurl:"/kibana/" intitle:"Kibana"',
            'intitle:"Kibana" inurl:"/discover"',
            'inurl:"5601/api/status" intext:"Kibana"',
        ]
    },

    # ══════════════════════════════════════
    #  81-90 | AĞ & PROTOKOL AÇIKLARI
    # ══════════════════════════════════════
    81: {
        "name": "VPN Login Panelleri",
        "file": "vpn_login_paneller",
        "queries": [
            'intitle:"VPN" inurl:"login"',
            'intitle:"Cisco AnyConnect" inurl:"/+webvpn+/"',
            'intitle:"Pulse Secure" inurl:"/dana-na/auth/"',
            'intitle:"OpenVPN Web GUI" inurl:"/login"',
            'inurl:"/remote/login" intitle:"FortiGate"',
        ]
    },
    82: {
        "name": "RDP (Uzak Masaüstü) Açık",
        "file": "rdp_acik_sistemler",
        "queries": [
            'inurl:"/tsweb/" intitle:"Remote Desktop"',
            'intitle:"Remote Desktop Web Connection"',
            'inurl:"/Remote/" intitle:"Remote"',
            'inurl:"/rdweb/" intitle:"Remote Desktop"',
            'intitle:"Windows Remote Desktop" inurl:"rdweb"',
        ]
    },
    83: {
        "name": "Telnet/SSH Hizmetleri",
        "file": "telnet_ssh_hizmetler",
        "queries": [
            'inurl:":23" intext:"login" intitle:"Telnet"',
            'inurl:":22" intext:"OpenSSH"',
            'intitle:"Network Login" inurl:":23"',
            'intext:"SSH-2.0" inurl:":22"',
            'inurl:"telnet://" intext:"login"',
        ]
    },
    84: {
        "name": "SNMP Açık Cihazlar",
        "file": "snmp_acik_cihazlar",
        "queries": [
            'inurl:":161" intext:"SNMP"',
            'intitle:"SNMP" inurl:"monitor"',
            'inurl:"snmpwalk" intext:"community"',
            'intext:"SNMP community string" inurl:"config"',
            'inurl:"/snmp/" intitle:"SNMP"',
        ]
    },
    85: {
        "name": "SMTP Mail Sunucuları",
        "file": "smtp_mail_sunucular",
        "queries": [
            'inurl:":25" intext:"SMTP"',
            'inurl:"/webmail/" intitle:"login"',
            'intitle:"Roundcube Webmail" inurl:"/webmail"',
            'intitle:"SquirrelMail" inurl:"/webmail"',
            'inurl:"/horde/" intitle:"Horde"',
        ]
    },
    86: {
        "name": "Açık Proxy Listesi",
        "file": "acik_proxy_listesi",
        "queries": [
            'inurl:"proxy.php" intext:"address"',
            'inurl:"?url=" inurl:"proxy"',
            'intitle:"CGI Proxy" inurl:"cgi-bin"',
            'inurl:"/glype/" intitle:"Glype"',
            'inurl:"/phproxy/" intitle:"PHP Proxy"',
        ]
    },
    87: {
        "name": "Açık DNS Resolver",
        "file": "acik_dns_resolver",
        "queries": [
            'intext:"DNS Server" inurl:"/dns/"',
            'inurl:":53" intext:"dns"',
            'intitle:"DNS Lookup" inurl:"/nslookup"',
            'inurl:"/dig.php" intitle:"DNS"',
            'intext:"BIND 9" intext:"named version"',
        ]
    },
    88: {
        "name": "Network Monitör Sayfaları",
        "file": "network_monitor_sayfalar",
        "queries": [
            'intitle:"Cacti" inurl:"/cacti/graph_view.php"',
            'inurl:"/nagios/" intitle:"Nagios"',
            'inurl:"/zabbix/" intitle:"Zabbix"',
            'inurl:"/prtg/" intitle:"PRTG"',
            'intitle:"Observium" inurl:"/login"',
        ]
    },
    89: {
        "name": "Açık MQTT Broker",
        "file": "mqtt_broker_acik",
        "queries": [
            'inurl:":1883" intext:"MQTT"',
            'inurl:":9001" intext:"MQTT"',
            'intitle:"MQTT" inurl:"broker"',
            'intext:"MQTT Broker" inurl:"dashboard"',
            'inurl:"/mqtt/" intext:"connected"',
        ]
    },
    90: {
        "name": "Açık Syslog Sunucuları",
        "file": "syslog_sunucular",
        "queries": [
            'intitle:"Syslog" inurl:"dashboard"',
            'inurl:"/syslog/" intitle:"Log Viewer"',
            'inurl:":514" intext:"syslog"',
            'intitle:"Graylog" inurl:"/login"',
            'inurl:"/loggly/" intitle:"Syslog"',
        ]
    },

    # ══════════════════════════════════════
    #  91-100 | ÖZEL HEDEFLER
    # ══════════════════════════════════════
    91: {
        "name": "Eğitim Kurumları Açıkları",
        "file": "egitim_kurumu_aciklar",
        "queries": [
            'site:.edu inurl:"admin" inurl:"login"',
            'site:.edu intext:"sql error"',
            'site:.edu inurl:"phpmyadmin"',
            'site:.edu inurl:"?id=" inurl:".php"',
            'site:.edu intitle:"Index of /"',
        ]
    },
    92: {
        "name": "Devlet Siteleri Açıkları",
        "file": "devlet_sitesi_aciklar",
        "queries": [
            'site:.gov inurl:"admin" inurl:"login"',
            'site:.gov intext:"sql error"',
            'site:.gov inurl:"?id=" inurl:".php"',
            'site:.gov intitle:"Index of /"',
            'site:.gov.tr inurl:"admin"',
        ]
    },
    93: {
        "name": "Bankacılık / Fintech Açıkları",
        "file": "bankacilik_aciklar",
        "queries": [
            'site:.bank inurl:"login"',
            'inurl:"online_banking" inurl:"login"',
            'intitle:"Internet Banking" inurl:"login"',
            'inurl:"/netbanking/" intitle:"login"',
            'inurl:"/ibanking/" intitle:"login"',
        ]
    },
    94: {
        "name": "E-Ticaret Siteleri",
        "file": "eticaret_aciklar",
        "queries": [
            'inurl:"shop" inurl:"?id=" inurl:".php"',
            'inurl:"cart.php?id="',
            'inurl:"product.php?id=" inurl:"shop"',
            'inurl:"checkout" inurl:"?id=" inurl:".php"',
            'inurl:"buy.php?id=" inurl:"shop"',
        ]
    },
    95: {
        "name": "Hastane / Sağlık Sistemleri",
        "file": "saglik_sistem_aciklar",
        "queries": [
            'site:.health inurl:"login"',
            'inurl:"hospital" inurl:"admin" inurl:"login"',
            'intitle:"Hospital Management" inurl:"login"',
            'inurl:"/ehr/" inurl:"login"',
            'intitle:"Patient Portal" inurl:"login"',
        ]
    },
    96: {
        "name": "Büyük Boyutlu Dosyalar (OSINT)",
        "file": "buyuk_dosyalar_osint",
        "queries": [
            'filetype:xls intext:"username" intext:"password"',
            'filetype:xlsx intext:"SSN" intext:"name"',
            'filetype:doc intext:"confidential" intext:"password"',
            'filetype:pdf intext:"username" intext:"password"',
            'filetype:csv intext:"password" intext:"email"',
        ]
    },
    97: {
        "name": "Açık Konfigürasyon Dosyaları",
        "file": "konfigurasyon_dosyalar",
        "queries": [
            'inurl:"web.config" intext:"password"',
            'inurl:"application.properties" intext:"password"',
            'inurl:"database.yml" intext:"password"',
            'inurl:"settings.py" intext:"SECRET_KEY"',
            'inurl:"appsettings.json" intext:"password"',
        ]
    },
    98: {
        "name": "Hata Mesajı İçeren Sayfalar",
        "file": "hata_mesaji_sayfalar",
        "queries": [
            'intext:"Fatal error" inurl:".php"',
            'intext:"Warning: include(" inurl:".php"',
            'intext:"Call Stack" intext:"PHP Warning"',
            'intext:"Parse error: syntax error" inurl:".php"',
            'intext:"Notice: Undefined variable" inurl:".php"',
        ]
    },
    99: {
        "name": "IoT Cihaz Kontrol Paneli",
        "file": "iot_kontrol_paneller",
        "queries": [
            'intitle:"IoT" inurl:"dashboard" inurl:"login"',
            'intitle:"Device Management" inurl:"iot"',
            'inurl:"/iot/" intitle:"control panel"',
            'intitle:"Smart Device" inurl:"/login"',
            'inurl:"/device/" intitle:"management"',
        ]
    },
    100: {
        "name": "Sosyal Mühendislik Hedefleri",
        "file": "sosyal_muhendislik_hedef",
        "queries": [
            'intext:"employee list" filetype:xls',
            'intext:"staff directory" filetype:pdf',
            'intext:"company" intext:"contact" filetype:csv',
            'intext:"CEO" intext:"email" filetype:xls',
            'intext:"employee" intext:"phone" filetype:csv',
        ]
    },
}

# ─── USER AGENT HAVUZU ────────────────────────────────────────────────────────
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.91",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

SAVE_DIR = "acikli_siteler"

# ─── HEADER OLUŞTUR ──────────────────────────────────────────────────────────
def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
    }

# ─── BANNER ──────────────────────────────────────────────────────────────────
def banner():
    cls()
    print(f"""
{R}██████╗  ██████╗ ██████╗ ██╗  ██╗    ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ {RST}
{Y}██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗{RST}
{G}██║  ██║██║   ██║██████╔╝█████╔╝     ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝{RST}
{C}██║  ██║██║   ██║██╔══██╗██╔═██╗     ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗{RST}
{M}██████╔╝╚██████╔╝██║  ██║██║  ██╗    ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║{RST}
{B}╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝{RST}

{DG}╔══════════════════════════════════════════════════════════════════════════════════════╗{RST}
{DG}║{RST}  {BLD}{W}Profesyonel Dork Arama Motoru{RST} {DG}|{RST} {G}100+ Kategori{RST} {DG}|{RST} {Y}Milyarlarca Hedef{RST} {DG}|{RST} {C}Otomatik Kayıt{RST}  {DG}║{RST}
{DG}╚══════════════════════════════════════════════════════════════════════════════════════╝{RST}
   {R}⚠  YASAL UYARI:{RST} {W}Bu araç yalnızca yasal güvenlik testleri için kullanılmalıdır.{RST}
   {R}⚠  SORUMLULUK:{RST} {W}Kullanıcı, bu araçla gerçekleştirilen her türlü eylemden sorumludur.{RST}
""")

# ─── MENÜ GÖSTER ─────────────────────────────────────────────────────────────
def show_menu():
    categories = [
        ("1-10",   "SQL ENJEKSİYONU",        R),
        ("11-20",  "ADMİN PANELLERİ",         Y),
        ("21-30",  "DOSYA & DİZİN AÇIKLARI",  G),
        ("31-40",  "GÜVENLİK KAMERALARI/IoT", C),
        ("41-50",  "VERİ SIZINTISI",           M),
        ("51-60",  "WEB UYGULAMA AÇIKLARI",   B),
        ("61-70",  "SUNUCU & ALTYAPI",         R),
        ("71-80",  "CMS & PLATFORM AÇIKLARI", Y),
        ("81-90",  "AĞ & PROTOKOL AÇIKLARI",  G),
        ("91-100", "ÖZEL HEDEFLER",            C),
    ]

    print(f"\n{DG}{'═'*86}{RST}")
    print(f"  {BLD}{W}KATEGORİ GRUPLARI:{RST}")
    print(f"{DG}{'═'*86}{RST}\n")

    for rng, label, color in categories:
        print(f"  {color}[{rng:>7}]{RST}  {BLD}{W}{label}{RST}")

    print(f"\n{DG}{'─'*86}{RST}")
    print(f"\n  {BLD}{W}TÜM SEÇENEKLERİ GÖRMEK İÇİN BİR ARALIK GİRİN{RST}")
    print(f"  {G}Örnek:{RST} {Y}1-10{RST} (SQL kategorileri için)")
    print(f"  {G}veya doğrudan numara:{RST} {Y}42{RST} (Email Listesi Sızıntısı)")
    print(f"  {G}Tümünü görmek için:{RST} {Y}menu{RST}")
    print(f"  {R}Çıkış için:{RST} {Y}q{RST} veya {Y}exit{RST}\n")
    print(f"{DG}{'═'*86}{RST}\n")

# ─── DETAYLI MENÜ ────────────────────────────────────────────────────────────
def show_full_menu(start=1, end=100):
    colors = [R, Y, G, C, M, B]
    groups = {
        (1,10):   ("SQL ENJEKSİYONU",         R),
        (11,20):  ("ADMİN PANELLERİ",          Y),
        (21,30):  ("DOSYA & DİZİN AÇIKLARI",   G),
        (31,40):  ("GÜVENLİK KAMERALARI/IoT",  C),
        (41,50):  ("VERİ SIZINTISI",            M),
        (51,60):  ("WEB UYGULAMA AÇIKLARI",    B),
        (61,70):  ("SUNUCU & ALTYAPI",          R),
        (71,80):  ("CMS & PLATFORM AÇIKLARI",  Y),
        (81,90):  ("AĞ & PROTOKOL AÇIKLARI",   G),
        (91,100): ("ÖZEL HEDEFLER",             C),
    }

    current_group = None

    for num, data in DORKS.items():
        if num < start or num > end:
            continue

        for (s, e), (glabel, gcolor) in groups.items():
            if s <= num <= e and current_group != (s, e):
                current_group = (s, e)
                print(f"\n{DG}┌{'─'*82}┐{RST}")
                print(f"{DG}│{RST}  {gcolor}{BLD}  ◆  {glabel}  [{s}-{e}]  ◆{RST}{DG}{'':>50}│{RST}")
                print(f"{DG}└{'─'*82}┘{RST}")

        col = colors[num % len(colors)]
        print(f"  {col}[{num:>3}]{RST}  {W}{data['name']}{RST}")

    print(f"\n{DG}{'═'*86}{RST}\n")

# ─── BING ARAMA MOTORUöyle ────────────────────────────────────────────────────
def search_bing(query, max_results=100):
    found = []
    page = 0
    session = requests.Session()

    while len(found) < max_results:
        try:
            params = {
                "q": query,
                "first": page * 10 + 1,
                "count": 10,
            }
            url = "https://www.bing.com/search"
            resp = session.get(url, params=params, headers=get_headers(), timeout=10)

            if resp.status_code != 200:
                break

            soup = BeautifulSoup(resp.text, "html.parser")
            results = soup.find_all("li", class_="b_algo")

            if not results:
                break

            for r in results:
                a_tag = r.find("a")
                if a_tag and a_tag.get("href"):
                    href = a_tag["href"]
                    if href.startswith("http") and href not in found:
                        found.append(href)
                        if len(found) >= max_results:
                            break

            page += 1
            time.sleep(random.uniform(1.5, 3.5))

        except requests.exceptions.RequestException:
            time.sleep(2)
            break

    return found

# ─── DUCKDUCKGO ARAMA ────────────────────────────────────────────────────────
def search_ddg(query, max_results=100):
    found = []
    session = requests.Session()
    
    try:
        params = {"q": query, "b": "", "kl": "tr-tr"}
        resp = session.get(
            "https://html.duckduckgo.com/html/",
            params=params,
            headers=get_headers(),
            timeout=15
        )

        if resp.status_code != 200:
            return found

        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.find_all("a", class_="result__url"):
            href = a.get("href", "")
            if not href.startswith("http"):
                href = "https://" + href
            if href not in found and "duckduckgo" not in href:
                found.append(href)
                if len(found) >= max_results:
                    break

        for link in soup.find_all("a"):
            href = link.get("href", "")
            if "/uddg=" in href:
                actual = urllib.parse.unquote(href.split("/uddg=")[-1].split("&")[0])
                if actual.startswith("http") and actual not in found and "duckduckgo" not in actual:
                    found.append(actual)
                    if len(found) >= max_results:
                        break

    except Exception:
        pass

    return found

# ─── ANA ARAMA FONKSİYONU ────────────────────────────────────────────────────
def search_dorking(dork_data, target_count):
    queries = dork_data["queries"]
    all_found = []
    per_query = max(1, (target_count // len(queries)) + 5)

    print(f"\n  {G}[*]{RST} {W}Arama başlıyor...{RST}")
    print(f"  {C}[i]{RST} {W}Hedef:{RST} {Y}{target_count} sonuç{RST}")
    print(f"  {C}[i]{RST} {W}Kullanılan dork sayısı:{RST} {Y}{len(queries)}{RST}\n")

    for i, query in enumerate(queries, 1):
        if len(all_found) >= target_count:
            break

        print(f"  {B}[{i}/{len(queries)}]{RST} {DG}Dork:{RST} {W}{query[:60]}...{RST}" if len(query) > 60
              else f"  {B}[{i}/{len(queries)}]{RST} {DG}Dork:{RST} {W}{query}{RST}")

        # Bing ile dene
        results = search_bing(query, per_query)
        if len(results) < 3:
            # DuckDuckGo ile dene
            print(f"  {Y}  ↳ Bing yetersiz, DuckDuckGo deneniyor...{RST}")
            results = search_ddg(query, per_query)

        new_count = 0
        for url in results:
            if url not in all_found:
                all_found.append(url)
                new_count += 1

        progress_pct = min(100, int(len(all_found) / target_count * 100))
        bar_len = 40
        filled = int(bar_len * progress_pct / 100)
        bar = f"{G}{'█' * filled}{DG}{'░' * (bar_len - filled)}{RST}"
        print(f"  {bar} {Y}{progress_pct}%{RST}  {G}+{new_count}{RST} yeni  |  {W}Toplam: {len(all_found)}{RST}\n")
        
        time.sleep(random.uniform(2, 4))

    return all_found[:target_count]

# ─── SONUÇLARI KAYDET ────────────────────────────────────────────────────────
def save_results(dork_data, results):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    filename = os.path.join(SAVE_DIR, f"{dork_data['file']}.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    mode = "a" if os.path.exists(filename) else "w"

    with open(filename, mode, encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"  Tarama: {dork_data['name']}\n")
        f.write(f"  Tarih : {timestamp}\n")
        f.write(f"  Bulgu : {len(results)} site\n")
        f.write(f"{'='*60}\n\n")
        for i, url in enumerate(results, 1):
            f.write(f"{i:>5}. {url}\n")
        f.write("\n")

    return filename

# ─── ANA AKIŞ ────────────────────────────────────────────────────────────────
def main():
    banner()
    show_menu()

    while True:
        try:
            choice_raw = input(f"\n  {G}dork@hunter{RST}{DG}:{RST}{B}~{RST} ").strip().lower()

            if choice_raw in ("q", "exit", "quit", "çıkış"):
                print(f"\n  {Y}[!] Çıkılıyor... Hoşça kal!{RST}\n")
                sys.exit(0)

            if choice_raw == "menu":
                banner()
                show_full_menu()
                continue

            # Aralık kontrolü (örn: 1-10)
            if "-" in choice_raw and not choice_raw.startswith("-"):
                parts = choice_raw.split("-")
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    start, end = int(parts[0]), int(parts[1])
                    banner()
                    show_full_menu(start, end)
                    continue

            if not choice_raw.isdigit():
                print(f"\n  {R}[!] Geçersiz giriş. Bir numara veya aralık girin.{RST}")
                continue

            choice = int(choice_raw)

            if choice not in DORKS:
                print(f"\n  {R}[!] Geçersiz seçim. 1-100 arasında bir değer girin.{RST}")
                continue

            dork_data = DORKS[choice]
            banner()

            print(f"\n{DG}{'═'*86}{RST}")
            print(f"  {BLD}{Y}SEÇİLEN:{RST}  {BLD}{W}{dork_data['name']}{RST}")
            print(f"  {BLD}{C}DOSYA  :{RST}  {G}{SAVE_DIR}/{dork_data['file']}.txt{RST}")
            print(f"{DG}{'═'*86}{RST}")

            while True:
                count_raw = input(f"\n  {C}[?]{RST} {W}Kaç tane site bulmamı istersin?{RST} {DG}(min 1, maks 500):{RST} ").strip()
                if not count_raw.isdigit():
                    print(f"  {R}[!] Lütfen sayısal bir değer girin.{RST}")
                    continue
                count = int(count_raw)
                if count < 1:
                    count = 1
                elif count > 500:
                    print(f"  {Y}[!] Maksimum 500 olarak sınırlandırıldı.{RST}")
                    count = 500
                break

            print(f"\n  {G}[✔]{RST} {W}Arama başlatılıyor...{RST}")
            print(f"  {Y}[!]{RST} {DG}Lütfen bekleyin, bu işlem birkaç dakika sürebilir.{RST}")

            results = search_dorking(dork_data, count)

            print(f"\n{DG}{'═'*86}{RST}")
            print(f"  {BLD}{G}SONUÇLAR{RST}")
            print(f"{DG}{'═'*86}{RST}\n")

            if not results:
                print(f"  {R}[✗] Sonuç bulunamadı. Farklı bir dork kategorisi deneyin.{RST}")
            else:
                for i, url in enumerate(results, 1):
                    color = [G, C, Y, M, B][i % 5]
                    print(f"  {DG}{i:>4}.{RST} {color}{url}{RST}")

                print(f"\n{DG}{'─'*86}{RST}")
                print(f"  {BLD}{G}[✔] TOPLAM BULUNAN:{RST} {BLD}{W}{len(results)}{RST} {G}site{RST}")

                # 10'dan fazlaysa otomatik kaydet
                if len(results) >= 1:
                    filename = save_results(dork_data, results)
                    print(f"  {BLD}{C}[💾] KAYDEDILDI    :{RST} {BLD}{Y}{filename}{RST}")
                    
                    if len(results) > 10:
                        print(f"\n  {G}[✔]{RST} {W}10'dan fazla site bulundu, otomatik olarak dosyaya yazıldı!{RST}")

            print(f"\n{DG}{'═'*86}{RST}")
            input(f"\n  {DG}[Enter'a bas devam et]{RST} ")
            banner()
            show_menu()

        except KeyboardInterrupt:
            print(f"\n\n  {Y}[!] Ctrl+C algılandı. Çıkılıyor...{RST}\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n  {R}[!] Hata: {e}{RST}")
            time.sleep(1)

# ─── GİRİŞ NOKTASI ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Bağımlılık kontrolü
    missing = []
    try:
        import requests
    except ImportError:
        missing.append("requests")
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        missing.append("beautifulsoup4")

    if missing:
        print(f"\n{R}[!] Eksik bağımlılık:{RST} {', '.join(missing)}")
        print(f"{Y}[i] Yüklemek için:{RST}")
        print(f"    {G}pip install {' '.join(missing)}{RST}")
        print(f"    veya: {G}pip3 install {' '.join(missing)}{RST}\n")
        sys.exit(1)

    main()
